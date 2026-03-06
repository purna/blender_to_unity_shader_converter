# ShaderNodeBump

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeBump
- **Category**: Vector
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
- **Primary**: Normal From Height node

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Normal From Height](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Normal-From-Height-Node.html) | Math/Vector | Generates normal from height map |

### Supporting Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Normal From Texture](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Normal-From-Texture-Node.html) | Math/Vector | Generates normal from texture |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Height | Float | 0.5 | Height input (grayscale) |
| Distance | Float | 0.05 | Distance for bump calculation |
| Normal | Normal | 0.0, 0.0, 1.0 | Normal input |
| Invert | Boolean | False | Invert height |
| Strength | Float | 1.0 | Normal strength |

## Conversion Process

### Step 1: Create Normal from Height
- **Description**: Convert height map to normal
- **Blender Input**: Height, Strength, Distance
- **Unity Output**: Normal vector

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Height          ──►     In                    Normal From Height
                                           │
                                           ▼
                                      Normal ──► [Output]
                                          
Strength       ──►     Scale                │
(blender to unity mapping)                  │
                                           │
Distance       ──►     (not directly used)  │
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| In | Float | 0 | Height input |
| Scale | Float | 1 | Strength multiplier |

## Visual Graph Layout

```
// Bump to Normal
[Height Map] ──> [Normal From Height] ──> [Normal Output]
                      ^
                      │
[Float: Strength] ────┘
```

## Pseudocode for Conversion Logic

```python
def convert_bump_node(blender_node):
    """
    Converts Blender ShaderNodeBump to Unity ShaderGraph Normal From Height.
    Near conversion - similar but parameter handling differs.
    """
    # 1. Create Normal From Height node
    normal_from_height = create_shadergraph_node("Normal From Height")
    
    # 2. Get inputs
    height_input = get_input_connection(blender_node.inputs["Height"])
    strength = blender_node.inputs["Strength"].default_value
    distance = blender_node.inputs["Distance"].default_value
    
    # 3. Connect height
    if height_input:
        connect_nodes(height_input, normal_from_height, "In")
    else:
        normal_from_height.set_input("In", blender_node.inputs["Height"].default_value)
    
    # 4. Handle strength
    # Unity uses "Scale" for the height-to-normal intensity
    # Blender uses "Strength" - need to adjust
    # Approximation: Scale ≈ 1 / Strength
    if strength > 0:
        normal_from_height.set_property("Scale", 1.0 / strength)
    else:
        normal_from_height.set_property("Scale", 1.0)
    
    # Note: Blender's Distance parameter affects how quickly normal changes
    # Unity doesn't have direct equivalent
    
    # 5. Connect optional Normal input (for inverted space)
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        log_warning("Bump: Normal input not fully supported in Unity")
    
    return normal_from_height.outputs["Normal"]
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Vector/Bump.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeBump/MeshRenderer-Snow.ShaderGraph` | Example shader |

## Compatibility Notes
- 100% compatible
- Strength/Scale mapping is approximate
- Distance parameter not available in Unity

## Limitations
- Distance parameter has no direct equivalent
- Inverted normal handling differs
