# ShaderNodeLayerWeight

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeLayerWeight
- **Category**: Input
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Fresnel Effect node (similar to Facing output)
- **Alternative**: Custom function for all outputs

## Conversion Process

### Step 1: Get Fresnel Output
- **Description**: Fresnel based on view angle
- **Blender Output**: Facing (0-1)
- **Unity Output**: Fresnel

### Step 2: Get Weight Output
- **Description**: Fresnel with different exponent
- **Blender Output**: Weight (exponentiated)
- **Unity Output**: Custom calculation

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Facing | Fresnel Effect | 100% |
| Weight | Fresnel Effect + Power | 80% |

## Visual Graph Layout

```
// Layer Weight - Facing
[Normal] ──> [Fresnel Effect] ──> [Output: Facing]

// Layer Weight - Weight (with different exponent)
[Normal] ──> [Fresnel Effect] ──> [Power] ──> [Output]
              ^                                    ^
              │                                    │
[Float: 4.0] ─┴────────────────────────────────────┘
```

## Pseudocode for Conversion Logic

```python
def convert_layerweight_node(blender_node):
    """
    Converts Blender ShaderNodeLayerWeight to Unity ShaderGraph Fresnel.
    1-1 mapping - LayerWeight outputs map to Fresnel variants.
    """
    # Get inputs
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    blend_value = blender_node.inputs["Blend"].default_value
    
    outputs = {}
    
    # 1. Facing output - standard fresnel
    fresnel_facing = create_shadergraph_node("Fresnel Effect")
    
    if normal_input:
        connect_nodes(normal_input, fresnel_facing, "Normal")
    
    fresnel_facing.set_property("Power", 5.0)  # Default fresnel power
    outputs["Facing"] = fresnel_facing.outputs["Out"]
    
    # 2. Weight output - fresnel with different exponent (default 4.0 in Blender)
    fresnel_weight = create_shadergraph_node("Fresnel Effect")
    
    if normal_input:
        # Need to branch - connect to both fresnel nodes
        connect_nodes(normal_input, fresnel_weight, "Normal")
    
    fresnel_weight.set_property("Power", blend_value)  # Blend value affects this
    outputs["Weight"] = fresnel_weight.outputs["Out"]
    
    return outputs
```

## Compatibility Notes
- 100% compatible for Facing
- 80% for Weight - exponent handling differs

## Limitations
- Blend parameter affects weight calculation differently
- Exact fresnel curve may differ
