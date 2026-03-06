# ShaderNodeDisplacement

## Conversion Type: 4 (No Conversion - Requires Manual Setup)

## Overview
- **Blender Node**: ShaderNodeDisplacement
- **Category**: Vector
- **Compatibility**: 0%

## Unity Equivalent
- **Primary**: Vertex Displacement (not in standard ShaderGraph)
- **Implementation**: Requires custom shader or geometry shader

## Conversion Process

### Step 1: Not Directly Convertible
- **Description**: Displacement requires mesh modification
- **Blender**: Modifies mesh geometry in rendering
- **Unity**: Cannot displace vertices in standard ShaderGraph

## Visual Graph Layout

```
// NOT POSSIBLE - Displacement requires:
// 1. Custom geometry shader
// 2. Compute shader for vertex displacement
// 3. Or use Unity's terrain/hair displacement systems

// Workaround: Use normal map instead
[Height Map] ──> [Normal From Height] ──> [Normal Input]
```

## Pseudocode for Conversion Logic

```python
def convert_displacement_node(blender_node):
    """
    Converts Blender ShaderNodeDisplacement - NOT POSSIBLE.
    This node modifies actual mesh geometry, which cannot be done in standard ShaderGraph.
    """
    # 1. Log critical warning
    log_error(
        "Displacement node cannot be converted to Unity ShaderGraph. "
        "Displacement requires mesh geometry modification which is not supported. "
        "Consider using:\n"
        "1. Normal map instead of displacement\n"
        "2. Custom geometry shader\n"
        "3. Unity's terrain system"
    )
    
    # 2. Try to convert to normal map as alternative
    height_input = get_input_connection(blender_node.inputs["Height"])
    if height_input:
        # Convert height to normal as workaround
        normal_from_height = create_shadergraph_node("Normal From Height")
        
        if height_input:
            connect_nodes(height_input, normal_from_height, "In")
        
        log_warning("Converting displacement to normal map as alternative")
        return normal_from_height.outputs["Normal"]
    
    return None
```

## Compatibility Notes
- 0% compatible
- Cannot displace mesh vertices in ShaderGraph

## Limitations
- True displacement requires geometry shader or compute shader
- Standard ShaderGraph cannot modify vertex positions
- Must use normal maps as visual alternative
