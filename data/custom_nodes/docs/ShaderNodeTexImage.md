# Blender to Unity: ShaderNodeTexImage Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeTexImage`
- **Unity ShaderGraph Nodes**: `Texture 2D Asset` + `Sample Texture 2D`
- **Category**: Texture
- **Compatibility**: 98%

This document provides a guide for converting Blender's `ShaderNodeTexImage` into a standard texture sampling setup in Unity's ShaderGraph. The process involves two key parts: the texture asset itself and the node that samples it.

## 1. Unity ShaderGraph Node Identification
A single Blender `Image Texture` node corresponds to **two** nodes in ShaderGraph:
1.  **Texture 2D Asset**: This node acts as a reference to the actual texture file (e.g., a `.png` or `.jpg`) in your Unity project.
2.  **Sample Texture 2D**: This node performs the lookup into the texture file at specific UV coordinates and outputs the color.

## 2. Step-by-Step Creation in ShaderGraph
1.  **Import the Texture**: First, drag the image file used in the Blender node into your Unity Project window. This creates a Texture asset.
2.  **Create Texture 2D Asset Node**: In the ShaderGraph editor, right-click and select **Create Node → Input → Texture → Texture 2D Asset**.
3.  **Assign the Texture**: On the `Texture 2D Asset` node, click the circle selection box and choose the texture you imported in step 1.
4.  **Create Sample Texture 2D Node**: Right-click and select **Create Node → Texture → Sample Texture 2D**.
5.  **Connect the Nodes**: Connect the **Output** of the `Texture 2D Asset` node to the **Texture (T2)** input of the `Sample Texture 2D` node.

## 3. Parameter Configuration
Most parameters from Blender's `Image Texture` node are controlled by the **Texture Import Settings** in Unity, not the ShaderGraph nodes.

### In Unity's Inspector (select the texture file):
| Blender Parameter | Unity Texture Import Setting | Notes |
|---|---|---|
| `Color Space` | `sRGB (Color Texture)` | For color textures (Albedo), enable this. For data textures (Masks, Normals, Roughness), disable it (setting it to Linear). |
| `Extension` | `Wrap Mode` | `Repeat` -> `Repeat`, `Extend` -> `Clamp`, `Clip` -> `Clamp`. `Mirror` -> `Mirror`. |
| `Interpolation` | `Filter Mode` | `Linear` -> `Bilinear` or `Trilinear`, `Closest` -> `Point (no filter)`. |

### In ShaderGraph (`Sample Texture 2D` node):
| Blender Input | Unity Node | Unity Input | Notes |
|---|---|---|---|
| `Vector` | `Sample Texture 2D` | `UV` | Connect a `UV` node here. This corresponds to the texture coordinates. |

## 4. Visual Graph Layout
The standard texture sampling layout is fundamental to almost all materials.

**Expected Layout:**
```
[UV Node] ---------> [Sample Texture 2D Node].[UV]
[Texture 2D Asset] -> [Sample Texture 2D Node].[Texture]

                       [Sample Texture 2D Node].[RGBA] -> [PBR Master Node].[Albedo]
```

## 5. Pseudocode for Conversion Logic
The conversion logic must handle both asset management and graph construction.

```python
def convert_image_texture_node(blender_node):
  # 1. Identify the image file used in Blender
  image_path = blender_node.image.filepath

  # 2. Find or create the corresponding texture asset in the Unity project
  unity_texture_asset = import_texture_to_unity(image_path)
  
  # --- Configure Texture Import Settings ---
  # Color Space
  if blender_node.image.colorspace_settings.name == 'sRGB':
    set_texture_import_setting(unity_texture_asset, "sRGB", True)
  else:
    set_texture_import_setting(unity_texture_asset, "sRGB", False) # Linear
  
  # Wrap Mode (Extension)
  wrap_mode = map_blender_extension_to_unity(blender_node.extension)
  set_texture_import_setting(unity_texture_asset, "wrapMode", wrap_mode)

  # --- Create ShaderGraph Nodes ---
  # 3. Create the Texture 2D Asset node
  tex_asset_node = create_shadergraph_node("Texture 2D Asset")
  tex_asset_node.set_asset(unity_texture_asset)

  # 4. Create the sampler node
  sampler_node = create_shadergraph_node("Sample Texture 2D")

  # 5. Connect the asset to the sampler
  connect_nodes(tex_asset_node, sampler_node, "output", "Texture")

  # The 'Vector' input and 'Color'/'Alpha' outputs are handled
  # by connecting other nodes to this setup.
  return sampler_node
```

## 6. Limitations and Compatibility Notes
- **Projection Modes**: Blender's `Box`, `Sphere`, and `Tube` projection mapping do not have a direct, one-node equivalent. They must be recreated manually using procedural math in ShaderGraph, typically involving `Position`, `Normal Vector`, and `Transform` nodes. This is a complex task. The converter should default to UV mapping.
- **Single Channel Output**: The `Sample Texture 2D` node outputs RGBA. If you only need one channel (like the `Alpha`), you must use a `Split` node after the sampler.
