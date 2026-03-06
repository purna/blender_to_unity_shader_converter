# ShaderNodeBsdfGlass

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeBsdfGlass
- **Category**: BSDF
- **Compatibility**: 60%

## Unity Equivalent
- **Primary**: PBR Master with Transparent surface type
- **Advanced**: Custom refraction shader

## Conversion Process

### Step 1: Set Surface Type
- **Description**: Enable transparency
- **Unity**: Set Surface Type to Transparent

### Step 2: Map Properties
- **Description**: Connect Color, Roughness, IOR
- **Blender Input**: Color, Roughness, IOR
- **Unity Output**: Base Color, Smoothness, Index of Refraction

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Base Color | 100% |
| Roughness | Smoothness (invert) | 90% |
| IOR | Index of Refraction | 80% |
| Normal | Normal | 100% |

## Visual Graph Layout

```
// Glass to PBR Master (Transparent)
[Color] ──> [PBR Master].[Base Color]
                 ^
                 │
[Float: IOR] ────┤
[Float: 1-Roughness] ──> [Smoothness]
                 
// Set Surface Type: Transparent
// Set Blend Mode: Alpha
```

## Pseudocode for Conversion Logic

```python
def convert_bsdf_glass_node(blender_node):
    """
    Converts Blender ShaderNodeBsdfGlass to Unity ShaderGraph.
    Near conversion - requires transparent surface type.
    """
    # Get or create PBR Master
    pbr_master = get_or_create_pbr_master()
    
    # 1. Set surface type to Transparent
    pbr_master.set_property("Surface Type", "Transparent")
    pbr_master.set_property("Blend Mode", "Alpha")
    
    # 2. Connect Color to Base Color
    color_input = get_input_connection(blender_node.inputs["Color"])
    if color_input:
        connect_nodes(color_input, pbr_master, "Base Color")
    else:
        pbr_master.set_input("Base Color", blender_node.inputs["Color"].default_value)
    
    # 3. Handle Roughness -> Smoothness (invert)
    roughness_input = get_input_connection(blender_node.inputs["Roughness"])
    if roughness_input:
        one_minus = create_shadergraph_node("One Minus")
        connect_nodes(roughness_input, one_minus, "In")
        connect_nodes(one_minus, pbr_master, "Smoothness")
    else:
        roughness = blender_node.inputs["Roughness"].default_value
        pbr_master.set_input("Smoothness", 1.0 - roughness)
    
    # 4. Handle IOR
    ior_input = get_input_connection(blender_node.inputs["IOR"])
    if ior_input:
        connect_nodes(ior_input, pbr_master, "Index of Refraction")
    else:
        ior = blender_node.inputs["IOR"].default_value
        pbr_master.set_input("Index of Refraction", ior)
    
    # 5. Connect Normal
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, pbr_master, "Normal")
    
    return pbr_master
```

## Compatibility Notes
- 60% compatible
- Glass requires transparent surface type
- IOR support varies by render pipeline (URP limited)

## Limitations
- True refraction not fully supported in standard ShaderGraph
- URP has limited IOR/transmission support
- Need HDRP for full glass refraction
