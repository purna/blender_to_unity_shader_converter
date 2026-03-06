# ShaderNodeBsdfTransparent

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeBsdfTransparent
- **Category**: BSDF
- **Compatibility**: 80%

## Unity Equivalent
- **Primary**: PBR Master with Transparent surface type

## Conversion Process

### Step 1: Set Surface Type
- **Description**: Enable transparency
- **Unity**: Set Surface Type to Transparent

### Step 2: Map Color
- **Description**: Connect color to emission or base color
- **Blender Input**: Color
- **Unity Output**: Base Color + Transparent

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Base Color + Alpha | 100% |
| Normal | Normal | 100% |

## Visual Graph Layout

```
// Transparent to PBR Master
[Color] ──> [PBR Master].[Base Color]
                 ^
                 │
[Float: 1.0] ───┤  (Alpha = 1.0)

// Set Surface Type: Transparent
```

## Pseudocode for Conversion Logic

```python
def convert_bsdf_transparent_node(blender_node):
    """
    Converts Blender ShaderNodeBsdfTransparent to Unity ShaderGraph.
    Near conversion - requires transparent surface type.
    """
    pbr_master = get_or_create_pbr_master()
    
    # 1. Set surface to Transparent
    pbr_master.set_property("Surface Type", "Transparent")
    pbr_master.set_property("Blend Mode", "Alpha")
    
    # 2. Connect Color to Base Color
    color_input = get_input_connection(blender_node.inputs["Color"])
    if color_input:
        connect_nodes(color_input, pbr_master, "Base Color")
    else:
        pbr_master.set_input("Base Color", blender_node.inputs["Color"].default_value)
    
    # 3. Set Alpha to 1.0 (fully transparent - shows what's behind)
    pbr_master.set_input("Alpha", 1.0)
    
    # 4. Connect Normal
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, pbr_master, "Normal")
    
    return pbr_master
```

## Compatibility Notes
- 80% compatible
- Simple transparency works well
- Complex transparency (ray-traced) not supported

## Limitations
- No true refraction transparency
- Cannot handle colored transparency the same way as Blender
