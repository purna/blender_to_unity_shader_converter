# Blender to Unity: ShaderNodeTangent Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeTangent`
- **Unity ShaderGraph Node**: `Tangent Vector`
- **Category**: Input
- **Compatibility**: 90% (Requires mesh tangents)

This document provides a comprehensive guide for converting Blender's `ShaderNodeTangent` into a Unity ShaderGraph `Tangent Vector` node.

## 1. Unity ShaderGraph Node Identification
The direct equivalent for Blender's `ShaderNodeTangent` is the **Tangent Vector** node in Unity's ShaderGraph. This node provides access to the mesh's vertex tangent vector, which is essential for lighting calculations, especially with normal maps.

## 2. Step-by-Step Creation in ShaderGraph
To create the `Tangent Vector` node in Unity ShaderGraph, follow these steps:
1. Open your ShaderGraph asset.
2. Right-click on the graph editor's grid.
3. Navigate the context menu: **Create Node → Input → Geometry → Tangent Vector**.
4. A new `Tangent Vector` node will appear on your graph.

## 3. Parameter Configuration
The `Tangent Vector` node in Unity has a critical **Space** parameter that must be configured correctly to match the Blender context.

| Blender Property | Unity Node | Unity Parameter | Instructions |
|---|---|---|---|
| (Implicitly World Space) | `Tangent Vector` | `Space` | Set the `Space` dropdown on the `Tangent Vector` node to **World**. Blender's shader nodes generally operate in World Space by default, so this ensures consistency. Other options (`Object`, `View`, `Tangent`) are available for more advanced use cases. |

The node has one output:
- **Out**: A `Vector3` representing the tangent vector in the selected space.

## 4. Visual Graph Layout
The `Tangent Vector` node is an input node that provides core mesh data.

**Expected Layout:**
- The `Tangent Vector` node's `Out` port is connected to other nodes that require tangent information. It is a key component in constructing a custom TBN (Tangent, Bitangent, Normal) matrix if you are not using a `Normal Map` node.

```
[Tangent Vector] --(Out)--> [Dot Product Node].[A]
                                [Normal Vector] --(Out)--> [Dot Product Node].[B]
```

## 5. Pseudocode for Conversion Logic
This pseudocode illustrates the logic for an automated conversion script.

```python
def convert_tangent_node(blender_node):
  # 1. Create a new Unity ShaderGraph Tangent Vector node
  unity_tangent_node = create_shadergraph_node("Tangent Vector")

  # 2. Configure the coordinate space
  # Blender's 'Tangent' node provides the tangent in world space.
  # The Unity 'Tangent Vector' node defaults to World space, but we set it explicitly.
  unity_tangent_node.set_property("Space", "World")

  # 3. Return the new node for subsequent connections
  return unity_tangent_node
```

## Notes
- **Compatibility Warning (90%)**: This conversion is only successful if the mesh data in Unity includes tangents. When exporting from Blender (e.g., via FBX), ensure that **"Export Tangents"** is enabled. If the mesh lacks tangents, the `Tangent Vector` node will return a zero vector `(0,0,0)`, which can lead to incorrect lighting or black materials.
- The `ShaderNodeTangent` is often used in conjunction with `ShaderNodeNormalMap` or for creating anisotropic shading effects. The `Tangent Vector` node serves the same purpose in Unity.
- Always verify that your mesh import settings in Unity have "Tangents" set to "Calculate" or "Import" to ensure this node functions correctly.
