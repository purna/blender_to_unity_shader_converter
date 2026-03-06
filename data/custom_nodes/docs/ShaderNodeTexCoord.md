# Blender to Unity: ShaderNodeTexCoord Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeTexCoord`
- **Unity ShaderGraph Node(s)**: `UV`, `Position`, `Normal Vector`, `Screen Position`
- **Category**: Input
- **Compatibility**: 95% (See limitations for specific outputs)

This document explains how to convert the versatile `ShaderNodeTexCoord` from Blender into the appropriate nodes in Unity's ShaderGraph. This single Blender node maps to multiple, more specific nodes in Unity.

## 1. Unity ShaderGraph Node Identification
The `ShaderNodeTexCoord` provides several distinct coordinate systems. Each output in Blender has a corresponding node in Unity ShaderGraph.

| Blender Output | Unity ShaderGraph Node | Creation Menu Path |
|---|---|---|
| `Generated` | `Position` | `Input → Geometry → Position` |
| `Normal` | `Normal Vector` | `Input → Geometry → Normal Vector` |
| `UV` | `UV` | `Input → Geometry → UV` |
| `Object` | `Position` | `Input → Geometry → Position` |
| `Camera` | N/A | See Limitations |
| `Window` | `Screen Position` | `Input → Geometry → Screen Position`|
| `Reflection` | N/A | See Limitations |

## 2. Step-by-Step Creation and Configuration

### A. For Blender's `UV` Output:
- **Action**: Create a **UV** node in ShaderGraph.
- **Instructions**:
    1. Right-click and select **Create Node → Input → Geometry → UV**.
    2. The `UV` node has outputs for UV0, UV1, UV2, and UV3. By default, connect the **UV0** output to the `UV` input of a `Sample Texture 2D` node. This is the most common use case.

### B. For Blender's `Object` Output:
- **Action**: Create a **Position** node in ShaderGraph.
- **Instructions**:
    1. Right-click and select **Create Node → Input → Geometry → Position**.
    2. On the created `Position` node, set the **Space** dropdown to **Object**.
    3. The `Out` port will now provide the vertex position relative to the object's origin.

### C. For Blender's `Generated` and `Normal` Outputs:
- **Action**: Use the **Position** and **Normal Vector** nodes respectively.
- **Instructions**:
    1. Create the appropriate node (`Position` or `Normal Vector`).
    2. Set the **Space** dropdown to **World**. This is the standard behavior for these outputs in Blender.

## 3. Visual Graph Layout Examples

**Layout for UV Mapping:**
```
[UV Node] --(UV0)--> [Sample Texture 2D Node].[UV]
                      [Texture 2D Asset] --> [Sample Texture 2D Node].[Texture]
```

**Layout for Object-Space Projection:**
```
[Position Node (Space: Object)] --(Out)--> [Split Node].[In]
                                             [Split Node].[R(X)] --> (Use for procedural texturing)
```

## 4. Pseudocode for Conversion Logic
This pseudocode demonstrates how to handle the multi-output nature of this node.

```python
def convert_tex_coord_node(blender_node, used_output_name):
  # This function is called for each output that is used.

  if used_output_name == "UV":
    # Create a UV node in Unity
    unity_node = create_shadergraph_node("UV")
    # The output to connect from will be "UV0" by default
    return unity_node, "UV0"

  elif used_output_name == "Object":
    # Create a Position node set to Object space
    unity_node = create_shadergraph_node("Position")
    unity_node.set_property("Space", "Object")
    return unity_node, "Out"

  elif used_output_name == "Normal":
    # Create a Normal Vector node
    unity_node = create_shadergraph_node("Normal Vector")
    unity_node.set_property("Space", "World")
    return unity_node, "Out"
    
  elif used_output_name == "Generated":
    # Generated coordinates are based on the object's bounding box.
    # A full recreation requires getting the bounding box size and offsetting
    # the object-space position. This is a more complex setup.
    # A simpler approximation is to use Object space position.
    unity_node = create_shadergraph_node("Position")
    unity_node.set_property("Space", "Object")
    # Add comment in graph: "Approximation of Blender's 'Generated' coords."
    return unity_node, "Out"

  # ... handle other outputs like Window, etc.

  else:
    # Output is not supported or recognized
    return None, None
```

## 5. Limitations and Compatibility Notes
- **Camera Output**: Blender's `Camera` output provides coordinates relative to the camera's view plane. This can be recreated in ShaderGraph by using a `Transform` node to convert `Position` from World to View space, but it's not a direct one-node equivalent.
- **Reflection Output**: The `Reflection` output is specific to ray tracing contexts in Cycles and does not have a direct, general-purpose equivalent in Unity's standard ShaderGraph rasterization pipeline. It is generally not convertible.
- **Generated Coordinates**: A precise 1:1 conversion of `Generated` coordinates is complex, as it depends on the object's bounding box dimensions, which are not directly available as a simple node in ShaderGraph. The common practice is to approximate it with `Position (Object Space)` and then manually adjust with `Multiply` and `Add` nodes if needed.
