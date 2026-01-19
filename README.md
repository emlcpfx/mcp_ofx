# MCP OFX - OpenFX SDK Server

A Model Context Protocol (MCP) server providing comprehensive access to the OpenFX (OFX) SDK for visual effects plugin development.

## Overview

This MCP server exposes the entire OpenFX SDK API, making it easy to:

- Look up any OFX constant, action, property, or suite
- Search the API by keyword
- Get detailed information about contexts, parameter types, and host compatibility
- Generate complete plugin skeleton code
- Understand the action call sequence for plugins

## Installation

```bash
pip install mcp-ofx
```

Or install from source:

```bash
git clone https://github.com/mcp-ofx/mcp-ofx
cd mcp-ofx
pip install -e .
```

## Usage

### As an MCP Server

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "ofx": {
      "command": "mcp-ofx"
    }
  }
}
```

### Available Tools

#### `ofx_lookup`
Look up an OFX definition by exact name.

```
ofx_lookup("kOfxStatOK")
ofx_lookup("kOfxActionDescribe")
ofx_lookup("kOfxParamTypeDouble")
```

#### `ofx_search`
Search definitions by keyword.

```
ofx_search("render")
ofx_search("clip", category="image_effect_actions")
```

#### `ofx_list_category`
List all definitions in a category.

Categories: `status_codes`, `core_actions`, `image_effect_actions`, `contexts`, `param_types`, `bit_depths`, `image_components`, `field_types`, `premult_states`, `thread_safety`, `change_reasons`, `suites`, `standard_clips`, `standard_params`, `gpu_properties`, `type_identifiers`, `data_structures`, `exported_functions`

#### `ofx_get_actions`
Get all OFX actions with their details.

#### `ofx_action_sequence`
Get the typical action call sequence for plugins.

#### `ofx_get_suite`
Get details about an OFX suite including all its functions.

```
ofx_get_suite("kOfxPropertySuite")
ofx_get_suite("kOfxImageEffectSuite")
```

#### `ofx_get_context`
Get details about an image effect context.

```
ofx_get_context("kOfxImageEffectContextFilter")
ofx_get_context("kOfxImageEffectContextTransition")
```

#### `ofx_get_param_type`
Get details about a parameter type.

```
ofx_get_param_type("kOfxParamTypeDouble")
ofx_get_param_type("kOfxParamTypeChoice")
```

#### `ofx_host_compatibility`
Get compatibility information for specific hosts.

```
ofx_host_compatibility("DaVinci Resolve")
ofx_host_compatibility("Nuke")
```

#### `ofx_generate_plugin`
Generate a complete plugin skeleton.

```
ofx_generate_plugin(
    plugin_name="My Blur",
    plugin_id="com.mycompany.myblur",
    context="kOfxImageEffectContextFilter",
    params=[
        {"name": "radius", "type": "kOfxParamTypeDouble", "default": 5.0, "min": 0, "max": 100}
    ],
    supports_gpu=True
)
```

#### `ofx_generate_param`
Generate code for a single parameter definition.

#### `ofx_summary`
Get a summary of the OFX SDK structure.

## OFX SDK Version

This server is based on **OpenFX 1.5** (December 2024) from the Academy Software Foundation.

## Supported Hosts

- DaVinci Resolve
- Nuke (reference implementation)
- Fusion
- Vegas Pro
- And more...

## Resources

- [OpenFX GitHub](https://github.com/AcademySoftwareFoundation/openfx)
- [OpenFX Documentation](https://openfx.readthedocs.io/)
- [OpenFX Website](https://openeffects.org/)

## License

MIT License
