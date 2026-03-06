# Blender to Unity: ShaderNodeVertexColor Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeVertexColor`
- **Unity ShaderGraph Node**: `Vertex Color`
- **Category**: Input
- **Compatibility**: 100% (Requires mesh with vertex colors)

This document provides a guide for converting Blender's `ShaderNodeVertexColor` into the corresponding `Vertex Color` node in Unity's ShaderGraph.

## 1. Unity ShaderGraph Node Identification
The direct equivalent for Blender's `ShaderNodeVertexColor` is the **Vertex Color** node in Unity ShaderGraph. This node accesses the color data stored per-vertex in the mesh asset.

## 2. Step-by-Step Creation in ShaderGraph
1.  Open your ShaderGraph asset.
2.  Right-click on the graph editor's grid.
3.  Navigate the context menu: **Create Node → Input → Geometry → Vertex Color**.
4.  A new `Vertex Color` node will appear on your graph.

## 3. Parameter Configuration
The node itself has no parameters to configure in ShaderGraph. The data it outputs is entirely dependent on the mesh asset being rendered.

| Blender Input/Property | Unity Node | Unity Output | Notes |
|---|---|---|---|
| `Color Layer` (selected layer) | `Vertex Color` | `Out` (RGBA) | Unity's `Vertex Color` node reads the primary vertex color channel. Blender can have multiple named layers, but standard formats like FBX typically only transfer one. Ensure you are using the active/primary layer in Blender. |

## 4. Visual Graph Layout
The `Vertex Color` node is a powerful input for adding detail and variation to materials without using textures.

**Expected Layout:**
- The `Out` port of the `Vertex Color` node is connected to an input on another node. A common use is to connect it directly to the `Base Color` of a master node, or to use it as a mask by first splitting its channels.

```
[Vertex Color Node] --(Out)--> [PBR Master Node].[Base Color]

// OR, using it as a mask:
[Vertex Color Node] --(Out)--> [Split Node].[In]
                               [Split Node].[R] --> [Lerp Node].[T]
```

## 5. Pseudocode for Conversion Logic
The conversion logic is straightforward as it's a direct node-for-node replacement.

```python
def convert_vertex_color_node(blender_node):
  # 1. Check which vertex color layer is being used in Blender.
  # If it's not the primary/default layer, log a warning, as only
  # the primary layer is typically exported.
  if blender_node.layer_name != get_active_vertex_color_layer_name():
    log_warning("Shader uses a non-primary vertex color layer ('{}'). " \
                "Ensure this layer is correctly exported and imported in Unity.")

  # 2. Create a new Unity ShaderGraph Vertex Color node.
  unity_node = create_shadergraph_node("Vertex Color")

  # 3. Return the new node for connection.
  # The node has no inputs to connect.
  return unity_node
```

## 6. Limitations and Compatibility Notes
- **Mesh Dependency**: This node will output black `(0,0,0,0)` if the mesh being rendered does not contain vertex color data.
- **Import Settings**: When you import your 3D model (e.g., an FBX) into Unity, you must ensure that vertex colors are being imported. In the Model Import Settings in the Inspector, find the **"Vertex Colors"** setting and make sure it is set to **"Import"**.
- **Multiple Layers**: Blender supports multiple, named vertex color layers on a single object. Unity's default mesh pipeline and the `Vertex Color` node primarily work with a single color channel. While advanced techniques using custom C# scripts and multiple UV channels can access more data, the standard conversion maps to the primary vertex color layer only.
