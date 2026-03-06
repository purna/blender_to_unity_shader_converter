# ShaderNodeObjectInfo

## Conversion Type: 4 (No Conversion - Limited)

## Overview
- **Blender Node**: ShaderNodeObjectInfo
- **Category**: Input
- **Compatibility**: 30%

## Unity Equivalent
- **Partial**: Object position available
- **None**: Random ID, particle info not available

## Conversion Process

### Step 1: Map Available Attributes
- **Description**: Connect available object attributes
- **Blender Output**: Location, Random
- **Unity Output**: Object position

### Step 2: Handle Unavailable Attributes
- **Description**: Log warning for unavailable attributes
- **Blender Output**: Random ID, etc.
- **Unity Output**: Not available

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Location | Position (Object Space) | 80% |
| Random | Not available | 0% |
| Index | Not available | 0% |

## Visual Graph Layout

```
// Available - Object Position
[Position: Object] ──> [Shader Input]

// Not available
// - Random Object ID
// - Object Index
```

## Pseudocode for Conversion Logic

```python
def convert_objectinfo_node(blender_node):
    """
    Converts Blender ShaderNodeObjectInfo to Unity ShaderGraph nodes.
    Partial conversion - only object position available.
    """
    outputs = {}
    
    # Get the attribute being accessed
    attribute = blender_node.info  # 'LOCATION', 'RANDOM', 'INDEX', etc.
    
    if attribute == 'LOCATION':
        # Object location
        position_node = create_shadergraph_node("Position")
        position_node.set_property("space", "Object")
        outputs["Location"] = position_node.outputs["Position"]
    
    else:
        # Attributes not available in Unity
        log_error(
            f"ObjectInfo attribute '{attribute}' is not available in Unity ShaderGraph. "
            f"Only Location (Object Position) is available."
        )
        return None
    
    return outputs
```

## Compatibility Notes
- 30% compatible
- Only location/position is available

## Limitations
- Random ID not available in Unity shaders
- Object index not available
- Many Blender-specific object attributes not in Unity
