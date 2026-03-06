# Blender to Unity: ShaderNodeAttribute Conversion Guide

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: `ShaderNodeAttribute`
- **Unity ShaderGraph Equivalent**: `Vertex Color`, `UV`, or advanced custom inputs.
- **Category**: Input
- **Compatibility**: 85% (Depends on the attribute type)

This document explains how to convert Blender's versatile `ShaderNodeAttribute` node, which can access various types of mesh data by name.

## 1. Conceptual Overview
The `ShaderNodeAttribute` in Blender is a generic accessor for data stored on a mesh's geometry. Instead of having separate nodes for every data type, this one node can retrieve them by name.

In Unity, the most common attributes have their own dedicated, easy-to-use nodes. The conversion strategy therefore depends entirely on the **name of the attribute** being requested in Blender.

## 2. Conversion Strategy by Attribute Type

### Case 1: Attribute is a Vertex Color Layer
- **Blender Setup**: `Attribute` node with `Attribute Name` set to a vertex color layer's name (e.g., the default "Col").
- **Unity Equivalent**: **`Vertex Color`** node.
- **Creation Menu Path**: `Create Node → Input → Geometry → Vertex Color`.
- **Notes**: This is a direct 1:1 mapping. Unity's node will access the primary vertex color data imported with the mesh.

### Case 2: Attribute is a UV Map
- **Blender Setup**: `Attribute` node with `Attribute Name` set to a UV Map's name (e.g., "UVMap", "UV2").
- **Unity Equivalent**: **`UV`** node.
- **Creation Menu Path**: `Create Node → Input → Geometry → UV`.
- **Notes**: On the `UV` node in ShaderGraph, you can select which UV channel to read from (UV0, UV1, UV2, UV3). The Blender attribute name must be mapped to the correct Unity channel. "UVMap" typically maps to UV0. "UV2" would map to UV1, and so on.

### Case 3: Attribute is Custom Data (Advanced)
- **Blender Setup**: `Attribute` node accessing a custom attribute created by the user (e.g., a float value named "wetness").
- **Unity Equivalent**: **No direct node.** This is an advanced use case requiring custom scripting.
- **Workflow**:
    1.  In Unity, a C# script is required to attach the custom data to the mesh vertices. This is often done by storing the data in an unused UV channel or by creating custom vertex streams.
    2.  In ShaderGraph, a **`Custom Interpolator`** node or a **`Custom Function`** node (using HLSL) is then needed to read this specific data from the vertex stream.
- **Compatibility**: 0% for automated conversion. This requires manual C# and HLSL programming.

## 3. Visual Graph Layout Examples

**Vertex Color Case:**
```
[Vertex Color Node] --(Out)--> [PBR Master Node].[Base Color]
```

**UV Map Case (for a second UV channel):**
```
[UV Node] --(UV1)--> [Sample Texture 2D Node].[UV]
```

## 4. Pseudocode for Conversion Logic
The converter logic must inspect the attribute name and choose the correct path.

```python
def convert_attribute_node(blender_node):
  # 1. Get the attribute name from the Blender node.
  attr_name = blender_node.attribute_name

  # 2. Check if it matches known attribute types.
  if attr_name in get_list_of_vertex_color_layer_names():
    # It's a vertex color layer.
    unity_node = create_shadergraph_node("Vertex Color")
    return unity_node

  elif attr_name in get_list_of_uv_map_names():
    # It's a UV map.
    unity_node = create_shadergraph_node("UV")
    
    # Determine which channel to use (e.g., 'UVMap' -> 0, 'UV2' -> 1)
    uv_channel_index = get_uv_channel_index_from_name(attr_name)
    
    # The output will be from the specific channel pin (UV0, UV1, etc.)
    output_pin_name = f"UV{uv_channel_index}"
    return unity_node, output_pin_name
    
  else:
    # 3. If it's not a recognized type, it's custom data.
    log_error(
      f"The material uses an 'Attribute' node for custom data ('{attr_name}'). " \
      "This is not directly supported in ShaderGraph. You must manually " \
      "create a C# script to upload this data to the mesh and use a " \
      "Custom Interpolator or Custom Function node to read it."
    )
    return None

```

## 5. Limitations and Summary
- The `ShaderNodeAttribute` is a powerful, flexible node in Blender.
- For the most common cases (accessing vertex colors and UVs), the conversion is straightforward, mapping to Unity's dedicated `Vertex Color` and `UV` nodes.
- For accessing any other arbitrary, user-defined vertex data, automated conversion is not feasible. This advanced feature requires manual recreation using C# and potentially HLSL, falling outside the scope of a direct converter.
