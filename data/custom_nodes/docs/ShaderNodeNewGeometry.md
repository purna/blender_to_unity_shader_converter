# ShaderNodeNewGeometry

## Conversion Type: 4 (No Conversion - Limited)

## Overview
- **Blender Node**: ShaderNodeNewGeometry
- **Category**: Input
- **Compatibility**: 30%

## Unity Equivalent
- **Partial**: Position, Normal, UV nodes available
- **None**: Many Blender-only attributes not available

## Conversion Process

### Step 1: Map Available Attributes
- **Description**: Connect available geometry attributes
- **Blender Output**: Incoming, Normal, True Normal, UV, UV(2), etc.
- **Unity Output**: Position, Normal, UV0 available

### Step 2: Handle Unavailable Attributes
- **Description**: Log warning for unavailable attributes
- **Blender Output**: Point Coord, Random, etc.
- **Unity Output**: Not available

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Position | Position node | 100% |
| Normal | Normal node | 100% |
| UV | UV node | 100% |
| True Normal | Normal (World) | 80% |
| Point Coord | Not available | 0% |
| Random | Not available | 0% |

## Visual Graph Layout

```
// Available geometry inputs
[Position] ──────────────────────> [Shader Input]
[Normal] ────────────────────────> [Shader Input]
[UV] ────────────────────────────> [Shader Input]

// Not available in Unity
// - Point Coord
// - Random  
// - Particle Info
```

## Pseudocode for Conversion Logic

```python
def convert_newgeometry_node(blender_node):
    """
    Converts Blender ShaderNodeNewGeometry to Unity ShaderGraph nodes.
    Partial conversion - only some attributes available.
    """
    outputs = {}
    
    # Get the attribute being accessed
    attribute = blender_node.attribute_type  # 'UV', 'NORMAL', 'POSITION', etc.
    
    if attribute == 'UV':
        # UV coordinates
        uv_node = create_shadergraph_node("UV")
        outputs["UV"] = uv_node.outputs["UV"]
    
    elif attribute == 'NORMAL':
        # Surface normal
        normal_node = create_shadergraph_node("Normal")
        outputs["Normal"] = normal_node.outputs["Normal"]
    
    elif attribute == 'POSITION':
        # Vertex position
        position_node = create_shadergraph_node("Position")
        outputs["Position"] = position_node.outputs["Position"]
    
    elif attribute == 'TRUE_NORMAL':
        # World normal
        normal_node = create_shadergraph_node("Normal")
        normal_node.set_property("space", "World")
        outputs["True Normal"] = normal_node.outputs["Normal"]
    
    else:
        # Attributes not available in Unity
        log_error(
            f"Geometry attribute '{attribute}' is not available in Unity ShaderGraph. "
            f"Available: Position, Normal, UV. "
            f"Not available: Point Coord, Random, etc."
        )
        return None
    
    return outputs
```

## Compatibility Notes
- 30% compatible
- Only basic attributes (Position, Normal, UV) available

## Limitations
- Point Coord not available
- Random value not available
- Many Blender-specific attributes not in Unity
