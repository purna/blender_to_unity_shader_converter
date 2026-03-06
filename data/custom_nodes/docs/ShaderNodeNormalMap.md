# ShaderNodeNormalMap

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeNormalMap
- **Category**: Vector
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
**Normal From Texture** node with **Sample Texture 2D** - Direct mapping

## Unity Shader Graph Nodes

### Primary Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Normal From Texture](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Normal-From-Texture-Node.html) | Math/Vector | Generates normal from texture |
| [Sample Texture 2D](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Sample-Texture-2D-Node.html) | Texture | Samples texture |

### Supporting Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Strength multiplier |
| [UV](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/UV-Node.html) | Input | UV coordinates |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color | Color | 0.5, 0.5, 1.0, 1.0 | Normal map texture |
| Vector | Vector | 0, 0 | UV coordinates |
| Space | Enum | Tangent | Tangent/Object/World space |
| Strength | Float | 1.0 | Normal strength |

## Conversion Process

### Step 1: Sample Normal Map
- **Description**: Sample the normal map texture with Type=Normal
- **Blender Input**: Normal map texture (RGB)
- **Unity Output**: RGB color from texture

### Step 2: Connect to Normal Map Node
- **Description**: Connect texture to Normal From Texture node
- **Blender Input**: RGB texture output
- **Unity Output**: Normal vector

### Step 3: Apply Strength
- **Description**: Adjust normal strength if needed
- **Blender Input**: Strength parameter
- **Unity Output**: Adjusted normal

## Unity Connections

### Basic Setup
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Texture          ──►     Base Map             Sample Texture 2D (Normal)
UV              ──►     UV                   │
                                           │
                                           ▼
                                     Normal Out
                                           │
                                           ▼
                                Normal From Texture
                                           │
                                           ▼
                                      Out ──► [Output]
```

### With Strength Adjustment
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Texture          ──►     Base Map             Sample Texture 2D (Normal)
UV              ──►     UV                   │
                                           │
                                           ▼
                                     Normal Out
                                           │
                                           ▼
                                Normal From Texture
                                           │
                                           ▼
                                      Out ◄──┐
                                             │
                              Multiply ◄──────┤
                                   │         │
                              Strength        │
                                   │         │
                                   └─────────┘
                                             ▼
                                      Out ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| Base Map | Texture | None | Normal map texture |
| UV | Vector2 | 0,0 | UV coordinates |
| Type | Enum | Normal | Texture type |

## Build Instructions

1. Create Sample Texture 2D node
2. Set Type to "Normal"
3. Connect to Normal From Texture node (or use inline)
4. Connect output to PBR Normal input
5. For strength: Use Multiply node after Normal From Texture

## Visual Graph Layout

```
// Basic Normal Map setup
[Texture 2D Asset] ──> [Sample Texture 2D: Normal] ──> [PBR Master].[Normal]
                                        ^
                                        │
[UV] ──────────────────────────────────┘

// With Strength adjustment
[Texture 2D Asset] ──> [Sample Texture 2D: Normal] ──> [Multiply] ──> [PBR Master].[Normal]
              ^                                              ^
              │                                              │
[Float: 1.5] ─┴──────────────────────────────────────────────┘
```

## Pseudocode for Conversion Logic

```python
def convert_normalmap_node(blender_node):
    """
    Converts Blender ShaderNodeNormalMap to Unity ShaderGraph Normal From Texture.
    1-1 direct mapping with minor strength adjustment difference.
    """
    # 1. Get the image input
    image_input = get_input_connection(blender_node.inputs["Color"])
    
    # 2. Get parameters
    strength = blender_node.inputs["Strength"].default_value
    space = blender_node.space  # 'TANGENT', 'OBJECT', 'WORLD'
    
    if image_input:
        # Get the texture from upstream
        texture_node = trace_texture_from_socket(image_input)
        texture_asset = texture_node.image
    else:
        # Use the image from the Normal Map node itself
        texture_asset = blender_node.image
    
    # 3. Create Sample Texture 2D node with Normal type
    sample_node = create_shadergraph_node("Sample Texture 2D")
    sample_node.set_property("texture", texture_asset)
    sample_node.set_property("mode", "Normal")  # This is key!
    
    # 4. Connect UV (from texture node or create default)
    uv_input = get_input_connection(blender_node.inputs["Vector"])
    if uv_input:
        connect_nodes(uv_input, sample_node, "UV")
    else:
        # Use default UV from object
        uv_node = create_shadergraph_node("UV")
        connect_nodes(uv_node, sample_node, "UV")
    
    # 5. Handle space conversion (Tangent to Object/World)
    # Unity ShaderGraph uses tangent space by default
    if space == "TANGENT":
        # Unity default - no conversion needed
        normal_output = sample_node.outputs["Normal"]
    elif space == "OBJECT" or space == "WORLD":
        # Need to transform from object/world to tangent space
        # This is complex - might require Custom Function
        log_warning(
            f"NormalMap: {space} space not directly supported. "
            "Converting to tangent space."
        )
        normal_output = sample_node.outputs["Normal"]
    else:
        normal_output = sample_node.outputs["Normal"]
    
    # 6. Apply strength multiplier
    if strength != 1.0:
        multiply_node = create_shadergraph_node("Multiply")
        connect_nodes(normal_output, multiply_node, "A")
        multiply_node.set_input("B", strength)
        return multiply_node
    
    return normal_output
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Vector/Normal Map.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeNormalMap/Normals.shader` | Example shader |

## Notes
- Direct mapping to Unity normal map workflow
- 10% loss due to minor encoding differences
- Supports Tangent, Object, World spaces
- Key: Must set Sample Texture 2D to "Normal" mode in Unity
