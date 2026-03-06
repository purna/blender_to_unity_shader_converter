# ShaderNodeCombineXYZ

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeCombineXYZ
- **Category**: Converter
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Combine node (Vector3)

## Conversion Process

### Step 1: Combine Components
- **Description**: Combine X, Y, Z floats into vector
- **Blender Input**: X, Y, Z floats
- **Unity Output**: XYZ Vector

## Blender to Unity Mapping

| Blender Input | Unity Input | Compatibility |
|--------------|-------------|---------------|
| X | R | 100% |
| Y | G | 100% |
| Z | B | 100% |

## Visual Graph Layout

```
// Combine XYZ components
[Float: X] ──┐
             ├─> [Combine] ──> [Vector3]
[Float: Y] ──┤
             │
[Float: Z] ──┘
```

## Pseudocode for Conversion Logic

```python
def convert_combine_xyz_node(blender_node):
    """
    Converts Blender ShaderNodeCombineXYZ to Unity ShaderGraph Combine node.
    1-1 direct mapping - Combine node joins XYZ components.
    """
    # 1. Create Combine node
    combine_node = create_shadergraph_node("Combine")
    
    # 2. Get component inputs
    x_input = get_input_connection(blender_node.inputs["X"])
    y_input = get_input_connection(blender_node.inputs["Y"])
    z_input = get_input_connection(blender_node.inputs["Z"])
    
    # 3. Connect X (maps to R)
    if x_input:
        connect_nodes(x_input, combine_node, "R")
    else:
        combine_node.set_input("R", blender_node.inputs["X"].default_value)
    
    # 4. Connect Y (maps to G)
    if y_input:
        connect_nodes(y_input, combine_node, "G")
    else:
        combine_node.set_input("G", blender_node.inputs["Y"].default_value)
    
    # 5. Connect Z (maps to B)
    if z_input:
        connect_nodes(z_input, combine_node, "B")
    else:
        combine_node.set_input("B", blender_node.inputs["Z"].default_value)
    
    return combine_node.outputs["RGBA"]  # In Unity, this is the Vector output
```

## Compatibility Notes
- 100% compatible
- Direct mapping to Combine node (X→R, Y→G, Z→B)

## Limitations
- None
