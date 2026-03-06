# Blender to Unity: ShaderNodeRGB Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeRGB`
- **Unity ShaderGraph Node**: `Color`
- **Category**: Input
- **Compatibility**: 100%

This document provides a comprehensive guide for converting Blender's `ShaderNodeRGB` into a Unity ShaderGraph `Color` node.

## 1. Unity ShaderGraph Node Identification
The direct equivalent for Blender's `ShaderNodeRGB` is the **Color** node in Unity's ShaderGraph. This node allows you to define a constant RGBA color value.

## 2. Step-by-Step Creation in ShaderGraph
To create the `Color` node in Unity ShaderGraph, follow these steps:
1. Open your ShaderGraph asset.
2. Right-click on the graph editor's grid.
3. Navigate the context menu: **Create Node → Input → Basic → Color**.
4. A new `Color` node will appear on your graph.

## 3. Parameter Configuration
The `ShaderNodeRGB` has a single, straightforward parameter to configure:

| Blender Parameter | Unity Node | Unity Parameter | Instructions |
|---|---|---|---|
| `Color` | `Color` | `Color` (preview) | Click the color swatch on the Unity `Color` node. In the color picker window, manually set the R, G, B, and A values to match the values from the Blender `ShaderNodeRGB` node. |

## 4. Visual Graph Layout
The `Color` node is a simple input node. Its primary role is to provide a constant color value to other nodes.

**Expected Layout:**
- The `Color` node's **Output** slot (a single circle) should be connected to an input slot on another node. For example, you can connect it directly to the `Base Color` input of a `PBR Master Node` or an `Unlit Master Node`.

```
[Color Node] --(output)--> [PBR Master Node].[Base Color]
```

## 5. Pseudocode for Conversion Logic
This pseudocode illustrates the logic for an automated conversion script.

```python
def convert_rgb_node(blender_node):
  # 1. Create a new Unity ShaderGraph Color node
  unity_node = create_shadergraph_node("Color")

  # 2. Get the color value from the Blender node
  blender_color = blender_node.outputs["Color"].default_value

  # 3. Set the color value on the Unity node
  # Note: RGBA values in Blender are 0-1, which matches Unity's format.
  unity_node.set_property("Color", blender_color)

  # 4. Return the new node for connection
  return unity_node
```

## Notes
- The conversion is a direct 1:1 mapping and should result in no visual discrepancies.
- Ensure the Alpha (A) channel value is correctly transferred, as it controls transparency.
- This node is one of the most fundamental building blocks for creating materials.
