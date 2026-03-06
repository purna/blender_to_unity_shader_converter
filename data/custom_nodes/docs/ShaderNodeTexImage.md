# ShaderNodeTexImage

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeTexImage
- **Category**: Texture
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Texture 2D Asset + Sample Texture 2D

## Conversion Process

### Step 1: Create Texture Asset
- **Description**: Import texture image
- **Blender Input**: Image file
- **Unity Output**: Texture 2D Asset node

### Step 2: Sample Texture
- **Description**: Sample the texture with UVs
- **Blender Input**: Vector (UV)
- **Unity Output**: RGBA color

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Image | Texture 2D Asset | 100% |
| Vector | UV input to Sample Texture | 100% |

## Visual Graph Layout

```
// Basic Texture Sampling
[Texture 2D Asset] ──> [Sample Texture 2D] ──> [Output: RGBA]
                               ^
                               │
                         [UV Coordinates]

// With color space conversion (Linear/sRGB)
[Sample Texture 2D] ──> [Gamma] ──> [Output]
```

## Pseudocode for Conversion Logic

```python
def convert_teximage_node(blender_node):
    """
    Converts Blender ShaderNodeTexImage to Unity ShaderGraph.
    1-1 direct mapping - Texture 2D Asset + Sample Texture 2D.
    """
    # 1. Get the image from Blender node
    image = blender_node.image
    
    # 2. Create Texture 2D Asset node with the image
    texture_asset = create_shadergraph_node("Texture 2D Asset")
    texture_asset.set_property("texture", image)
    
    # 3. Create Sample Texture 2D node
    sample_node = create_shadergraph_node("Sample Texture 2D")
    
    # 4. Connect texture asset to sample
    connect_nodes(texture_asset.outputs["Texture"], sample_node, "Texture")
    
    # 5. Connect UV/Vector input
    vector_input = get_input_connection(blender_node.inputs["Vector"])
    if vector_input:
        connect_nodes(vector_input, sample_node, "UV")
    else:
        # Use default UV from UV node
        uv_node = create_shadergraph_node("UV")
        connect_nodes(uv_node, sample_node, "UV")
    
    # 6. Handle color space (sRGB vs Linear)
    # Blender automatically handles color space in node output
    # Unity Sample Texture 2D has "sRGB" checkbox
    color_space = blender_node.color_space  # 'sRGB', 'NONE', 'LINEAR'
    
    if color_space == 'sRGB':
        sample_node.set_property("sRGB", True)
    else:
        sample_node.set_property("sRGB", False)
    
    # 7. Return the RGBA output
    return sample_node.outputs["RGBA"]
```

## Compatibility Notes
- 100% compatible
- Direct mapping
- Texture import needs to be done manually in Unity

## Limitations
- Image file must be imported separately into Unity
- Texture settings (filtering, wrapping) set in Unity
