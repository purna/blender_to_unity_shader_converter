# ShaderNodeGamma

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeGamma
- **Category**: Color
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP

## Unity Equivalent
- **Primary**: Gamma node
- **Alternative**: Power node (with 1/gamma exponent)

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Gamma](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Gamma-Node.html) | Math/Utility | Applies gamma correction to input |

### Alternative Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Power](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Power-Node.html) | Math/Exponential | Use with exponent = 1/gamma |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color | Color | 1.0, 1.0, 1.0, 1.0 | Input color |
| Gamma | Float | 1.0 | Gamma exponent value |

## Conversion Process

### Step 1: Connect Input
- **Description**: Connect color to gamma node
- **Blender Input**: Color
- **Unity Output**: Gamma corrected color

### Step 2: Set Gamma
- **Description**: Set gamma value
- **Blender Input**: Gamma (default 1.0)
- **Unity Output**: Power exponent

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     In                  Gamma
                                        │
                                        ▼
                                   Out         ──►   [Output]
                                      
                                      Gamma
                                        │
                                        ▼
                                   Out         ──►   [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| In | Vector4 | 0 | Input color |
| Gamma | Float | 1.0 | Gamma exponent |

## Visual Graph Layout

```
// Basic Gamma correction
[Color] ──> [Gamma] ──> [Output]
              ^
              │
[Float: 2.2] ─┘

// Alternative using Power
[Color] ──> [Power] ──> [Output]
              ^
              │
[Float: 0.4545] ──► (1/2.2)
```

## Pseudocode for Conversion Logic

```python
def convert_gamma_node(blender_node):
    """
    Converts Blender ShaderNodeGamma to Unity ShaderGraph Gamma node.
    1-1 direct mapping - exact equivalent.
    """
    # 1. Create Gamma node
    gamma_node = create_shadergraph_node("Gamma")
    
    # 2. Get inputs
    color_input = get_input_connection(blender_node.inputs["Color"])
    gamma_input = get_input_connection(blender_node.inputs["Gamma"])
    
    # 3. Connect color
    if color_input:
        connect_nodes(color_input, gamma_node, "In")
    else:
        gamma_node.set_input("In", blender_node.inputs["Color"].default_value)
    
    # 4. Set gamma value
    if gamma_input:
        connect_nodes(gamma_input, gamma_node, "Gamma")
    else:
        gamma_node.set_input("Gamma", blender_node.inputs["Gamma"].default_value)
    
    return gamma_node
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Color/Gamma.shadersubgraph` | Unity Shader Graph subgraph |

## Compatibility Notes
- 100% compatible
- Direct 1:1 mapping
- Unity's Gamma node is equivalent to Blender's Gamma node
- Alternative: Use Power with 1/gamma for correction

## Limitations
- None
