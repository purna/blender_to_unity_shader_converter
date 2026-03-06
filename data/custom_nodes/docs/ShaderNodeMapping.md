# ShaderNodeMapping

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeMapping
- **Category**: Vector
- **Compatibility**: 90%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
- **Basic**: Tiling And Offset node (Location/Scale only)
- **Full**: Rotate + Tiling And Offset (includes rotation)

## Unity Shader Graph Nodes

### Primary Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Tiling And Offset](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Tiling-And-Offset-Node.html) | UV | Applies tiling and offset to UV coordinates |
| [Rotate](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Rotate-Node.html) | Math/Vector | Rotates UV coordinates |

### Supporting Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Scale multiplication |
| [Add](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Add-Node.html) | Math/Basic | Location offset |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Vector | Vector3 | 0, 0, 0 | Input vector/UV |
| Location | Vector3 | 0, 0, 0 | Translation offset |
| Rotation | Vector3 | 0, 0, 0 | Rotation (Euler degrees) |
| Scale | Vector3 | 1, 1, 1 | Scale factor |

## Conversion Process

### Step 1: Apply Scale
- **Description**: Multiply input by scale
- **Blender Input**: Vector, Scale
- **Unity Nodes**: Multiply (or Tiling)
- **Formula**: vector * scale

### Step 2: Apply Rotation
- **Description**: Apply rotation to scaled vector
- **Blender Input**: Scaled vector, Rotation
- **Unity Nodes**: Rotate
- **Formula**: rotate(scaled_vector, rotation)

### Step 3: Apply Location
- **Description**: Add location offset
- **Blender Input**: Rotated vector, Location
- **Unity Nodes**: Add (or Offset in TilingAndOffset)
- **Formula**: rotated_vector + location

## Unity Connections

### Simple 2D UV Mapping (Tiling And Offset)
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Vector (UV)      ──►     UV                   Tiling And Offset
Location         ──►     Offset               │
Scale            ──►     Tiling              │
                                           │
                                           ▼
                                      Out ──► [Output]
```

### Full 3D Mapping (Node Chain)
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Vector          ──►     A                    Multiply
Scale          ──►     B                    │
                           │                │
                           ▼                ▼
                      Out ─────►     In    Rotate
                                      │
                              Angle (rotation[2])
                                      │
                                      ▼
                                 Out ─────►     A    Add
                                                  │
                                          Location
                                                  │
                                                  ▼
                                             Out ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| UV | Vector2 | 0,0 | Input UV coordinates |
| Tiling | Vector2 | 1,1 | Scale factor |
| Offset | Vector2 | 0,0 | Translation offset |
| Center | Vector2 | 0.5,0.5 | Rotation center |
| Rotation | Float | 0 | Rotation in degrees |

## Build Instructions

### For 2D UV Coordinates
1. Create Tiling And Offset node (UV > Tiling And Offset)
2. Connect UV to the node
3. Set Offset for Location (X, Y)
4. Set Tiling for Scale (X, Y)

### For Full 3D Vector Transformation
1. Create Multiply node - connect Vector and Scale
2. Create Rotate node - connect scaled vector
3. Create Add node - connect rotated vector and Location
4. Note: Rotation requires conversion from degrees to radians

### Using Subgraph (Recommended)
1. Import `Subgraphs/Vector/Mapping.shadersubgraph` from blender-nodes-for-unity3d
2. Use the subgraph node directly
3. Set Location, Rotation, Scale properties

## Visual Graph Layout

```
// Basic UV Transform (location + scale only)
[UV] ──> [Tiling And Offset] ──> [Output]
              ^                    ^
              │                    │
[Tiling: 2,2] │                    │
[Offset: 0.5, 0] ─────────────────┘

// Full Transform with Rotation
[UV] ──> [Rotate] ──> [Tiling And Offset] ──> [Output]
    ^       ^                   ^
    │       │                   │
    │  [Angle: 45°] ────────────┤
    │
[Default UV] ───────────────────┘

