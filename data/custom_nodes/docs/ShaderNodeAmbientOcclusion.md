# Blender to Unity: ShaderNodeAmbientOcclusion Conversion Guide

## Conversion Type: 4 (No Conversion - Requires Baking)

## Overview
- **Blender Node**: `ShaderNodeAmbientOcclusion`
- **Unity ShaderGraph Equivalent**: Baked Texture Workflow (Not a direct node)
- **Category**: Input / Rendering
- **Compatibility**: 10% (Not directly convertible)

This document explains why Blender's `ShaderNodeAmbientOcclusion` cannot be directly converted to a single Unity ShaderGraph node and describes the standard industry workflow for achieving the same effect.

## 1. Conceptual Difference: Real-time Ray Tracing vs. Baked Textures
- **Blender Cycles/Eevee**: The `Ambient Occlusion` node is a powerful, real-time effect. It dynamically calculates light occlusion by casting rays into the surrounding scene from the shaded point. This is computationally expensive and requires knowledge of the entire scene geometry.
- **Unity ShaderGraph**: A Unity shader, by default, only knows about the single vertex/pixel it is currently rendering. It cannot "see" other objects in the scene to calculate real-time ambient occlusion.

Therefore, the effect must be **pre-calculated (baked)** into a texture map in Blender. The Unity shader then just reads from this texture.

## 2. The Ambient Occlusion (AO) Baking Workflow

### Step 1: Bake the AO in Blender
1.  In Blender, ensure you have a separate, blank Image Texture created to bake to.
2.  Select your object and go to the **Render Properties** tab.
3.  Change the **Render Engine** to **Cycles**.
4.  In the **Bake** panel, set the **Bake Type** to **Ambient Occlusion**.
5.  Make sure your object's material has the blank image texture node selected (but not necessarily connected to anything).
6.  Click the **Bake** button. Blender will render the AO data onto your blank texture.
7.  **Save** the resulting image as a `.png` or `.jpg` file.

### Step 2: Use the AO Map in Unity ShaderGraph
1.  **Import** the saved AO texture into your Unity project.
2.  In ShaderGraph, create a **`Texture 2D Asset`** node and assign your AO texture to it.
3.  Create a **`Sample Texture 2D`** node and connect the `Texture 2D Asset` to its input.
4.  The output of the `Sample Texture 2D` (typically the **R** channel) now contains your AO data.
5.  Use a **`Multiply`** node to combine the AO with your base color.

## 3. Visual Graph Layout (Unity)
This is the standard setup for applying a baked AO map.

```
// Base Color
[Color Node (Blue)] -----------------------------+
                                                  |
                                                  V
// AO Map                                [Multiply Node] -> [PBR Master Node].[Base Color]
[Texture 2D Asset (AO Map)] -> [Sample Texture 2D] -+
           |                                        ^
           V                                        |
      [Split Node] -> [R Channel] ------------------+

```
*Note: Using a `Split` and taking the `R` channel is common practice as AO is grayscale data and can be packed efficiently.*

## 4. Pseudocode for Conversion Logic
An automated converter cannot perform the bake process. Instead, it should detect the use of the `ShaderNodeAmbientOcclusion` and provide guidance.

```python
def convert_ambient_occlusion_node(blender_node):
  # 1. Detect that an AO node is being used.
  is_ao_node_present = True

  # 2. Check if the output of the AO node is connected to something.
  if is_node_output_connected(blender_node.outputs["Color"]) or \
     is_node_output_connected(blender_node.outputs["AO"]):
    
    # 3. Log a critical warning for the user.
    log_manual_step_required(
      "The material uses a real-time Ambient Occlusion node. " \
      "This cannot be converted directly to Unity ShaderGraph. " \
      "You must BAKE the Ambient Occlusion to a texture in Blender (Cycles Bake) " \
      "and then use that texture to multiply against your Base Color in Unity."
    )

  # 4. Return nothing, as no nodes can be created automatically.
  return None
```

## 5. Alternative: Screen Space Ambient Occlusion (SSAO)
Unity provides its own real-time ambient occlusion solutions as a post-processing effect.
- **URP**: Add the **Screen Space Ambient Occlusion (SSAO)** renderer feature to your URP Forward Renderer asset.
- **HDRP**: Provides a high-quality AO effect in the Volume settings.

These effects are global, apply to the whole screen, and are **not** part of the material conversion process. They are configured in the renderer settings, not in ShaderGraph.
