# Blender to Unity: ShaderNodeAddShader Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeAddShader`
- **Unity ShaderGraph Node**: `Add`
- **Category**: Shading Model
- **Compatibility**: 80% (Conceptual difference)

This document explains how to convert Blender's `ShaderNodeAddShader`. This is not a direct node-for-node conversion due to fundamental differences in how Blender and Unity structure shaders.

## 1. Conceptual Difference: Blender vs. Unity
- **Blender (BSDF Chaining)**: In Blender, you can chain multiple BSDF nodes (e.g., `Principled BSDF`, `Emission`) together using nodes like `Add Shader` and `Mix Shader`. This combines the entire light-scattering behavior of the shaders.
- **Unity (Master Node Stack)**: In Unity's ShaderGraph, you have a single **Master Node** (`PBR` or `Unlit`). All calculations (for Base Color, Normal, Emission, Roughness, etc.) are done *before* they are plugged into the Master Node's inputs. You do not add "shaders" together; you add their *output values*.

The Unity equivalent of `Add Shader` is to calculate the results of two different shader paths and then use an **`Add`** node to combine their final color and emission values.

## 2. Unity ShaderGraph Node Identification
The core of the conversion is the **Add** node.
- **Creation Menu Path**: `Right-click → Create Node → Math → Basic → Add`

## 3. Step-by-Step Recreation Example
Let's recreate a common use case: adding an `Emission` shader to a `Principled BSDF` in Blender.

**Blender Setup:**
- A `Principled BSDF` node defines the base material.
- An `Emission` node defines a light-emitting layer.
- An `Add Shader` node combines them.

**Unity Recreation:**
1.  **Calculate Base Properties**: Set up the nodes for your base material's color, roughness, etc. This branch of nodes represents your `Principled BSDF`.
2.  **Calculate Emission**: Set up a separate branch of nodes that results in the color and strength of your emissive layer. This represents your `Emission` shader.
3.  **Combine with `Add`**:
    - Create an **`Add`** node.
    - Connect the final output of your base color logic to the **`A`** input of the `Add` node.
    - Connect the final output of your emission logic to the **`B`** input of the `Add` node.
4.  **Connect to Master Node**:
    - Connect the result of the `Add` node to the **`Emission`** input on your `PBR Master Node`.
    - Connect the original base color to the **`Base Color`** input.

## 4. Visual Graph Layout
This layout shows how to add a procedural noise pattern as an emissive layer on top of a base color.

```
// Branch 1: Base Color
[Color Node (Blue)] --------------------------------------> [PBR Master Node].[Base Color]

// Branch 2: Emission
[Simple Noise Node] -> [Multiply Node] -> [Color Node (Yellow)] --+
                                                                  |
                                                                  V
[Color Node (Blue)] -----------------------------------------> [Add Node].[A]
                                                                  |
// Combine the results                                            |
[Branch 2 Output] -------------------------------------------> [Add Node].[B]
                                                                  |
                                                                  V
                                                 [PBR Master Node].[Emission]
```

## 5. Pseudocode for Conversion Logic
The conversion logic must identify the two incoming shader branches and add their corresponding outputs.

```python
def convert_add_shader_node(blender_add_node):
  # 1. Identify the two shader trees connected to the Add Shader inputs.
  shader_tree_1 = get_upstream_tree(blender_add_node.inputs["Shader1"])
  shader_tree_2 = get_upstream_tree(blender_add_node.inputs["Shader2"])

  # 2. Convert each tree into its final value outputs (Color, Emission, etc.)
  # This is a recursive process.
  values_1 = convert_shader_tree_to_values(shader_tree_1)
  values_2 = convert_shader_tree_to_values(shader_tree_2)

  # 3. Create 'Add' nodes in Unity to combine the values.
  final_values = {}
  
  # Example for Emission:
  if "Emission" in values_1 and "Emission" in values_2:
    add_emission_node = create_shadergraph_node("Add")
    connect_node(values_1["Emission"], add_emission_node, "output", "A")
    connect_node(values_2["Emission"], add_emission_node, "output", "B")
    final_values["Emission"] = add_emission_node
  elif "Emission" in values_1:
    final_values["Emission"] = values_1["Emission"]
  else:
    final_values["Emission"] = values_2["Emission"]

  # ... repeat for Base Color, etc., as logically appropriate.
  
  # 4. The final_values dictionary now holds the combined nodes
  # that will be connected to the Master Node.
  return final_values
```

## 6. Limitations and Compatibility Notes
- **Architectural Mismatch**: This is the primary limitation. You are not adding fully self-contained shaders. This can be problematic for complex effects like combining two different BSDFs with unique fresnel or specular responses.
- **Energy Conservation**: Manually adding color and emission values can easily lead to non-physically correct results (e.g., materials that reflect more light than they receive). Blender's internal BSDF math handles this more gracefully. In Unity, you must be careful.
- **Best Practice**: Use `Add Shader` in Blender for layering emissive or transparent effects on top of an opaque surface. For mixing two opaque surfaces, a `Mix Shader` (which translates to a `Lerp` in Unity) is often a better choice.