// 3D Rotation requires Custom Function
[UV] ──> [Custom Function: 3D Rotation] ──> [Output]
         (rotation matrix for X, Y, Z)
```

## Pseudocode for Conversion Logic

```python
def convert_mapping_node(blender_node):
    """
    Converts Blender ShaderNodeMapping to Unity ShaderGraph nodes.
    Near conversion - basic Location/Scale work directly, Rotation requires extra nodes.
    """
    # 1. Get inputs
    vector_input = get_input_connection(blender_node.inputs["Vector"])
    location = blender_node.inputs["Location"].default_value  # Vector3
    rotation = blender_node.inputs["Rotation"].default_value  # Vector3 (degrees)
    scale = blender_node.inputs["Scale"].default_value  # Vector3
    
    # 2. Use Unity's Tiling And Offset for Location and Scale
    tiling_offset = create_shadergraph_node("Tiling And Offset")
    
    # Connect UV input
    if vector_input:
        connect_nodes(vector_input, tiling_offset, "UV")
    else:
        # Use default UV
        default_uv = create_shadergraph_node("UV")
        connect_nodes(default_uv, tiling_offset, "UV")
    
    # 3. Set Tiling (Scale)
    tiling_offset.set_property("Tiling", (scale[0], scale[1]))
    
    # 4. Set Offset (Location) - Note: Blender uses different coordinate system
    # Blender: Location is direct offset
    # Unity: Offset is subtracted
    tiling_offset.set_property("Offset", (-location[0], -location[1]))
    
    result = tiling_offset
    
    # 5. Handle Rotation (X, Y, Z in degrees)
    has_rotation = (rotation[0] != 0 or rotation[1] != 0 or rotation[2] != 0)
    
    if has_rotation:
        # Need to create rotation nodes
        # Unity doesn't have 3D rotation for UVs - need Custom Function
        
        if rotation[2] != 0:  # Z-axis rotation (most common for 2D UVs)
            # Use Unity's Rotate node for Z-axis
            rotate_node = create_shadergraph_node("Rotate")
            rotate_node.set_property("unit", "Degrees")
            rotate_node.set_property("angle", rotation[2])
            
            # Connect: Tiling_Offset output -> Rotate input
            connect_nodes(tiling_offset.outputs["UV"], rotate_node, "UV")
            result = rotate_node
        
        # For X/Y rotation (3D texture mapping)
        if rotation[0] != 0 or rotation[1] != 0:
            # Need Custom Function for 3D rotation
            log_warning(
                "Mapping: 3D rotation (X/Y axes) requires Custom Function node. "
                "Using 2D rotation only."
            )
            
            if rotation[2] == 0:
                # No Z rotation, need to add one
                result = _create_2d_rotation(tiling_offset, rotation[0], rotation[1])
    
    return result


def _create_2d_rotation(uv_input, rot_x, rot_y):
    """Create 2D rotation from X and Y rotation values"""
    # Calculate combined angle
    import math
    angle = math.degrees(math.atan2(rot_y, rot_x))
    
    rotate_node = create_shadergraph_node("Rotate")
    rotate_node.set_property("unit", "Degrees")
    rotate_node.set_property("angle", angle)
    
    connect_nodes(uv_input.outputs["UV"], rotate_node, "UV")
    return rotate_node
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Vector/Mapping.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeMapping/Procedural-UV-AutoScroll.ShaderGraph` | Example shader |
| `data/custom_nodes/examples/ShaderNodeMapping/Procedural-UV-OffsetPingPong.ShaderGraph` | Example shader |
| `data/custom_nodes/examples/ShaderNodeMapping/Procedural-UV-Warped.ShaderGraph` | Example shader |

## Notes
- Unity's Tiling and Offset handles Location and Scale directly
- 3D rotation requires custom function or rotation matrix nodes
- For best results: use custom function for full 3D transformation
- Unity typically uses 2D UV, but can work with 3D for projections
- Z-axis rotation works directly with Unity's Rotate node
- X/Y rotation not fully supported in standard ShaderGraph
