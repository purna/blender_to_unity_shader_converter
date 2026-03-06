# ShaderNodeSeparateRGB

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeSeparateRGB
- **Category**: Converter
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Split node

## Conversion Process

### Step 1: Split Color
- **Description**: Split RGBA color into R, G, B channels
- **Blender Input**: Color
- **Unity Output**: R, G, B float values

## Blender to Unity Mapping

| Blender Output | Unity Output | Compatibility |
|---------------|-------------|---------------|
| R | R | 100% |
| G | G | 100% |
| B | B | 100% |
| A | A | 100% |

## Visual Graph Layout

```
// Split RGB channels
[Color] ──> [Split] ──> [R] ──> [Float Output]
                    │
                    ├─> [G] ──> [Float Output]
                    │
                    └─> [B] ──> [Float Output]
```

## Pseudocode for Conversion Logic

```python
def convert_separate_rgb_node(blender_node):
    """
    Converts Blender ShaderNodeSeparateRGB to Unity ShaderGraph Split node.
    1-1 direct mapping - Split node extracts channels.
    """
    # 1. Create Split node
    split_node = create_shadergraph_node("Split")
    
    # 2. Get color input
    color_input = get_input_connection(blender_node.inputs["Image"])
    
    if color_input:
        connect_nodes(color_input, split_node, "In")
    else:
        # Use default color
        default_color = blender_node.inputs["Image"].default_value
        color_node = create_shadergraph_node("Color", {"value": default_color})
        connect_nodes(color_node, split_node, "In")
    
    # 3. Return dict of channel outputs
    return {
        "R": split_node.outputs["R"],
        "G": split_node.outputs["G"],
        "B": split_node.outputs["B"],
        "A": split_node.outputs["A"]
    }
```

## Compatibility Notes
- 100% compatible
- Direct mapping to Split node

## Limitations
- None
