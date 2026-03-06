# Blender to Unity: ShaderNodeSeparateRGB Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeSeparateRGB`
- **Unity ShaderGraph Node**: `Split`
- **Category**: Converter
- **Compatibility**: 100%

This document provides a comprehensive guide for converting Blender's `ShaderNodeSeparateRGB` into a Unity ShaderGraph `Split` node.

## 1. Unity ShaderGraph Node Identification
The direct equivalent for Blender's `ShaderNodeSeparateRGB` is the **Split** node in Unity's ShaderGraph. This node takes a multi-channel input (like a `Vector4` color) and separates it into its individual R, G, B, and A channels.

## 2. Step-by-Step Creation in ShaderGraph
To create the `Split` node in Unity ShaderGraph, follow these steps:
1. Open your ShaderGraph asset.
2. Right-click on the graph editor's grid.
3. Navigate the context menu: **Create Node → Channel → Split**.
4. A new `Split` node will appear on your graph.

## 3. Parameter Configuration
The `Split` node has one input and four outputs. The key is to correctly link the preceding node.

| Blender Input | Unity Node | Unity Input | Instructions |
|---|---|---|---|
| `Image` | `Split` | `In (4)` | Connect the output of another node (e.g., a `Color` node, `Texture 2D Asset` node, or any `Vector4` property) to the `In` slot of the `Split` node. |

The outputs are then used independently:
- **R**: The red channel as a float.
- **G**: The green channel as a float.
- **B**: The blue channel as a float.
- **A**: The alpha channel as a float.

## 4. Visual Graph Layout
The `Split` node acts as a channel separator.

**Expected Layout:**
- A node providing a `Vector4` (like a `Color` node) is connected to the `In` port of the `Split` node.
- The `R`, `G`, `B`, and `A` output ports are then connected to the input ports of other nodes. For instance, you could use the `R` output to control the `Metallic` property of a `PBR Master Node`.

```
[Color Node] --(output)--> [Split Node].[In]
                               [Split Node].[R] --(output)--> [Other Node].[Input]
                               [Split Node].[G] --(output)--> [Another Node].[Input]
```

## 5. Pseudocode for Conversion Logic
This pseudocode illustrates the logic for an automated conversion script.

```python
def convert_separate_rgb_node(blender_node, all_nodes):
  # 1. Create a new Unity ShaderGraph Split node
  unity_split_node = create_shadergraph_node("Split")

  # 2. Find the node connected to the Blender "Image" input
  connected_blender_node = blender_node.inputs["Image"].links[0].from_node
  
  # 3. Find the corresponding Unity node that was already converted
  unity_source_node = find_converted_node(connected_blender_node, all_nodes)

  # 4. Connect the source node to the new Split node
  connect_nodes(unity_source_node, unity_split_node, "output", "In")

  # 5. Return the new node for subsequent connections
  # The outputs (R, G, B, A) will be connected in a later step
  # when processing the nodes that use them.
  return unity_split_node
```

## Notes
- The `ShaderNodeSeparateRGB` in Blender separates a color input. The `Split` node in Unity is more versatile and can separate any `Vector2`, `Vector3`, or `Vector4`. The converter should ensure the input is treated as a color.
- This conversion is a direct 1:1 mapping of functionality.
- It is essential for workflows where individual color channels are used to drive different material properties (e.g., packing Roughness, Metallic, and Ambient Occlusion into one texture).
