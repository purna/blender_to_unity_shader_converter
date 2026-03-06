# Blender to Unity: ShaderNodeVelvet Conversion Guide

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: `ShaderNodeVelvet`
- **Unity ShaderGraph Equivalent**: Custom Shader / PBR with approximation
- **Category**: Shader
- **Compatibility**: 75% (Partial)

This document explains how to convert Blender's `ShaderNodeVelvet` to Unity with approximation.

## 1. Conceptual Overview
The `ShaderNodeVelvet` in Blender creates a velvet shader with specific BRDF (Bidirectional Reflectance Distribution Function) properties. Unity doesn't have a direct velvet shader, but it can be approximated using PBR properties.

## 2. Unity Equivalent
- **Primary**: PBR Master with custom setup
- **Alternative**: Custom Shader

## 3. Parameters

| Blender Input | Type | Unity Implementation | Notes |
|--------------|------|---------------------|-------|
| Color | Color | Base Color | Direct mapping |
| Sigma | Float | Smoothness/Roughness | Manual conversion |

## 4. Conversion Strategy

### Method 1: PBR Approximation
- Use a PBR Master node
- Set Base Color to the velvet color
- Adjust Smoothness to approximate the velvet sheen
- Lower smoothness values create more velvet-like appearance

### Method 2: Custom Shader
- Create a custom shader with appropriate BRDF
- Implement the velvet reflectance formula
- Expose Color and Sigma as shader properties

## 5. Visual Graph Layout

```
[Color] ──> [PBR Master].[Base Color]
              ^ (Low Smoothness for velvet)
[Sigma] ──> [Smoothness]
```

## 6. Pseudocode for Conversion Logic

```python
def convert_velvet_node(blender_node):
    # Get inputs
    color = get_input_connection(blender_node.inputs["Color"])
    sigma = blender_node.inputs["Sigma"].default_value
    
    # Create PBR Master
    pbr_master = create_shadergraph_node("PBR Master")
    
    # Connect color
    if color:
        connect_nodes(color, pbr_master, "Base Color")
    
    # Convert sigma to smoothness (inverse relationship)
    # Lower sigma = higher smoothness for velvet effect
    smoothness = 1.0 - sigma
    smoothness_node = create_shadergraph_node("Float", {"value": smoothness})
    connect_nodes(smoothness_node, pbr_master, "Smoothness")
    
    log_warning(
        "Velvet shader is approximated using PBR. "
        "The characteristic velvet sheen may not match exactly."
    )
    
    return pbr_master
```

## 7. Limitations
- No direct velvet shader in Unity
- Sigma parameter must be inverted to Smoothness
- The characteristic velvet edge reflectance is an approximation
- May require custom shader for exact match
