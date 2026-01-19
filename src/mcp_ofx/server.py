"""
MCP Server for OpenFX SDK.

Provides tools for looking up OFX API definitions and generating code.
"""

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools.lookup import (
    lookup_definition,
    search_definitions,
    list_category,
    get_categories,
    get_actions,
    get_action_sequence,
    get_suite_functions,
    get_param_type_info,
    get_context_requirements,
    get_host_info,
)
from .tools.codegen import (
    generate_plugin_skeleton,
    generate_parameter_code,
)
from .data import (
    STATUS_CODES,
    CORE_ACTIONS,
    IMAGE_EFFECT_ACTIONS,
    CONTEXTS,
    PARAM_TYPES,
    BIT_DEPTHS,
    IMAGE_COMPONENTS,
    SUITES,
    HOST_COMPATIBILITY,
)


app = Server("mcp-ofx")


@app.list_tools()
async def list_tools():
    """List available OFX tools."""
    return [
        Tool(
            name="ofx_lookup",
            description="Look up an OFX definition by exact name (e.g., 'kOfxStatOK', 'kOfxActionDescribe', 'kOfxParamTypeDouble')",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The OFX constant name to look up"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="ofx_search",
            description="Search OFX definitions by keyword. Returns all matching definitions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches names and descriptions)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional: limit search to category (status_codes, core_actions, image_effect_actions, contexts, param_types, bit_depths, image_components, suites, etc.)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="ofx_list_category",
            description="List all definitions in a category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name: status_codes, core_actions, image_effect_actions, contexts, param_types, bit_depths, image_components, field_types, premult_states, thread_safety, change_reasons, suites, standard_clips, standard_params, gpu_properties, type_identifiers, data_structures, exported_functions"
                    }
                },
                "required": ["category"]
            }
        ),
        Tool(
            name="ofx_get_actions",
            description="Get all OFX actions (both core and image effect actions) with their details",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="ofx_action_sequence",
            description="Get the typical action call sequence for OFX plugins",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Plugin context (filter, generator, transition, general, retimer, paint)"
                    }
                }
            }
        ),
        Tool(
            name="ofx_get_suite",
            description="Get details about an OFX suite including all its functions",
            inputSchema={
                "type": "object",
                "properties": {
                    "suite_name": {
                        "type": "string",
                        "description": "Suite name (e.g., 'kOfxPropertySuite', 'kOfxImageEffectSuite', 'kOfxParameterSuite')"
                    }
                },
                "required": ["suite_name"]
            }
        ),
        Tool(
            name="ofx_get_context",
            description="Get details about an OFX image effect context including required clips and params",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Context name (e.g., 'kOfxImageEffectContextFilter')"
                    }
                },
                "required": ["context"]
            }
        ),
        Tool(
            name="ofx_get_param_type",
            description="Get details about an OFX parameter type",
            inputSchema={
                "type": "object",
                "properties": {
                    "param_type": {
                        "type": "string",
                        "description": "Parameter type (e.g., 'kOfxParamTypeDouble', 'kOfxParamTypeChoice')"
                    }
                },
                "required": ["param_type"]
            }
        ),
        Tool(
            name="ofx_host_compatibility",
            description="Get compatibility information for a specific host application",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "Host name (e.g., 'DaVinci Resolve', 'Nuke', 'Fusion')"
                    }
                },
                "required": ["host"]
            }
        ),
        Tool(
            name="ofx_generate_plugin",
            description="Generate a complete OFX plugin skeleton code",
            inputSchema={
                "type": "object",
                "properties": {
                    "plugin_name": {
                        "type": "string",
                        "description": "Human-readable plugin name"
                    },
                    "plugin_id": {
                        "type": "string",
                        "description": "Unique plugin identifier (e.g., 'com.company.myplugin')"
                    },
                    "context": {
                        "type": "string",
                        "description": "Plugin context (default: kOfxImageEffectContextFilter)"
                    },
                    "params": {
                        "type": "array",
                        "description": "List of parameter definitions [{name, type, label, default, min, max}]",
                        "items": {
                            "type": "object"
                        }
                    },
                    "supports_gpu": {
                        "type": "boolean",
                        "description": "Include GPU rendering support"
                    }
                },
                "required": ["plugin_name", "plugin_id"]
            }
        ),
        Tool(
            name="ofx_generate_param",
            description="Generate code for defining a single OFX parameter",
            inputSchema={
                "type": "object",
                "properties": {
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name"
                    },
                    "param_type": {
                        "type": "string",
                        "description": "Parameter type constant (e.g., 'kOfxParamTypeDouble')"
                    },
                    "label": {
                        "type": "string",
                        "description": "Display label"
                    },
                    "default": {
                        "description": "Default value"
                    },
                    "min": {
                        "description": "Minimum value"
                    },
                    "max": {
                        "description": "Maximum value"
                    },
                    "hint": {
                        "type": "string",
                        "description": "Tooltip hint"
                    }
                },
                "required": ["param_name", "param_type"]
            }
        ),
        Tool(
            name="ofx_summary",
            description="Get a summary of the OFX SDK structure and main components",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""

    if name == "ofx_lookup":
        result = lookup_definition(arguments["name"])
        if result:
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        return [TextContent(type="text", text=f"Definition '{arguments['name']}' not found")]

    elif name == "ofx_search":
        results = search_definitions(
            arguments["query"],
            arguments.get("category")
        )
        if results:
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        return [TextContent(type="text", text=f"No results found for '{arguments['query']}'")]

    elif name == "ofx_list_category":
        items = list_category(arguments["category"])
        if items:
            return [TextContent(type="text", text=json.dumps(items, indent=2))]
        categories = get_categories()
        return [TextContent(type="text", text=f"Category not found. Available: {categories}")]

    elif name == "ofx_get_actions":
        actions = get_actions()
        return [TextContent(type="text", text=json.dumps(actions, indent=2))]

    elif name == "ofx_action_sequence":
        context = arguments.get("context", "filter")
        sequence = get_action_sequence(context)
        return [TextContent(type="text", text=json.dumps(sequence, indent=2))]

    elif name == "ofx_get_suite":
        suite_name = arguments["suite_name"]
        if suite_name in SUITES:
            return [TextContent(type="text", text=json.dumps(SUITES[suite_name], indent=2))]
        return [TextContent(type="text", text=f"Suite '{suite_name}' not found. Available: {list(SUITES.keys())}")]

    elif name == "ofx_get_context":
        context = arguments["context"]
        info = get_context_requirements(context)
        if info:
            return [TextContent(type="text", text=json.dumps(info, indent=2))]
        return [TextContent(type="text", text=f"Context not found. Available: {list(CONTEXTS.keys())}")]

    elif name == "ofx_get_param_type":
        param_type = arguments["param_type"]
        info = get_param_type_info(param_type)
        if info:
            return [TextContent(type="text", text=json.dumps(info, indent=2))]
        return [TextContent(type="text", text=f"Param type not found. Available: {list(PARAM_TYPES.keys())}")]

    elif name == "ofx_host_compatibility":
        host = arguments["host"]
        info = get_host_info(host)
        if info:
            return [TextContent(type="text", text=json.dumps(info, indent=2))]
        return [TextContent(type="text", text=f"Host not found. Available: {list(HOST_COMPATIBILITY.keys())}")]

    elif name == "ofx_generate_plugin":
        code = generate_plugin_skeleton(
            plugin_name=arguments["plugin_name"],
            plugin_id=arguments["plugin_id"],
            context=arguments.get("context", "kOfxImageEffectContextFilter"),
            params=arguments.get("params"),
            supports_gpu=arguments.get("supports_gpu", False),
        )
        return [TextContent(type="text", text=code)]

    elif name == "ofx_generate_param":
        code = generate_parameter_code(
            param_name=arguments["param_name"],
            param_type=arguments["param_type"],
            label=arguments.get("label"),
            default=arguments.get("default"),
            min_val=arguments.get("min"),
            max_val=arguments.get("max"),
            hint=arguments.get("hint"),
        )
        return [TextContent(type="text", text=code)]

    elif name == "ofx_summary":
        summary = {
            "name": "OpenFX (OFX) SDK",
            "version": "1.5",
            "source": "https://github.com/AcademySoftwareFoundation/openfx",
            "documentation": "https://openfx.readthedocs.io/",
            "overview": {
                "total_status_codes": len(STATUS_CODES),
                "total_core_actions": len(CORE_ACTIONS),
                "total_image_effect_actions": len(IMAGE_EFFECT_ACTIONS),
                "total_contexts": len(CONTEXTS),
                "total_param_types": len(PARAM_TYPES),
                "total_bit_depths": len(BIT_DEPTHS),
                "total_image_components": len(IMAGE_COMPONENTS),
                "total_suites": len(SUITES),
            },
            "contexts": list(CONTEXTS.keys()),
            "param_types": list(PARAM_TYPES.keys()),
            "suites": list(SUITES.keys()),
            "supported_hosts": list(HOST_COMPATIBILITY.keys()),
            "key_concepts": [
                "Property System - All configuration via typed key-value pairs",
                "Suite Mechanism - Hosts provide function pointers via suites",
                "Action System - Hosts communicate with plugins via action strings",
                "Contexts - Plugins declare supported contexts (filter, generator, etc.)",
                "Clips - Named inputs/outputs for image data",
                "Parameters - User-controllable values with animation support",
            ]
        }
        return [TextContent(type="text", text=json.dumps(summary, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
