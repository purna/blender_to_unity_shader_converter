# ShaderNodeBsdfPrincipled

## Conversion Type: 2 (Near Conversion)

## Overview
Blender's universal physically-based shader that covers most material types. This is the most complex conversion as it has many parameters.

## Unity Equivalent
- **Primary**: PBR Master (Lit) - covers 90% of use cases
- **Advanced**: Custom shader for subsurface, clearcoat, sheen

## Conversion Process

### Step 1: Basic PBR Mapping (90%)
| Blender Parameter | Unity Input | Notes |
|-----------------|-------------|-------|
| Base Color | Base Color | Direct mapping |
| Metallic | Metallic | 0-1 float |
| Roughness | Smoothness | Invert: 1-Roughness |
| Normal | Normal | Connect normal map |
| Emission | Emission | Color × Strength |

### Step 2: Unsupported Features (10%)
- **Subsurface Scattering**: Approximate with translucent or custom SSS shader
- **Clearcoat**: Add second specular layer if needed
- **Sheen**: Use Sheen in PBR Master (URP/HDRP)
- **Transmission**: Use Transparent surface type

## Visual Graph Layout

```
// Basic PBR Material
[Color] ──> [PBR Master].[Base Color]
[Float: Metallic] ──> [PBR Master].[Metallic]
[Float: 1.0 - Roughness] ──> [PBR Master].[Smoothness]
[Normal Map] ──> [PBR Master].[Normal]
[Emission Color] ──> [Multiply: Strength] ──> [PBR Master].[Emission]

// With SSS approximation
[Color] ──> [PBR Master].[Base Color]
                      ^
                      │
[Color: Subsurface] ──┤
[Float: Subsurface Weight] ──> [PBR Master].[Subsurface]
```

## Pseudocode for Conversion Logic

```python
def convert_principled_bsdf_node(blender_node):
    """
    Converts Blender ShaderNodeBsdfPrincipled to Unity ShaderGraph PBR Master node.
    Near conversion - most properties map directly, some require approximation.
    """
    # Create PBR Master node
    pbr_master = create_shadergraph_node("PBR Master")
    
    # 1. Base Color - Direct mapping
    base_color_input = get_input_connection(blender_node.inputs["Base Color"])
    if base_color_input:
        connect_nodes(base_color_input, pbr_master, "Base Color")
    else:
        pbr_master.set_input("Base Color", blender_node.inputs["Base Color"].default_value)
    
    # 2. Metallic - Direct mapping (0-1)
    metallic_input = get_input_connection(blender_node.inputs["Metallic"])
    if metallic_input:
        connect_nodes(metallic_input, pbr_master, "Metallic")
    else:
        pbr_master.set_input("Metallic", blender_node.inputs["Metallic"].default_value)
    
    # 3. Roughness -> Smoothness (INVERT!)
    # Unity Smoothness = 1.0 - Blender Roughness
    roughness_input = get_input_connection(blender_node.inputs["Roughness"])
    if roughness_input:
        # Create One Minus node to invert
        one_minus = create_shadergraph_node("One Minus")
        connect_nodes(roughness_input, one_minus, "In")
        connect_nodes(one_minus, pbr_master, "Smoothness")
    else:
        roughness = blender_node.inputs["Roughness"].default_value
        pbr_master.set_input("Smoothness", 1.0 - roughness)
    
    # 4. Normal - Direct mapping
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, pbr_master, "Normal")
    
    # 5. Emission - Direct with strength
    emission_color_input = get_input_connection(blender_node.inputs["Emission Color"])
    emission_strength = blender_node.inputs["Emission Strength"].default_value
    
    if emission_color_input:
        if emission_strength != 1.0:
            # Multiply color by strength
            multiply = create_shadergraph_node("Multiply")
            connect_nodes(emission_color_input, multiply, "A")
            multiply.set_input("B", emission_strength)
            connect_nodes(multiply, pbr_master, "Emission")
        else:
            connect_nodes(emission_color_input, pbr_master, "Emission")
    
    # 6. Subsurface Scattering (NOT DIRECTLY SUPPORTED)
    sss_input = get_input_connection(blender_node.inputs["Subsurface Weight"])
    if sss_input:
        log_warning(
            "Principled BSDF: Subsurface Scattering not directly supported. "
            "Use Translucent BSDF or custom shader."
        )
        # Approximation: Use as subsurface color
        sss_color = blender_node.inputs["Subsurface"].default_value
        # Note: URP/HDRP have different SSS support
    
    # 7. Clearcoat - URP/HDRP has Sheen/Clearcoat
    clearcoat_weight = blender_node.inputs["Clearcoat Weight"].default_value
    if clearcoat_weight > 0:
        log_warning(
            "Principled BSDF: Clearcoat not fully supported in standard ShaderGraph. "
            "Enable Sheen/Clearcoat in PBR Master if available."
        )
        # In URP: Enable Clearcoat in Master Node settings
        # Note: Clearcoat requires additional setup
    
    # 8. Sheen - Available in HDRP/URP
    sheen_weight = blender_node.inputs["Sheen Weight"].default_value
    if sheen_weight > 0:
        sheen_color = blender_node.inputs["Sheen Color"].default_value
        pbr_master.set_property("Sheen", True)
        pbr_master.set_input("Sheen Color", sheen_color)
        pbr_master.set_input("Sheen", sheen_weight)
    
    # 9. Transmission -> Transparency
    transmission = blender_node.inputs["Transmission Weight"].default_value
    if transmission > 0:
        # Need to set surface type to Transparent
        pbr_master.set_property("Surface Type", "Transparent")
        # Note: IOR handling differs
    
    return pbr_master
```

## Compatibility: 50% (due to advanced features)

## Limitations
- SSS requires custom implementation
- Clearcoat/Coat not directly supported
- Advanced transmission needs custom shader
- IOR calculations differ
- Some URP versions have limited support for advanced PBR features
