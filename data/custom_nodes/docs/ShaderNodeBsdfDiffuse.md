# ShaderNodeBsdfDiffuse

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeBsdfDiffuse
- **Category**: BSDF
- **Compatibility**: 70%

## Unity Equivalent
- **Primary**: PBR Master node (approximate with Base Color + Roughness)
- **Alternative**: Custom shader for exact match

## Conversion Process

### Step 1: Map Base Properties
- **Description**: Extract color from Diffuse BSDF
- **Blender Input**: Color
- **Unity Output**: Base Color

### Step 2: Set Roughness
- **Description**: Diffuse has no roughness control in Blender, default to 1.0
- **Blender Input**: None (always 1.0)
- **Unity Output**: Smoothness = 0

### Step 3: Connect to Master
- **Description**: Connect to PBR Master
- **Unity Output**: PBR Master inputs

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Base Color | 100% |
| Normal | Normal | 100% |

## Visual Graph Layout

```
// Diffuse to PBR Master
[Color] ──> [PBR Master].[Base Color]
                 ^
                 │
[Float: 0] ─────┤  (Smoothness = 0)
[Float: 0] ─────┤  (Metallic = 0)
```

## Pseudocode for Conversion Logic

```python
def convert_bsdf_diffuse_node(blender_node):
    """
    Converts Blender ShaderNodeBsdfDiffuse to Unity ShaderGraph PBR Master.
    Near conversion - Diffuse is basic diffuse, maps to PBR with fixed roughness.
    """
    # Create PBR Master (or reuse existing)
    pbr_master = get_or_create_pbr_master()
    
    # 1. Connect Color to Base Color
    color_input = get_input_connection(blender_node.inputs["Color"])
    if color_input:
        connect_nodes(color_input, pbr_master, "Base Color")
    else:
        pbr_master.set_input("Base Color", blender_node.inputs["Color"].default_value)
    
    # 2. Diffuse has no roughness - set to maximum (Unity Smoothness = 0)
    pbr_master.set_input("Roughness", 1.0)  # Diffuse = fully rough
    pbr_master.set_input("Metallic", 0.0)   # Diffuse = non-metallic
    
    # 3. Connect Normal if present
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, pbr_master, "Normal")
    
    return pbr_master
```

## Compatibility Notes
- 70% compatible
- Diffuse BSDF in Blender has no roughness - maps to fully rough in Unity
- Cannot create pure diffuse in Unity PBR (always specular)

## Limitations
- No pure diffuse in PBR - always has some specular reflection
- For exact diffuse, need custom shader (not using PBR Master)

## Example
See [`Lambert.shadergraph`](../../examples/ShaderNodeBsdfDiffuse/Lambert.shadergraph) for a Unity implementation of diffuse lighting using the dot product between surface normal and light direction - exactly matching Blender's Diffuse BSDF.
