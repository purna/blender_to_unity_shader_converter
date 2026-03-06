# Blender to Unity: ShaderNodeBevel Conversion Guide

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: `ShaderNodeBevel`
- **Unity ShaderGraph Equivalent**: `Bevel` Node or Baked Normal Map
- **Category**: Input / Normals
- **Compatibility**: 70% (Depends on Unity version and workflow)

This document explains how to convert Blender's `ShaderNodeBevel`, which is a shader-based effect that simulates rounded edges on geometry.

## 1. Conceptual Overview: Procedural Edge Beveling
The `ShaderNodeBevel` in Blender does not actually add geometry. Instead, it's a procedural technique that operates on the normal vectors of the mesh. It detects sharp edges and generates a new normal vector that smoothly interpolates across the edge, giving the *illusion* of a soft, beveled, or rounded corner. This is a powerful technique for adding detail without increasing polygon count.

Unity has a similar node in some versions of ShaderGraph, but the most common and reliable method in game development is to bake this detail into a normal map.

## 2. Conversion Strategy

### Method 1: Using the `Bevel` Node (If Available)
Some versions of Unity's ShaderGraph include a built-in `Bevel` node that works similarly to Blender's.

- **Creation Menu Path**: `Create Node → Utility → Bevel` (Path may vary)
- **Workflow**:
    1. Create a `Bevel` node.
    2. Set the **Radius** to match the `Radius` from the Blender node.
    3. The `Output` of the `Bevel` node is a new normal vector. Connect this to the **Normal** input of your `PBR Master Node`.

### Method 2: Baking a Normal Map (Recommended Workflow)
This is the most performant and reliable method for production.
- **Workflow**:
    1. In Blender, create a high-poly version of your model with real, geometric bevels.
    2. Create a low-poly version (the one you will use in-game).
    3. Use Blender's **Cycles Bake** functionality to bake the normals from the high-poly model to the low-poly model's UV map. Set the **Bake Type** to **Normal**.
    4. Save the resulting normal map texture.
    5. In Unity, use a `Sample Texture 2D` node to read the baked normal map and connect it to the **Normal** input of your Master Node.

### Method 3: Manual Recreation (Advanced)
It is possible to recreate the effect from scratch using derivative nodes (`ddx`/`ddy`) and other math, but this is highly complex and not recommended for general use.

## 3. Visual Graph Layout (Using Unity's `Bevel` Node)
```
[Bevel Node] --(Output)--> [PBR Master Node].[Normal]
  (Set Radius)
```

## 4. Pseudocode for Conversion Logic
The converter should try to use the built-in `Bevel` node and issue a warning if it's not a perfect match.

```python
def convert_bevel_node(blender_node):
  # 1. Get the parameters from the Blender node.
  radius = blender_node.inputs["Radius"].default_value
  samples = blender_node.inputs["Samples"].default_value

  # 2. Check if a Bevel node exists in the target Unity version.
  if shadergraph_version_has_bevel_node():
    # 3. Create a Unity Bevel node.
    unity_bevel_node = create_shadergraph_node("Bevel")
    unity_bevel_node.set_property("Radius", radius)
    
    # Unity's node may not have a 'Samples' property.
    if samples > 4: # Blender's default is 4
      log_warning(
        "Blender's Bevel node used a high sample count ({samples}). " \
        "Unity's Bevel node may not have this setting, potentially " \
        "resulting in lower quality. For best results, consider baking a normal map."
      )
      
    return unity_bevel_node
  else:
    # 4. If the node doesn't exist, log a clear error.
    log_error(
      "The material uses a Bevel node, but this node is not available " \
      "in your version of ShaderGraph. The recommended workflow is to " \
      "bake a normal map from a high-poly beveled model in Blender."
    )
    return None
```

## 5. Limitations and Best Practices
- **Performance**: Real-time bevel calculations are expensive. For anything other than simple hard-surface models, this can negatively impact performance.
- **Quality**: The quality of shader-based bevels can sometimes be inconsistent, with artifacts appearing at complex geometry intersections.
- **Best Practice**: For hero assets or any performance-sensitive scenario, **baking normals from a high-poly model is the superior method**. It provides the highest quality at the best performance (the cost of a simple texture sample). Use real-time bevels sparingly for procedural or simple geometric shaders.
