# ShaderNodeCombineRGB

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeCombineRGB
- **Category**: Converter
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Combine node

## Conversion Process

### Step 1: Combine Channels
- **Description**: Combine R, G, B floats into color
- **Blender Input**: R, G, B floats
- **Unity Output**: RGBA color

## Blender to Unity Mapping

| Blender Input | Unity Input | Compatibility |
|--------------|-------------|---------------|
| R | R | 100% |
| G | G | 100% |
| B | B | 100% |

## Visual Graph Layout

```
// Combine RGB channels
[Float: R] ──┐
             ├─> [Combine] ──> [Color]
[Float: G] ──┤
             │
[Float: B] ──┘
```

## Pseudocode for Conversion Logic

```python
def convert_combine_rgb_node(blender_node):
    """
    Converts Blender ShaderNodeCombineRGB to Unity ShaderGraph Combine node.
    1-1 direct mapping - Combine node joins channels.
    """
    # 1. Create Combine node
    combine_node = create_shadergraph_node("Combine")
    
    # 2. Get channel inputs
    r_input = get_input_connection(blender_node.inputs["R"])
    g_input = get_input_connection(blender_node.inputs["G"])
    b_input = get_input_connection(blender_node.inputs["B"])
    
    # 3. Connect R channel
    if r_input:
        connect_nodes(r_input, combine_node, "R")
    else:
        combine_node.set_input("R", blender_node.inputs["R"].default_value)
    
    # 4. Connect G channel
    if g_input:
        connect_nodes(g_input, combine_node, "G")
    else:
        combine_node.set_input("G", blender_node.inputs["G"].default_value)
    
    # 5. Connect B channel
    if b_input:
        connect_nodes(b_input, combine_node, "B")
    else:
        combine_node.set_input("B", blender_node.inputs["B"].default_value)
    
    # Set Alpha to 1.0 by default
    combine_node.set_input("A", 1.0)
    
    return combine_node.outputs["RGBA"]
```

## Compatibility Notes
- 100% compatible
- Direct mapping to Combine node

## Limitations
- None
