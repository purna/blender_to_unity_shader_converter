# Blender to Unity: ShaderNodeSeparateXYZ Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeSeparateXYZ`
- **Unity ShaderGraph Node**: `Split`
- **Category**: Converter
- **Compatibility**: 100%

This document provides a comprehensive guide for converting Blender's `ShaderNodeSeparateXYZ` into a Unity ShaderGraph `Split` node.

## 1. Unity ShaderGraph Node Identification
The direct equivalent for Blender's `ShaderNodeSeparateXYZ` is the **Split** node in Unity's ShaderGraph. This node takes a multi-channel vector input (e.g., `Vector3`) and separates it into its individual components.

## 2. Step-by-Step Creation in ShaderGraph
To create the `Split` node in Unity ShaderGraph, follow these steps:
1. Open your ShaderGraph asset.
2. Right-click on the graph editor's grid.
3. Navigate the context menu: **Create Node → Channel → Split**.
4. A new `Split` node will appear on your graph.

## 3. Parameter Configuration
The `Split` node's primary configuration involves connecting a vector input. The outputs will correspond to the components of that vector.

| Blender Input | Unity Node | Unity Input | Instructions |
|---|---|---|---|
| `Vector` | `Split` | `In (3)` | Connect the output of a node that provides vector data (e.g., `Position`, `Normal Vector`, or a `Vector3` property) to the `In` slot of the `Split` node. |

The `Split` node automatically adapts its outputs based on the input type. For a `Vector3` input from `ShaderNodeSeparateXYZ`, it will provide:
- **R**: The **X** component as a float.
- **G**: The **Y** component as a float.
- **B**: The **Z** component as a float.
- **A**: Unused/disabled for a `Vector3` input.

## 4. Visual Graph Layout
The `Split` node is a utility node used to deconstruct vectors.

**Expected Layout:**
- A node providing vector data (like the `Position` node) is connected to the `In` port of the `Split` node.
- The `R`, `G`, and `B` output ports (representing X, Y, and Z) are then connected to other nodes. For example, you could use the `R` (X) output to drive the movement of a texture coordinate.

```
[Position Node] --(output)--> [Split Node].[In]
                                [Split Node].[R] --(output)--> [Add Node].[A]
                                [Split Node].[G] --(output)--> [Multiply Node].[A]
```

## 5. Pseudocode for Conversion Logic
This pseudocode illustrates the logic for an automated conversion script.

```python
def convert_separate_xyz_node(blender_node, all_nodes):
  # 1. Create a new Unity ShaderGraph Split node
  unity_split_node = create_shadergraph_node("Split")

  # 2. Find the node connected to the Blender "Vector" input
  connected_blender_node = blender_node.inputs["Vector"].links[0].from_node
  
  # 3. Find the corresponding Unity node that was already converted
  unity_source_node = find_converted_node(connected_blender_node, all_nodes)

  # 4. Connect the source node to the new Split node
  connect_nodes(unity_source_node, unity_split_node, "output", "In")

  # 5. Return the new node for subsequent connections
  # The outputs (R, G, B) will be connected when processing the
  # nodes that use them. Note the R, G, B to X, Y, Z mapping.
  return unity_split_node
```

## Notes
- While the `Split` node in Unity uses R, G, B, A labels for its outputs, these directly correspond to X, Y, Z, W when a vector is input. This is a crucial detail for the conversion logic.
- This conversion is a direct 1:1 mapping of functionality and is essential for any vector manipulation.
- This node is frequently used with `TexCoord` (UVs), `Position`, and `Normal Vector` nodes.
