"""
Comprehensive OFX SDK definitions extracted from the official OpenFX headers.
Source: https://github.com/AcademySoftwareFoundation/openfx
Version: OFX 1.5 (December 2024)
"""

# =============================================================================
# STATUS CODES (ofxCore.h)
# =============================================================================

STATUS_CODES = {
    "kOfxStatOK": {
        "value": 0,
        "description": "Status code indicating all was fine",
        "header": "ofxCore.h"
    },
    "kOfxStatFailed": {
        "value": 1,
        "description": "Status error code for a failed operation",
        "header": "ofxCore.h"
    },
    "kOfxStatErrFatal": {
        "value": 2,
        "description": "Status error code for a fatal error. Only returned when the plug-in or host cannot continue to function and needs to be restarted.",
        "header": "ofxCore.h"
    },
    "kOfxStatErrUnknown": {
        "value": 3,
        "description": "Status error code for an operation on or request for an unknown object",
        "header": "ofxCore.h"
    },
    "kOfxStatErrMissingHostFeature": {
        "value": 4,
        "description": "Status error code returned by plug-ins when they are missing host functionality. Plug-Ins returning this should post an appropriate error message.",
        "header": "ofxCore.h"
    },
    "kOfxStatErrUnsupported": {
        "value": 5,
        "description": "Status error code for an unsupported feature/operation",
        "header": "ofxCore.h"
    },
    "kOfxStatErrExists": {
        "value": 6,
        "description": "Status error code for an operation attempting to create something that exists",
        "header": "ofxCore.h"
    },
    "kOfxStatErrFormat": {
        "value": 7,
        "description": "Status error code for an incorrect format",
        "header": "ofxCore.h"
    },
    "kOfxStatErrMemory": {
        "value": 8,
        "description": "Status error code indicating that something failed due to memory shortage",
        "header": "ofxCore.h"
    },
    "kOfxStatErrBadHandle": {
        "value": 9,
        "description": "Status error code for an operation on a bad handle",
        "header": "ofxCore.h"
    },
    "kOfxStatErrBadIndex": {
        "value": 10,
        "description": "Status error code indicating that a given index was invalid or unavailable",
        "header": "ofxCore.h"
    },
    "kOfxStatErrValue": {
        "value": 11,
        "description": "Status error code indicating that something failed due an illegal value",
        "header": "ofxCore.h"
    },
    "kOfxStatReplyYes": {
        "value": 12,
        "description": "OfxStatus returned indicating a 'yes'",
        "header": "ofxCore.h"
    },
    "kOfxStatReplyNo": {
        "value": 13,
        "description": "OfxStatus returned indicating a 'no'",
        "header": "ofxCore.h"
    },
    "kOfxStatReplyDefault": {
        "value": 14,
        "description": "OfxStatus returned indicating that a default action should be performed",
        "header": "ofxCore.h"
    },
    "kOfxStatErrImageFormat": {
        "value": 1000,
        "description": "Error code for incorrect image formats (Image Effect specific)",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# CORE ACTIONS (ofxCore.h)
# =============================================================================

CORE_ACTIONS = {
    "kOfxActionLoad": {
        "value": "OfxActionLoad",
        "description": "First action passed to a plug-in after the binary has been loaded. Used to create global data structures and fetch suites from the host.",
        "handle": "NULL",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["The plugin's setHost function has been called"],
        "post": ["This action will not be called again while the binary remains loaded"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxCore.h"
    },
    "kOfxActionDescribe": {
        "value": "OfxActionDescribe",
        "description": "Second action passed to a plug-in. Plugin defines how it behaves and the resources it needs. Must set supported contexts.",
        "handle": "OfxImageEffectHandle (descriptor)",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionLoad has been called"],
        "post": ["kOfxActionDescribe will not be called again unless it fails", "kOfxImageEffectActionDescribeInContext will be called for each supported context"],
        "returns": ["kOfxStatOK", "kOfxStatErrMissingHostFeature", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxCore.h",
        "required": True
    },
    "kOfxActionUnload": {
        "value": "OfxActionUnload",
        "description": "Last action passed to the plug-in before the binary is unloaded. Used to destroy global data structures.",
        "handle": "NULL",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionLoad has been called", "All instances have been destroyed"],
        "post": ["No other actions will be called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal"],
        "header": "ofxCore.h"
    },
    "kOfxActionCreateInstance": {
        "value": "OfxActionCreateInstance",
        "description": "First action passed to a plug-in's instance after creation. Used to create per-instance data structures.",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionDescribe has been called", "Instance is fully constructed with all objects requested"],
        "post": ["Instance pointer valid until kOfxActionDestroyInstance"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatErrMemory", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionDestroyInstance": {
        "value": "OfxActionDestroyInstance",
        "description": "Last action passed to a plug-in's instance before destruction. Used to destroy per-instance data structures.",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called", "Instance members not yet destroyed"],
        "post": ["Instance pointer is no longer valid"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionPurgeCaches": {
        "value": "OfxActionPurgeCaches",
        "description": "Called in low memory situations. Instance should destroy data structures and release memory.",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionSyncPrivateData": {
        "value": "OfxActionSyncPrivateData",
        "description": "Called when plugin should synchronise private data to its parameter set. Occurs before save or copy.",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called"],
        "post": ["Private state data can be reconstructed from parameter set"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionInstanceChanged": {
        "value": "OfxActionInstanceChanged",
        "description": "Signals that something has changed in a plugin's instance. Bracketed by Begin/EndInstanceChanged.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropType", "kOfxPropName", "kOfxPropChangeReason", "kOfxPropTime", "kOfxImageEffectPropRenderScale"],
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called", "kOfxActionBeginInstanceChanged has been called"],
        "post": ["kOfxActionEndInstanceChanged will be called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionBeginInstanceChanged": {
        "value": "OfxActionBeginInstanceChanged",
        "description": "Brackets the start of a set of kOfxActionInstanceChanged actions.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropChangeReason"],
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called"],
        "post": ["kOfxActionInstanceChanged will be called at least once", "kOfxActionEndInstanceChanged will be called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionEndInstanceChanged": {
        "value": "OfxActionEndInstanceChanged",
        "description": "Brackets the end of a set of kOfxActionInstanceChanged actions.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropChangeReason"],
        "outArgs": "NULL",
        "pre": ["kOfxActionBeginInstanceChanged has been called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionBeginInstanceEdit": {
        "value": "OfxActionBeginInstanceEdit",
        "description": "Called when instance is first actively edited by a user (interface opened).",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called"],
        "post": ["kOfxActionEndInstanceEdit will be called when last editor closes"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
    "kOfxActionEndInstanceEdit": {
        "value": "OfxActionEndInstanceEdit",
        "description": "Called when last user interface on an instance is closed.",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": "NULL",
        "pre": ["kOfxActionBeginInstanceEdit has been called"],
        "post": ["No user interface is open on the instance"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrFatal", "kOfxStatFailed"],
        "header": "ofxCore.h"
    },
}

# =============================================================================
# IMAGE EFFECT ACTIONS (ofxImageEffect.h)
# =============================================================================

IMAGE_EFFECT_ACTIONS = {
    "kOfxImageEffectActionDescribeInContext": {
        "value": "OfxImageEffectActionDescribeInContext",
        "description": "Called for each context the plugin supports. Define parameters and clips per context.",
        "handle": "OfxImageEffectHandle (context descriptor)",
        "inArgs": ["kOfxImageEffectPropContext"],
        "outArgs": "NULL",
        "pre": ["kOfxActionDescribe has been called"],
        "returns": ["kOfxStatOK", "kOfxStatErrMissingHostFeature", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "required": True
    },
    "kOfxImageEffectActionGetRegionOfDefinition": {
        "value": "OfxImageEffectActionGetRegionOfDefinition",
        "description": "Calculate the RoD (output bounds) for the effect at a given frame.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropTime", "kOfxImageEffectPropRenderScale", "kOfxImageEffectPropThumbnailRender (optional)"],
        "outArgs": ["kOfxImageEffectPropRegionOfDefinition"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "default_behavior": {
            "generator": "Project window",
            "filter": "RoD of Source clip",
            "paint": "RoD of Source clip",
            "transition": "Union of SourceFrom and SourceTo RoDs",
            "general": "Union of all non-optional input clips",
            "retimer": "Union of Source at preceding and following SourceTime frames"
        }
    },
    "kOfxImageEffectActionGetRegionsOfInterest": {
        "value": "OfxImageEffectActionGetRegionsOfInterest",
        "description": "Given a region to render, what region is needed from each input clip.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropTime", "kOfxImageEffectPropRenderScale", "kOfxImageEffectPropRegionOfInterest", "kOfxImageEffectPropThumbnailRender (optional)"],
        "outArgs": ["OfxImageClipPropRoI_<ClipName> for each clip"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "default_behavior": "Same as kOfxImageEffectPropRegionOfInterest"
    },
    "kOfxImageEffectActionGetTimeDomain": {
        "value": "OfxImageEffectActionGetTimeDomain",
        "description": "Ask effect what range of frames it can produce (General context only).",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": ["kOfxImageEffectPropFrameRange"],
        "pre": ["kOfxActionCreateInstance has been called", "Effect is in General context"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "default_behavior": "Union of all non-optional input clip frame ranges, or infinite if none"
    },
    "kOfxImageEffectActionGetFramesNeeded": {
        "value": "OfxImageEffectActionGetFramesNeeded",
        "description": "What frames are needed from each input clip to process a given frame. Only called if kOfxImageEffectPropTemporalClipAccess is true.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropTime", "kOfxImageEffectPropThumbnailRender (optional)"],
        "outArgs": ["OfxImageClipPropFrameRange_<ClipName> for each clip"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "default_behavior": "Single frame at kOfxPropTime"
    },
    "kOfxImageEffectActionGetClipPreferences": {
        "value": "OfxImageEffectActionGetClipPreferences",
        "description": "Dynamically specify preferences for input/output clips (pixel depth, components, frame rate, etc.).",
        "handle": "OfxImageEffectHandle",
        "inArgs": "NULL",
        "outArgs": [
            "OfxImageClipPropComponents_<ClipName>",
            "OfxImageClipPropDepth_<ClipName>",
            "OfxImageClipPropPAR_<ClipName>",
            "kOfxImageEffectPropFrameRate",
            "kOfxImageClipPropFieldOrder",
            "kOfxImageEffectPropPreMultiplication",
            "kOfxImageClipPropContinuousSamples",
            "kOfxImageEffectFrameVarying"
        ],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectActionIsIdentity": {
        "value": "OfxImageEffectActionIsIdentity",
        "description": "Check if effect can pass through input unchanged (optimization). Return clip name and time to use instead.",
        "handle": "OfxImageEffectHandle",
        "inArgs": ["kOfxPropTime", "kOfxImageEffectPropFieldToRender", "kOfxImageEffectPropRenderWindow", "kOfxImageEffectPropRenderScale", "kOfxImageEffectPropThumbnailRender (optional)"],
        "outArgs": ["kOfxPropName (clip to use)", "kOfxPropTime (time to use from that clip)"],
        "returns": ["kOfxStatOK (is identity)", "kOfxStatReplyDefault (not identity, render)", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectActionRender": {
        "value": "OfxImageEffectActionRender",
        "description": "Process pixels - turn input clips and parameters into output image. MUST be trapped.",
        "handle": "OfxImageEffectHandle",
        "inArgs": [
            "kOfxPropTime",
            "kOfxImageEffectPropFieldToRender",
            "kOfxImageEffectPropRenderWindow",
            "kOfxImageEffectPropRenderScale",
            "kOfxImageEffectPropSequentialRenderStatus",
            "kOfxImageEffectPropInteractiveRenderStatus",
            "kOfxImageEffectPropRenderQualityDraft",
            "kOfxImageEffectPropNoSpatialAwareness",
            "kOfxImageEffectPropThumbnailRender (optional)"
        ],
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called", "kOfxImageEffectActionBeginSequenceRender has been called"],
        "post": ["kOfxImageEffectActionEndSequenceRender will be called"],
        "returns": ["kOfxStatOK", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h",
        "required": True
    },
    "kOfxImageEffectActionBeginSequenceRender": {
        "value": "OfxImageEffectActionBeginSequenceRender",
        "description": "Called before rendering a range of frames. Set up for long sequence.",
        "handle": "OfxImageEffectHandle",
        "inArgs": [
            "kOfxImageEffectPropFrameRange",
            "kOfxImageEffectPropFrameStep",
            "kOfxPropIsInteractive",
            "kOfxImageEffectPropRenderScale",
            "kOfxImageEffectPropSequentialRenderStatus",
            "kOfxImageEffectPropInteractiveRenderStatus",
            "kOfxImageEffectPropThumbnailRender (optional)"
        ],
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called"],
        "post": ["kOfxImageEffectActionRender will be called at least once", "kOfxImageEffectActionEndSequenceRender will be called"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectActionEndSequenceRender": {
        "value": "OfxImageEffectActionEndSequenceRender",
        "description": "Called after rendering a range of frames. Free resources.",
        "handle": "OfxImageEffectHandle",
        "inArgs": [
            "kOfxImageEffectPropFrameRange",
            "kOfxImageEffectPropFrameStep",
            "kOfxPropIsInteractive",
            "kOfxImageEffectPropRenderScale",
            "kOfxImageEffectPropSequentialRenderStatus",
            "kOfxImageEffectPropInteractiveRenderStatus",
            "kOfxImageEffectPropThumbnailRender (optional)"
        ],
        "outArgs": "NULL",
        "pre": ["kOfxActionCreateInstance has been called", "kOfxImageEffectActionBeginSequenceRender was called", "kOfxImageEffectActionRender was called at least once"],
        "returns": ["kOfxStatOK", "kOfxStatReplyDefault", "kOfxStatErrMemory", "kOfxStatFailed", "kOfxStatErrFatal"],
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# CONTEXTS (ofxImageEffect.h)
# =============================================================================

CONTEXTS = {
    "kOfxImageEffectContextGenerator": {
        "value": "OfxImageEffectContextGenerator",
        "description": "Creates images without input (e.g., noise generator, text, solid color)",
        "required_clips": ["Output"],
        "optional_clips": [],
        "typical_uses": ["Noise generators", "Text effects", "Solid colors", "Gradients"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectContextFilter": {
        "value": "OfxImageEffectContextFilter",
        "description": "Processes a single source image (e.g., blur, color correction)",
        "required_clips": ["Source", "Output"],
        "optional_clips": ["Mask (optional)"],
        "typical_uses": ["Blur", "Sharpen", "Color correction", "Distortion"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectContextTransition": {
        "value": "OfxImageEffectContextTransition",
        "description": "Blends between two source images with a transition parameter",
        "required_clips": ["SourceFrom", "SourceTo", "Output"],
        "required_params": ["Transition (0.0-1.0)"],
        "typical_uses": ["Dissolve", "Wipe", "Slide transitions"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectContextPaint": {
        "value": "OfxImageEffectContextPaint",
        "description": "Painting/drawing effects with brush input",
        "required_clips": ["Source", "Output"],
        "optional_clips": ["Brush"],
        "typical_uses": ["Clone brush", "Painting effects"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectContextGeneral": {
        "value": "OfxImageEffectContextGeneral",
        "description": "Flexible multi-input effects with arbitrary clip configuration",
        "required_clips": ["Output"],
        "optional_clips": ["Any number of custom inputs"],
        "typical_uses": ["Compositing", "Multi-input operations", "Complex effects"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectContextRetimer": {
        "value": "OfxImageEffectContextRetimer",
        "description": "Time remapping effects with SourceTime parameter",
        "required_clips": ["Source", "Output"],
        "required_params": ["SourceTime (double)"],
        "typical_uses": ["Speed changes", "Time warping", "Frame blending"],
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# PARAMETER TYPES (ofxParam.h)
# =============================================================================

PARAM_TYPES = {
    "kOfxParamTypeInteger": {
        "value": "OfxParamTypeInteger",
        "description": "Single valued integer parameter",
        "dimensions": 1,
        "c_type": "int",
        "default_property": "kOfxParamPropDefault (int)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeDouble": {
        "value": "OfxParamTypeDouble",
        "description": "Single valued floating point parameter",
        "dimensions": 1,
        "c_type": "double",
        "default_property": "kOfxParamPropDefault (double)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeBoolean": {
        "value": "OfxParamTypeBoolean",
        "description": "Single valued boolean parameter",
        "dimensions": 1,
        "c_type": "int",
        "default_property": "kOfxParamPropDefault (int 0 or 1)",
        "supports_animation": "Host dependent (kOfxParamHostPropSupportsBooleanAnimation)",
        "header": "ofxParam.h"
    },
    "kOfxParamTypeChoice": {
        "value": "OfxParamTypeChoice",
        "description": "Single valued, 'one-of-many' dropdown parameter",
        "dimensions": 1,
        "c_type": "int",
        "default_property": "kOfxParamPropDefault (int)",
        "related_properties": ["kOfxParamPropChoiceOption", "kOfxParamPropChoiceOrder"],
        "supports_animation": "Host dependent (kOfxParamHostPropSupportsChoiceAnimation)",
        "header": "ofxParam.h"
    },
    "kOfxParamTypeStrChoice": {
        "value": "OfxParamTypeStrChoice",
        "description": "String-valued 'one-of-many' parameter (OFX 1.5+)",
        "dimensions": 1,
        "c_type": "char*",
        "default_property": "kOfxParamPropDefault (string)",
        "related_properties": ["kOfxParamPropChoiceOption", "kOfxParamPropChoiceEnum"],
        "supports_animation": "Host dependent (kOfxParamHostPropSupportsStrChoiceAnimation)",
        "version": "1.5",
        "header": "ofxParam.h"
    },
    "kOfxParamTypeRGBA": {
        "value": "OfxParamTypeRGBA",
        "description": "Red, Green, Blue and Alpha color parameter",
        "dimensions": 4,
        "c_type": "double",
        "default_property": "kOfxParamPropDefault (double x 4)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeRGB": {
        "value": "OfxParamTypeRGB",
        "description": "Red, Green and Blue color parameter",
        "dimensions": 3,
        "c_type": "double",
        "default_property": "kOfxParamPropDefault (double x 3)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeDouble2D": {
        "value": "OfxParamTypeDouble2D",
        "description": "Two dimensional floating point parameter",
        "dimensions": 2,
        "c_type": "double",
        "default_property": "kOfxParamPropDefault (double x 2)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeInteger2D": {
        "value": "OfxParamTypeInteger2D",
        "description": "Two dimensional integer point parameter",
        "dimensions": 2,
        "c_type": "int",
        "default_property": "kOfxParamPropDefault (int x 2)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeDouble3D": {
        "value": "OfxParamTypeDouble3D",
        "description": "Three dimensional floating point parameter",
        "dimensions": 3,
        "c_type": "double",
        "default_property": "kOfxParamPropDefault (double x 3)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeInteger3D": {
        "value": "OfxParamTypeInteger3D",
        "description": "Three dimensional integer parameter",
        "dimensions": 3,
        "c_type": "int",
        "default_property": "kOfxParamPropDefault (int x 3)",
        "supports_animation": True,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeString": {
        "value": "OfxParamTypeString",
        "description": "UTF8 string parameter",
        "dimensions": 1,
        "c_type": "char*",
        "default_property": "kOfxParamPropDefault (string)",
        "related_properties": ["kOfxParamPropStringMode", "kOfxParamPropStringFilePathExists"],
        "supports_animation": "Host dependent (kOfxParamHostPropSupportsStringAnimation)",
        "header": "ofxParam.h"
    },
    "kOfxParamTypeCustom": {
        "value": "OfxParamTypeCustom",
        "description": "Plug-in defined parameter with custom serialization",
        "dimensions": 1,
        "c_type": "char* (encoded)",
        "default_property": "kOfxParamPropDefault (string)",
        "related_properties": ["kOfxParamPropCustomInterpCallbackV1"],
        "supports_animation": "Host dependent (kOfxParamHostPropSupportsCustomAnimation)",
        "header": "ofxParam.h"
    },
    "kOfxParamTypeBytes": {
        "value": "OfxParamTypeBytes",
        "description": "Plug-in defined opaque binary data parameter",
        "dimensions": 1,
        "c_type": "OfxBytes*",
        "default_property": "kOfxParamPropDefault (pointer to OfxBytes or NULL)",
        "supports_animation": False,
        "header": "ofxParam.h"
    },
    "kOfxParamTypeGroup": {
        "value": "OfxParamTypeGroup",
        "description": "Grouping parameter for hierarchy - contains no value",
        "dimensions": 0,
        "c_type": None,
        "related_properties": ["kOfxParamPropGroupOpen"],
        "supports_animation": False,
        "header": "ofxParam.h"
    },
    "kOfxParamTypePage": {
        "value": "OfxParamTypePage",
        "description": "Page parameter for UI layout organization - contains no value",
        "dimensions": 0,
        "c_type": None,
        "related_properties": ["kOfxParamPropPageChild"],
        "supports_animation": False,
        "header": "ofxParam.h"
    },
    "kOfxParamTypePushButton": {
        "value": "OfxParamTypePushButton",
        "description": "Push button parameter for triggering actions - contains no value",
        "dimensions": 0,
        "c_type": None,
        "supports_animation": False,
        "header": "ofxParam.h"
    },
}

# =============================================================================
# BIT DEPTHS (ofxCore.h)
# =============================================================================

BIT_DEPTHS = {
    "kOfxBitDepthNone": {
        "value": "OfxBitDepthNone",
        "description": "No bit depth / unconnected clip",
        "bytes_per_component": 0,
        "header": "ofxCore.h"
    },
    "kOfxBitDepthByte": {
        "value": "OfxBitDepthByte",
        "description": "Unsigned 8-bit integer samples (0-255)",
        "bytes_per_component": 1,
        "c_type": "unsigned char",
        "header": "ofxCore.h"
    },
    "kOfxBitDepthShort": {
        "value": "OfxBitDepthShort",
        "description": "Unsigned 16-bit integer samples (0-65535)",
        "bytes_per_component": 2,
        "c_type": "unsigned short",
        "header": "ofxCore.h"
    },
    "kOfxBitDepthHalf": {
        "value": "OfxBitDepthHalf",
        "description": "16-bit floating point samples (IEEE 754 half precision)",
        "bytes_per_component": 2,
        "c_type": "half (fp16)",
        "version": "1.4",
        "header": "ofxCore.h"
    },
    "kOfxBitDepthFloat": {
        "value": "OfxBitDepthFloat",
        "description": "32-bit floating point samples (IEEE 754 single precision)",
        "bytes_per_component": 4,
        "c_type": "float",
        "header": "ofxCore.h"
    },
}

# =============================================================================
# IMAGE COMPONENTS (ofxImageEffect.h)
# =============================================================================

IMAGE_COMPONENTS = {
    "kOfxImageComponentNone": {
        "value": "OfxImageComponentNone",
        "description": "Unset/unconnected image components",
        "num_components": 0,
        "header": "ofxImageEffect.h"
    },
    "kOfxImageComponentRGBA": {
        "value": "OfxImageComponentRGBA",
        "description": "Red, Green, Blue, Alpha components",
        "num_components": 4,
        "channel_order": ["R", "G", "B", "A"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageComponentRGB": {
        "value": "OfxImageComponentRGB",
        "description": "Red, Green, Blue components (no alpha)",
        "num_components": 3,
        "channel_order": ["R", "G", "B"],
        "header": "ofxImageEffect.h"
    },
    "kOfxImageComponentAlpha": {
        "value": "OfxImageComponentAlpha",
        "description": "Single Alpha channel only",
        "num_components": 1,
        "channel_order": ["A"],
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# FIELD HANDLING (ofxImageEffect.h)
# =============================================================================

FIELD_TYPES = {
    "kOfxImageFieldNone": {
        "value": "OfxFieldNone",
        "description": "Unfielded full frame image",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageFieldLower": {
        "value": "OfxFieldLower",
        "description": "Lower field (scan lines 0, 2, 4...)",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageFieldUpper": {
        "value": "OfxFieldUpper",
        "description": "Upper field (scan lines 1, 3, 5...)",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageFieldBoth": {
        "value": "OfxFieldBoth",
        "description": "Both fields interlaced",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageFieldSingle": {
        "value": "OfxFieldSingle",
        "description": "Single field, half height image",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageFieldDoubled": {
        "value": "OfxFieldDoubled",
        "description": "Single field, each scan line doubled to full height",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# PREMULTIPLICATION STATES (ofxImageEffect.h)
# =============================================================================

PREMULT_STATES = {
    "kOfxImageOpaque": {
        "value": "OfxImageOpaque",
        "description": "Image is opaque, has no premultiplication state",
        "header": "ofxImageEffect.h"
    },
    "kOfxImagePreMultiplied": {
        "value": "OfxImageAlphaPremultiplied",
        "description": "Image is premultiplied by its alpha",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageUnPreMultiplied": {
        "value": "OfxImageAlphaUnPremultiplied",
        "description": "Image is unpremultiplied (straight alpha)",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# THREAD SAFETY LEVELS (ofxImageEffect.h)
# =============================================================================

THREAD_SAFETY = {
    "kOfxImageEffectRenderUnsafe": {
        "value": "OfxImageEffectRenderUnsafe",
        "description": "Only a single render call can be made at any time among ALL instances",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectRenderInstanceSafe": {
        "value": "OfxImageEffectRenderInstanceSafe",
        "description": "Any instance can have a single render call at any one time",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectRenderFullySafe": {
        "value": "OfxImageEffectRenderFullySafe",
        "description": "Any instance can have multiple renders running simultaneously",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# CHANGE REASONS (ofxCore.h)
# =============================================================================

CHANGE_REASONS = {
    "kOfxChangeUserEdited": {
        "value": "OfxChangeUserEdited",
        "description": "User or host changed the instance (includes undo/redo, resets, file loading)",
        "header": "ofxCore.h"
    },
    "kOfxChangePluginEdited": {
        "value": "OfxChangePluginEdited",
        "description": "The plugin itself changed the value in some action",
        "header": "ofxCore.h"
    },
    "kOfxChangeTime": {
        "value": "OfxChangeTime",
        "description": "Time changed and affected the object because it varies over time",
        "header": "ofxCore.h"
    },
}

# =============================================================================
# SUITES (multiple headers)
# =============================================================================

SUITES = {
    "kOfxPropertySuite": {
        "value": "OfxPropertySuite",
        "version": 1,
        "struct": "OfxPropertySuiteV1",
        "description": "Suite for manipulating generic properties on OFX objects",
        "functions": [
            {"name": "propSetPointer", "description": "Set a single pointer value at index"},
            {"name": "propSetString", "description": "Set a single string value at index"},
            {"name": "propSetDouble", "description": "Set a single double value at index"},
            {"name": "propSetInt", "description": "Set a single int value at index"},
            {"name": "propSetPointerN", "description": "Set multiple pointer values"},
            {"name": "propSetStringN", "description": "Set multiple string values"},
            {"name": "propSetDoubleN", "description": "Set multiple double values"},
            {"name": "propSetIntN", "description": "Set multiple int values"},
            {"name": "propGetPointer", "description": "Get a single pointer value"},
            {"name": "propGetString", "description": "Get a single string value"},
            {"name": "propGetDouble", "description": "Get a single double value"},
            {"name": "propGetInt", "description": "Get a single int value"},
            {"name": "propGetPointerN", "description": "Get multiple pointer values"},
            {"name": "propGetStringN", "description": "Get multiple string values"},
            {"name": "propGetDoubleN", "description": "Get multiple double values"},
            {"name": "propGetIntN", "description": "Get multiple int values"},
            {"name": "propReset", "description": "Reset property to default value"},
            {"name": "propGetDimension", "description": "Get number of dimensions in property"},
        ],
        "header": "ofxProperty.h"
    },
    "kOfxImageEffectSuite": {
        "value": "OfxImageEffectSuite",
        "version": 1,
        "struct": "OfxImageEffectSuiteV1",
        "description": "Suite for image effect operations",
        "functions": [
            {"name": "getPropertySet", "description": "Get property set for image effect"},
            {"name": "getParamSet", "description": "Get parameter set for image effect"},
            {"name": "clipDefine", "description": "Define a clip in describe action"},
            {"name": "clipGetHandle", "description": "Get handle for named clip instance"},
            {"name": "clipGetPropertySet", "description": "Get property set for clip"},
            {"name": "clipGetImage", "description": "Fetch image from clip at time/region"},
            {"name": "clipReleaseImage", "description": "Release image handle"},
            {"name": "clipGetRegionOfDefinition", "description": "Get clip's RoD at time"},
            {"name": "abort", "description": "Check if processing should abort"},
            {"name": "imageMemoryAlloc", "description": "Allocate image memory from host pool"},
            {"name": "imageMemoryFree", "description": "Free allocated image memory"},
            {"name": "imageMemoryLock", "description": "Lock memory and get pointer"},
            {"name": "imageMemoryUnlock", "description": "Unlock memory"},
        ],
        "header": "ofxImageEffect.h"
    },
    "kOfxParameterSuite": {
        "value": "OfxParameterSuite",
        "version": 1,
        "struct": "OfxParameterSuiteV1",
        "description": "Suite for defining and manipulating parameters",
        "functions": [
            {"name": "paramDefine", "description": "Define a new parameter in describe action"},
            {"name": "paramGetHandle", "description": "Get handle for parameter instance"},
            {"name": "paramSetGetPropertySet", "description": "Get property set for param set"},
            {"name": "paramGetPropertySet", "description": "Get property set for parameter"},
            {"name": "paramGetValue", "description": "Get current parameter value"},
            {"name": "paramGetValueAtTime", "description": "Get parameter value at specific time"},
            {"name": "paramGetDerivative", "description": "Get parameter derivative at time"},
            {"name": "paramGetIntegral", "description": "Get parameter integral over time range"},
            {"name": "paramSetValue", "description": "Set current parameter value"},
            {"name": "paramSetValueAtTime", "description": "Set keyframe at specific time"},
            {"name": "paramGetNumKeys", "description": "Get number of keyframes"},
            {"name": "paramGetKeyTime", "description": "Get time of nth keyframe"},
            {"name": "paramGetKeyIndex", "description": "Find keyframe index at/before/after time"},
            {"name": "paramDeleteKey", "description": "Delete keyframe at time"},
            {"name": "paramDeleteAllKeys", "description": "Delete all keyframes"},
            {"name": "paramCopy", "description": "Copy parameter value/animation"},
            {"name": "paramEditBegin", "description": "Begin undo/redo group"},
            {"name": "paramEditEnd", "description": "End undo/redo group"},
        ],
        "header": "ofxParam.h"
    },
    "kOfxMemorySuite": {
        "value": "OfxMemorySuite",
        "version": 1,
        "struct": "OfxMemorySuiteV1",
        "description": "General purpose memory management",
        "functions": [
            {"name": "memoryAlloc", "description": "Allocate memory through host"},
            {"name": "memoryFree", "description": "Free allocated memory"},
        ],
        "header": "ofxMemory.h"
    },
    "kOfxMultiThreadSuite": {
        "value": "OfxMultiThreadSuite",
        "version": 1,
        "struct": "OfxMultiThreadSuiteV1",
        "description": "Multi-threading and mutex operations",
        "functions": [
            {"name": "multiThread", "description": "Spawn parallel threads"},
            {"name": "multiThreadNumCPUs", "description": "Get number of CPUs"},
            {"name": "multiThreadIndex", "description": "Get current thread index"},
            {"name": "multiThreadIsSpawnedThread", "description": "Check if in spawned thread"},
            {"name": "mutexCreate", "description": "Create a mutex"},
            {"name": "mutexDestroy", "description": "Destroy a mutex"},
            {"name": "mutexLock", "description": "Lock a mutex (blocking)"},
            {"name": "mutexTryLock", "description": "Try to lock mutex (non-blocking)"},
            {"name": "mutexUnlock", "description": "Unlock a mutex"},
        ],
        "header": "ofxMultiThread.h"
    },
    "kOfxMessageSuite": {
        "value": "OfxMessageSuite",
        "version": 2,
        "struct": "OfxMessageSuiteV2",
        "description": "User messaging and error reporting",
        "functions": [
            {"name": "message", "description": "Post transient message to user"},
            {"name": "setPersistentMessage", "description": "Set persistent error/warning message"},
            {"name": "clearPersistentMessage", "description": "Clear persistent message"},
        ],
        "message_types": ["kOfxMessageFatal", "kOfxMessageError", "kOfxMessageWarning", "kOfxMessageMessage", "kOfxMessageLog", "kOfxMessageQuestion"],
        "header": "ofxMessage.h"
    },
    "kOfxInteractSuite": {
        "value": "OfxInteractSuite",
        "version": 1,
        "struct": "OfxInteractSuiteV1",
        "description": "Custom overlay GUI interaction",
        "functions": [
            {"name": "interactSwapBuffers", "description": "Swap OpenGL buffers"},
            {"name": "interactRedraw", "description": "Request redraw"},
            {"name": "interactGetPropertySet", "description": "Get interact property set"},
        ],
        "header": "ofxInteract.h"
    },
    "kOfxDrawSuite": {
        "value": "OfxDrawSuite",
        "version": 1,
        "struct": "OfxDrawSuiteV1",
        "description": "Host-native overlay drawing (alternative to OpenGL)",
        "functions": [
            {"name": "getColour", "description": "Get host standard color"},
            {"name": "setColour", "description": "Set drawing color"},
            {"name": "setLineWidth", "description": "Set line width"},
            {"name": "setLineStipple", "description": "Set line stipple pattern"},
            {"name": "draw", "description": "Draw geometric primitive"},
            {"name": "drawText", "description": "Draw UTF-8 text"},
        ],
        "header": "ofxDrawSuite.h"
    },
}

# =============================================================================
# STANDARD CLIP NAMES (ofxImageEffect.h)
# =============================================================================

STANDARD_CLIPS = {
    "kOfxImageEffectOutputClipName": {
        "value": "Output",
        "description": "Standard name for output clip",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectSimpleSourceClipName": {
        "value": "Source",
        "description": "Standard name for single source input clip",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectTransitionSourceFromClipName": {
        "value": "SourceFrom",
        "description": "Name of 'from' clip in transition context",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectTransitionSourceToClipName": {
        "value": "SourceTo",
        "description": "Name of 'to' clip in transition context",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# STANDARD PARAMETER NAMES (ofxImageEffect.h)
# =============================================================================

STANDARD_PARAMS = {
    "kOfxImageEffectTransitionParamName": {
        "value": "Transition",
        "description": "Mandated transition parameter for transition context (0.0-1.0)",
        "header": "ofxImageEffect.h"
    },
    "kOfxImageEffectRetimerParamName": {
        "value": "SourceTime",
        "description": "Mandated SourceTime parameter for retimer context",
        "header": "ofxImageEffect.h"
    },
}

# =============================================================================
# GPU RENDERING PROPERTIES (ofxGPURender.h)
# =============================================================================

GPU_PROPERTIES = {
    # CUDA
    "kOfxImageEffectPropCudaRenderSupported": {
        "type": "string",
        "description": "Indicates host/plugin CUDA support",
        "values": ["false", "true"],
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropCudaEnabled": {
        "type": "int",
        "description": "Set to 1 when images are CUDA memory pointers",
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropCudaStream": {
        "type": "pointer",
        "description": "Pointer to cudaStream_t for async operations",
        "header": "ofxGPURender.h"
    },
    # Metal
    "kOfxImageEffectPropMetalRenderSupported": {
        "type": "string",
        "description": "Indicates host/plugin Metal support",
        "values": ["false", "true"],
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropMetalEnabled": {
        "type": "int",
        "description": "Set to 1 when images are Metal id<MTLBuffer>",
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropMetalCommandQueue": {
        "type": "pointer",
        "description": "Pointer to id<MTLCommandQueue>",
        "header": "ofxGPURender.h"
    },
    # OpenCL
    "kOfxImageEffectPropOpenCLRenderSupported": {
        "type": "string",
        "description": "Indicates OpenCL buffer support",
        "values": ["false", "true"],
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropOpenCLEnabled": {
        "type": "int",
        "description": "Set to 1 when using OpenCL",
        "header": "ofxGPURender.h"
    },
    "kOfxImageEffectPropOpenCLCommandQueue": {
        "type": "pointer",
        "description": "Pointer to cl_command_queue",
        "header": "ofxGPURender.h"
    },
}

# =============================================================================
# TYPE IDENTIFIERS (ofxCore.h, ofxImageEffect.h)
# =============================================================================

TYPE_IDENTIFIERS = {
    "kOfxTypeImageEffectHost": {
        "value": "OfxTypeImageEffectHost",
        "description": "Type identifier for image effect host handles",
        "header": "ofxImageEffect.h"
    },
    "kOfxTypeImageEffect": {
        "value": "OfxTypeImageEffect",
        "description": "Type identifier for image effect plugin handles",
        "header": "ofxImageEffect.h"
    },
    "kOfxTypeImageEffectInstance": {
        "value": "OfxTypeImageEffectInstance",
        "description": "Type identifier for image effect instance handles",
        "header": "ofxImageEffect.h"
    },
    "kOfxTypeClip": {
        "value": "OfxTypeClip",
        "description": "Type identifier for clip handles",
        "header": "ofxImageEffect.h"
    },
    "kOfxTypeImage": {
        "value": "OfxTypeImage",
        "description": "Type identifier for image handles",
        "header": "ofxImageEffect.h"
    },
    "kOfxTypeParameter": {
        "value": "OfxTypeParameter",
        "description": "Type identifier for parameter descriptor handles",
        "header": "ofxParam.h"
    },
    "kOfxTypeParameterInstance": {
        "value": "OfxTypeParameterInstance",
        "description": "Type identifier for parameter instance handles",
        "header": "ofxParam.h"
    },
}

# =============================================================================
# DATA STRUCTURES (ofxCore.h)
# =============================================================================

DATA_STRUCTURES = {
    "OfxHost": {
        "description": "Host structure passed to plugin's setHost function",
        "fields": [
            {"name": "host", "type": "OfxPropertySetHandle", "description": "Global handle to host properties"},
            {"name": "fetchSuite", "type": "function pointer", "description": "Function to fetch suites from host"},
        ],
        "header": "ofxCore.h"
    },
    "OfxPlugin": {
        "description": "Structure that defines a plug-in to a host",
        "fields": [
            {"name": "pluginApi", "type": "const char*", "description": "Plugin API type (e.g., 'OfxImageEffectPluginAPI')"},
            {"name": "apiVersion", "type": "int", "description": "Version of the plugin API"},
            {"name": "pluginIdentifier", "type": "const char*", "description": "Unique identifier (e.g., 'com.company.plugin')"},
            {"name": "pluginVersionMajor", "type": "unsigned int", "description": "Major version number"},
            {"name": "pluginVersionMinor", "type": "unsigned int", "description": "Minor version number"},
            {"name": "setHost", "type": "function pointer", "description": "Called first to set host connection"},
            {"name": "mainEntry", "type": "OfxPluginEntryPoint*", "description": "Main entry point for actions"},
        ],
        "header": "ofxCore.h"
    },
    "OfxRangeI": {
        "description": "One dimensional integer bounds",
        "fields": [
            {"name": "min", "type": "int", "description": "Minimum value"},
            {"name": "max", "type": "int", "description": "Maximum value"},
        ],
        "header": "ofxCore.h"
    },
    "OfxRangeD": {
        "description": "One dimensional double bounds",
        "fields": [
            {"name": "min", "type": "double", "description": "Minimum value"},
            {"name": "max", "type": "double", "description": "Maximum value"},
        ],
        "header": "ofxCore.h"
    },
    "OfxPointI": {
        "description": "Two dimensional integer point",
        "fields": [
            {"name": "x", "type": "int", "description": "X coordinate"},
            {"name": "y", "type": "int", "description": "Y coordinate"},
        ],
        "header": "ofxCore.h"
    },
    "OfxPointD": {
        "description": "Two dimensional double point",
        "fields": [
            {"name": "x", "type": "double", "description": "X coordinate"},
            {"name": "y", "type": "double", "description": "Y coordinate"},
        ],
        "header": "ofxCore.h"
    },
    "OfxRectI": {
        "description": "Two dimensional integer region (x1 <= x < x2)",
        "fields": [
            {"name": "x1", "type": "int", "description": "Left edge"},
            {"name": "y1", "type": "int", "description": "Bottom edge"},
            {"name": "x2", "type": "int", "description": "Right edge"},
            {"name": "y2", "type": "int", "description": "Top edge"},
        ],
        "header": "ofxCore.h"
    },
    "OfxRectD": {
        "description": "Two dimensional double region (x1 <= x < x2)",
        "fields": [
            {"name": "x1", "type": "double", "description": "Left edge"},
            {"name": "y1", "type": "double", "description": "Bottom edge"},
            {"name": "x2", "type": "double", "description": "Right edge"},
            {"name": "y2", "type": "double", "description": "Top edge"},
        ],
        "header": "ofxCore.h"
    },
    "OfxBytes": {
        "description": "Structure for kOfxParamTypeBytes parameter data",
        "fields": [
            {"name": "data", "type": "const unsigned char*", "description": "Pointer to data buffer"},
            {"name": "length", "type": "size_t", "description": "Length of data buffer in bytes"},
        ],
        "header": "ofxParam.h"
    },
}

# =============================================================================
# EXPORTED FUNCTIONS (ofxCore.h)
# =============================================================================

EXPORTED_FUNCTIONS = {
    "OfxGetPlugin": {
        "signature": "OfxPlugin* OfxGetPlugin(int nth)",
        "description": "Returns the nth plugin implemented inside a binary",
        "header": "ofxCore.h",
        "required": True
    },
    "OfxGetNumberOfPlugins": {
        "signature": "int OfxGetNumberOfPlugins(void)",
        "description": "Returns the number of plugins implemented inside a binary",
        "header": "ofxCore.h",
        "required": True
    },
    "OfxSetHost": {
        "signature": "OfxStatus OfxSetHost(const OfxHost *host)",
        "description": "First function host should call (added 2020). Plugin can return kOfxStatFailed to be skipped.",
        "header": "ofxCore.h",
        "required": False,
        "version": "2020"
    },
}

# =============================================================================
# HOST COMPATIBILITY (known quirks)
# =============================================================================

HOST_COMPATIBILITY = {
    "DaVinci Resolve": {
        "supports_ofx_version": "1.4",
        "known_limitations": [
            "No parametric parameters (kOfxParamTypeParametric)",
            "No kOfxParamPropDefaultCoordinateSystem support",
            "Some interface functions have limited support",
            "Specific clip naming conventions",
        ],
        "gpu_support": ["CUDA", "Metal", "OpenCL"],
        "notes": "Always test specifically in Resolve - has quirks vs Nuke"
    },
    "Nuke": {
        "supports_ofx_version": "1.4",
        "notes": "Generally considered the reference OFX implementation",
        "gpu_support": ["CUDA", "OpenCL"],
    },
    "Fusion": {
        "supports_ofx_version": "1.4",
        "gpu_support": ["CUDA", "OpenCL"],
    },
    "Vegas Pro": {
        "supports_ofx_version": "1.4",
    },
}
