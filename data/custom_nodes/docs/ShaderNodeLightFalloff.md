# ShaderNodeLightFalloff

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeLightFalloff
- **Category**: Input
- **Compatibility**: 70%

## Unity Equivalent
- **Primary**: Distance-based attenuation (not directly available)
- **Implementation**: Custom function or approximation

## Conversion Process

### Step 1: Get Quadratic Falloff
- **Description**: Standard inverse square falloff
- **Blender Output**: Quadratic
- **Unity Output**: Custom calculation needed

### Step 2: Get Linear/Constant
- **Description**: Different falloff modes
- **Blender Output**: Linear, Constant
- **Unity Output**: Custom calculation

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Quadratic | 1 / Distance² | 70% |
| Linear | 1 / Distance | 70% |
| Constant | 1.0 | 80% |

## Visual Graph Layout

```
// Quadratic Falloff approximation
[Position] ──> [Distance] ──> [Multiply] ──> [Power: 2] ──> [One Minus] ──> [Output]
                                              ^              ^
                                              │              │
                                      [Float: 1.0] ───────┘
```

## Pseudocode for Conversion Logic

```python
def convert_lightfalloff_node(blender_node):
    """
    Converts Blender ShaderNodeLightFalloff to Unity ShaderGraph.
    Near conversion - requires distance-based attenuation math.
    """
    # Get falloff type
    # Blender: 'QUADRATIC', 'LINEAR', 'CONSTANT'
    falloff_type = blender_node.falloff
    
    # Get light position - not directly available in Unity shader
    # This would need to be passed as a property or calculated differently
    
    outputs = {}
    
    if falloff_type == 'QUADRATIC':
        # 1 / distance² approximation
        # Note: Can't get light position in standard shader
        
        log_warning(
            "LightFalloff: Quadratic falloff requires light position. "
            "Using approximation with shader properties."
        )
        
        # Create as custom property that can be set from script
        quadratic = create_shadergraph_node("Property", {
            "name": "LightFalloff_Quadratic",
            "type": "Float",
            "default": 1.0
        })
        outputs["Quadratic"] = quadratic.outputs["Out"]
    
    elif falloff_type == 'LINEAR':
        # 1 / distance approximation
        linear = create_shadergraph_node("Property", {
            "name": "LightFalloff_Linear",
            "type": "Float", 
            "default": 1.0
        })
        outputs["Linear"] = linear.outputs["Out"]
    
    else:  # CONSTANT
        # Always 1.0 - direct value
        constant = create_shadergraph_node("Float", {"value": 1.0})
        outputs["Constant"] = constant.outputs["Out"]
    
    return outputs
```

## Compatibility Notes
- 70% compatible
- Light position not available in standard shaders
- Need custom implementation or script integration

## Limitations
- Cannot get light position in standard ShaderGraph
- Requires custom shader code or script-side handling
- Not a direct node-to-node conversion
