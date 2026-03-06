# ShaderNodeInvert

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeInvert
- **Category**: Color
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP

## Unity Equivalent
**One Minus** node - Direct 1:1 mapping

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [One Minus](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/One-Minus-Node.html) | Math/Utility | Inverts the input value (1 - input) |

### Alternative Node Chain
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Subtract](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Subtract-Node.html) | Math/Basic | Use with 1.0 for inversion |
| [Lerp](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Lerp-Node.html) | Math/Interpolation | For factor-based blending |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color | Color | 1.0, 1.0, 1.0, 1.0 | Input color to invert |
| Factor | Float | 1.0 | Blend factor for inversion |

## Conversion Process

### Step 1: Direct Inversion (Simple)
- **Description**: Invert color using One Minus node
- **Blender Input**: Color
- **Unity Output**: Inverted color

### Step 2: Factor-Based Inversion (With Blend)
- **Description**: Blend between original and inverted based on Factor
- **Blender Input**: Color, Factor
- **Unity Nodes**: One Minus + Lerp

## Unity Connections

### Simple Inversion
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color (0,8)     ──►     In                  One Minus
                                        │
                                        ▼
                                   Out         ──►   [Output]
```

### Factor-Based Inversion
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color            ──►     A                   Lerp
                              ▲
                              │
Color            ──►     One Minus ──► B     Lerp
                              │
                              ▼
Factor           ──►     T
                                 │
                                 ▼
                              Out         ──►   [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| In | Vector4 | 0 | Input color to invert |

## Visual Graph Layout

```
// Simple inversion
[Color: 0.8] ──> [One Minus] ──> [Output: 0.2]

// Factor-based inversion (Blender's Fac input)
[Color] ──┬─> [One Minus] ──┬─> [Lerp] ──> [Output]
          │                 │      ^
          │                 │      │
          └─────────────────┘   [Fac]
```

## Pseudocode for Conversion Logic

```python
def convert_invert_node(blender_node):
    """
    Converts Blender ShaderNodeInvert to Unity ShaderGraph One Minus node.
    1-1 direct mapping for basic color/value inversion.
    """
    # 1. Check if Factor input is connected
    factor_input = get_input_connection(blender_node.inputs["Fac"])
    color_input = get_input_connection(blender_node.inputs["Color"])
    
    if factor_input is None and color_input is None:
        # No inputs connected - use default values
        color_value = blender_node.inputs["Color"].default_value
        factor_value = blender_node.inputs["Fac"].default_value
        
        # Create One Minus node with direct value
        unity_one_minus = create_shadergraph_node("One Minus")
        
        # Set the color value directly
        if isinstance(color_value, (int, float)):
            unity_one_minus.set_input("In", color_value)
        else:
            # It's a color, need to handle differently
            unity_color = create_shadergraph_node("Color", {"value": color_value})
            connect_nodes(unity_color, unity_one_minus, "In")
        
        return unity_one_minus
    
    elif factor_input is not None:
        # Factor-based inversion: Lerp(Color, 1-Color, Factor)
        # This requires multiple nodes
        
        # Create original color node
        if color_input:
            original = color_input
        else:
            # Use default color
            color_value = blender_node.inputs["Color"].default_value
            original = create_shadergraph_node("Color", {"value": color_value})
        
        # Create One Minus for inverted version
        one_minus = create_shadergraph_node("One Minus")
        connect_nodes(original, one_minus, "In")
        
        # Create Lerp to blend based on factor
        lerp_node = create_shadergraph_node("Lerp")
        connect_nodes(original, lerp_node, "A")
        connect_nodes(one_minus, lerp_node, "B")
        
        if factor_input:
            connect_nodes(factor_input, lerp_node, "T")
        else:
            # Use default factor
            factor_value = blender_node.inputs["Fac"].default_value
            lerp_node.set_input("T", factor_value)
        
        return lerp_node
    
    else:
        # Simple 1 - Color inversion
        unity_one_minus = create_shadergraph_node("One Minus")
        connect_nodes(color_input, unity_one_minus, "In")
        return unity_one_minus
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Color/Invert.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeInvert/2 Tone Dissolve.shader` | Example shader |

## Notes
- Fully compatible - direct 1:1 mapping
- Unity's One Minus node performs exactly the same operation
- For factor-based inversion: Lerp(Color, 1-Color, Factor)
- Works with both color (RGBA) and float inputs
