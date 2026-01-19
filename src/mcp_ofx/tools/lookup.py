"""
OFX SDK lookup tools for searching and retrieving API definitions.
"""

from typing import Any, Optional
from ..data import (
    STATUS_CODES,
    CORE_ACTIONS,
    IMAGE_EFFECT_ACTIONS,
    CONTEXTS,
    PARAM_TYPES,
    BIT_DEPTHS,
    IMAGE_COMPONENTS,
    FIELD_TYPES,
    PREMULT_STATES,
    THREAD_SAFETY,
    CHANGE_REASONS,
    SUITES,
    STANDARD_CLIPS,
    STANDARD_PARAMS,
    GPU_PROPERTIES,
    TYPE_IDENTIFIERS,
    DATA_STRUCTURES,
    EXPORTED_FUNCTIONS,
    HOST_COMPATIBILITY,
)

# Combined lookup dictionary for searching
ALL_DEFINITIONS = {
    "status_codes": STATUS_CODES,
    "core_actions": CORE_ACTIONS,
    "image_effect_actions": IMAGE_EFFECT_ACTIONS,
    "contexts": CONTEXTS,
    "param_types": PARAM_TYPES,
    "bit_depths": BIT_DEPTHS,
    "image_components": IMAGE_COMPONENTS,
    "field_types": FIELD_TYPES,
    "premult_states": PREMULT_STATES,
    "thread_safety": THREAD_SAFETY,
    "change_reasons": CHANGE_REASONS,
    "suites": SUITES,
    "standard_clips": STANDARD_CLIPS,
    "standard_params": STANDARD_PARAMS,
    "gpu_properties": GPU_PROPERTIES,
    "type_identifiers": TYPE_IDENTIFIERS,
    "data_structures": DATA_STRUCTURES,
    "exported_functions": EXPORTED_FUNCTIONS,
}


def lookup_definition(name: str) -> Optional[dict[str, Any]]:
    """
    Look up an OFX definition by name.

    Args:
        name: The OFX constant name (e.g., 'kOfxStatOK', 'kOfxActionDescribe')

    Returns:
        Dictionary containing the definition details, or None if not found.
    """
    for category, definitions in ALL_DEFINITIONS.items():
        if name in definitions:
            result = definitions[name].copy()
            result["category"] = category
            result["name"] = name
            return result
    return None


def search_definitions(query: str, category: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Search for OFX definitions matching a query string.

    Args:
        query: Search string (case-insensitive)
        category: Optional category to limit search

    Returns:
        List of matching definitions.
    """
    results = []
    query_lower = query.lower()

    categories = [category] if category else ALL_DEFINITIONS.keys()

    for cat in categories:
        if cat not in ALL_DEFINITIONS:
            continue
        for name, definition in ALL_DEFINITIONS[cat].items():
            # Search in name
            if query_lower in name.lower():
                result = definition.copy()
                result["category"] = cat
                result["name"] = name
                results.append(result)
                continue

            # Search in description
            if "description" in definition:
                if query_lower in definition["description"].lower():
                    result = definition.copy()
                    result["category"] = cat
                    result["name"] = name
                    results.append(result)
                    continue

            # Search in value
            if "value" in definition:
                if query_lower in str(definition["value"]).lower():
                    result = definition.copy()
                    result["category"] = cat
                    result["name"] = name
                    results.append(result)

    return results


def list_category(category: str) -> list[str]:
    """
    List all definitions in a category.

    Args:
        category: Category name

    Returns:
        List of definition names in that category.
    """
    if category not in ALL_DEFINITIONS:
        return []
    return list(ALL_DEFINITIONS[category].keys())


def get_categories() -> list[str]:
    """Get all available categories."""
    return list(ALL_DEFINITIONS.keys())


def get_actions() -> dict[str, dict]:
    """Get all actions (core + image effect)."""
    actions = {}
    actions.update(CORE_ACTIONS)
    actions.update(IMAGE_EFFECT_ACTIONS)
    return actions


def get_action_sequence(context: str) -> list[str]:
    """
    Get the typical action sequence for a given context.

    Args:
        context: Plugin context (e.g., 'filter', 'generator')

    Returns:
        List of actions in typical order.
    """
    # Common sequence for all contexts
    sequence = [
        "kOfxActionLoad",
        "kOfxActionDescribe",
        "kOfxImageEffectActionDescribeInContext",
        "kOfxActionCreateInstance",
    ]

    # Runtime actions
    runtime = [
        "kOfxActionBeginInstanceEdit",
        "kOfxActionBeginInstanceChanged",
        "kOfxActionInstanceChanged",
        "kOfxActionEndInstanceChanged",
        "kOfxImageEffectActionGetClipPreferences",
        "kOfxImageEffectActionGetRegionOfDefinition",
        "kOfxImageEffectActionGetRegionsOfInterest",
        "kOfxImageEffectActionGetFramesNeeded",
        "kOfxImageEffectActionIsIdentity",
        "kOfxImageEffectActionBeginSequenceRender",
        "kOfxImageEffectActionRender",
        "kOfxImageEffectActionEndSequenceRender",
        "kOfxActionEndInstanceEdit",
    ]

    # Cleanup
    cleanup = [
        "kOfxActionSyncPrivateData",
        "kOfxActionPurgeCaches",
        "kOfxActionDestroyInstance",
        "kOfxActionUnload",
    ]

    return sequence + runtime + cleanup


def get_suite_functions(suite_name: str) -> Optional[list[dict]]:
    """
    Get function list for a suite.

    Args:
        suite_name: Suite name (e.g., 'kOfxPropertySuite')

    Returns:
        List of function definitions, or None if suite not found.
    """
    if suite_name in SUITES:
        return SUITES[suite_name].get("functions", [])
    return None


def get_param_type_info(param_type: str) -> Optional[dict]:
    """
    Get detailed information about a parameter type.

    Args:
        param_type: Parameter type (e.g., 'kOfxParamTypeDouble')

    Returns:
        Dictionary with parameter type details.
    """
    return PARAM_TYPES.get(param_type)


def get_context_requirements(context: str) -> Optional[dict]:
    """
    Get requirements for a specific context.

    Args:
        context: Context name (e.g., 'kOfxImageEffectContextFilter')

    Returns:
        Dictionary with context requirements.
    """
    return CONTEXTS.get(context)


def get_host_info(host: str) -> Optional[dict]:
    """
    Get compatibility information for a specific host.

    Args:
        host: Host name (e.g., 'DaVinci Resolve')

    Returns:
        Dictionary with host compatibility info.
    """
    return HOST_COMPATIBILITY.get(host)
