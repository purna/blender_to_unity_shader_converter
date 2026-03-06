# ShaderNodeSeparateXYZ

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeSeparateXYZ
- **Category**: Converter
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Split node

## Conversion Process

### Step 1: Split Vector
- **Description**: Split XYZ vector into X, Y, Z components
- **Blender Input**: Vector
- **Unity Output**: X, Y, Z float values

## Blender to Unity Mapping

| Blender Output | Unity Output | Compatibility |
|---------------|-------------|---------------|
| X | R | 100% |
| Y | G | 100% |
| Z | B | 100% |

## Visual Graph Layout

```
// Split XYZ vector
[> [Split]Vector] ── ──> [X/R] ──> [Float Output]
                    │
                    ├─> [Y/G] ──> [Float Output]
                    │
                    └─> [Z/B] ──> [Float Output]
```

## Pseudocode for Conversion Logic

```python
def convert_separate_xyz_node(blender_node):
    """
    Converts Blender ShaderNodeSeparateXYZ to Unity ShaderGraph Split node.
    1-1 direct mapping - Split node extracts XYZ components.
    """
    # 1. Create Split node
    split_node = create_shadergraph_node("Split")
    
    # 2. Get vector input
    vector_input = get_input_connection(blender_node.inputs["Vector"])
    
    if vector_input:
        connect_nodes(vector_input, split_node, "In")
    else:
        # Use default vector
        default_vector = blender_node.inputs["Vector"].default_value
        vector_node = create_shadergraph_node("Vector3", {"value": default_vector})
        connect_nodes(vector_node, split_node, "In")
    
    # 3. Return dict of component outputs
    # Unity Split outputs: R=X, G=Y, B=Z
    return {
        "X": split_node.outputs["R"],
        "Y": split_node.outputs["G"],
        "Z": split_node.outputs["B"]
    }
```

## Compatibility Notes
- 100% compatible
- Direct mapping to Split node (X→R, Y→G, Z→B)

## Limitations
- None
