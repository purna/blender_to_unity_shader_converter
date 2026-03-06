# ShaderNodeTexCoord

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeTexCoord
- **Category**: Input
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: UV node or Texture Coordinate node

## Conversion Process

### Step 1: Select Coordinate Type
- **Description**: Choose UV/Object/World/Normal coordinates
- **Blender Input**: Node setting (not shader input)
- **Unity Output**: Corresponding UV output

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Generated | UV0 | 100% |
| Normal | Normal | 100% |
| UV0 | UV0 | 100% |
| UV1 | UV1 | 100% |
| UV2 | UV2 | 100% |
| Object | Object Space Position | 100% |
| World | World Space Position | 100% |

## Visual Graph Layout

```
// UV Coordinates from different sources
[UV] ──────────────────────────> [Texture Sample].[UV]
                                   ^
[Generated] ──────────────────────┤
                                   ^
[Object Position] ────────────────┤

// World Space for triplanar
[World Position] ──> [Subtract: Object Position] ──> [Triplanar]
```

## Pseudocode for Conversion Logic

```python
def convert_texcoord_node(blender_node):
    """
    Converts Blender ShaderNodeTexCoord to Unity ShaderGraph.
    1-1 direct mapping - different coordinate outputs.
    """
    # 1. Get the coordinate type from Blender
    texcoord_type = blender_node.texcoord  # 'UV', 'GENERATED', 'NORMAL', 'OBJECT', 'WORLD'
    
    outputs = {}
    
    if texcoord_type == 'UV' or texcoord_type == 'GENERATED':
        # Blender UV/Generated maps to Unity UV
        uv_node = create_shadergraph_node("UV")
        outputs["UV"] = uv_node.outputs["UV"]
        
        # Also connect to UV1, UV2 if needed
        if blender_node.uv_map != "":
            # Named UV map - need to handle specially
            log_warning(f"TexCoord: Named UV map '{blender_node.uv_map}' requires custom setup")
    
    elif texcoord_type == 'OBJECT':
        # Object space position
        position_node = create_shadergraph_node("Position")
        position_node.set_property("space", "Object")
        outputs["Object"] = position_node.outputs["Position"]
    
    elif texcoord_type == 'WORLD':
        # World space position
        position_node = create_shadergraph_node("Position")
        position_node.set_property("space", "World")
        outputs["World"] = position_node.outputs["Position"]
    
    elif texcoord_type == 'NORMAL':
        # Surface normal
        normal_node = create_shadergraph_node("Normal")
        outputs["Normal"] = normal_node.outputs["Normal"]
    
    # Return dictionary of available outputs
    return outputs
```

## Compatibility Notes
- 100% compatible
- Direct mapping between coordinate systems

## Limitations
- Named UV maps require additional setup
- Some coordinate spaces behave differently
