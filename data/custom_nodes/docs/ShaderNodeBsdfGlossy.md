# ShaderNodeBsdfGlossy

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeBsdfGlossy
- **Category**: BSDF
- **Compatibility**: 70%

## Unity Equivalent
- **Primary**: PBR Master with high Metallic, controlled Smoothness

## Conversion Process

### Step 1: Set Metallic
- **Description**: Glossy = metallic reflection
- **Unity**: Set Metallic to 1.0

### Step 2: Map Roughness
- **Description**: Invert roughness to smoothness
- **Blender Input**: Roughness
- **Unity Output**: Smoothness (1 - Roughness)

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Base Color | 100% |
| Roughness | Smoothness (invert) | 90% |
| Normal | Normal | 100% |

## Visual Graph Layout

```
// Glossy to PBR Master
[Color] ──> [PBR Master].[Base Color]
                 ^
                 │
[Float: 1.0] ───┤  (Metallic = 1.0)
                 ^
                 │
[Float: 1-Roughness] ──> [Smoothness]
```

## Pseudocode for Conversion Logic

```python
def convert_bsdf_glossy_node(blender_node):
    """
    Converts Blender ShaderNodeBsdfGlossy to Unity ShaderGraph PBR Master.
    Near conversion - maps to metallic surface.
    """
    pbr_master = get_or_create_pbr_master()
    
    # 1. Glossy = metallic in PBR
    pbr_master.set_input("Metallic", 1.0)
    
    # 2. Connect Color
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
    
    # 4. Connect Normal
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, pbr_master, "Normal")
    
    return pbr_master
```

## Compatibility Notes
- 70% compatible
- Glossy is essentially metallic reflection in PBR
- Different fresnel calculations between Blender and Unity

## Limitations
- Cannot create non-metallic specular in Unity PBR
- Fresnel behavior differs
