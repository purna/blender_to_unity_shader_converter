# ShaderNodeEmission

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeEmission
- **Category**: Shading
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Emission input on PBR Master
- **Alternative**: Multiply node + Emission input

## Conversion Process

### Step 1: Connect Color
- **Description**: Connect emission color
- **Blender Input**: Color
- **Unity Output**: Emission color

### Step 2: Apply Strength
- **Description**: Multiply color by strength
- **Blender Input**: Strength
- **Unity Output**: Emission with multiplier

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Emission Color | 100% |
| Strength | Emission Strength (via Multiply) | 100% |
| Normal | Normal (not used for emission) | N/A |

## Visual Graph Layout

```
// Simple Emission (strength = 1.0)
[Color] ──> [PBR Master].[Emission]

// With Strength (strength > 1.0)
[Color] ──> [Multiply] ──> [PBR Master].[Emission]
              ^
              │
[Float: Strength] ────────┘
```

## Pseudocode for Conversion Logic

```python
def convert_emission_node(blender_node):
    """
    Converts Blender ShaderNodeEmission to Unity ShaderGraph.
    1-1 direct mapping - connects to PBR Master Emission input.
    """
    pbr_master = get_or_create_pbr_master()
    
    # 1. Get inputs
    color_input = get_input_connection(blender_node.inputs["Color"])
    strength = blender_node.inputs["Strength"].default_value
    
    # 2. Handle emission with strength
    if strength != 1.0:
        # Need to multiply color by strength
        multiply_node = create_shadergraph_node("Multiply")
        
        if color_input:
            connect_nodes(color_input, multiply_node, "A")
        else:
            multiply_node.set_input("A", blender_node.inputs["Color"].default_value)
        
        multiply_node.set_input("B", strength)
        
        connect_nodes(multiply_node, pbr_master, "Emission")
    else:
        # Direct connection
        if color_input:
            connect_nodes(color_input, pbr_master, "Emission")
        else:
            pbr_master.set_input("Emission", blender_node.inputs["Color"].default_value)
    
    return pbr_master
```

## Compatibility Notes
- 100% compatible
- Direct mapping to PBR Master Emission input

## Limitations
- None - simple and direct
