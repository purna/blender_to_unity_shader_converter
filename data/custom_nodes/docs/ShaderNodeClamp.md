# ShaderNodeClamp

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Utility
- **Compatibility**: 100%

## Example
See example: `data/custom_nodes/examples/Converter/BlenderMath.shadersubgraph`

## Blender Node Description
Clamps value to range. Direct mathematical operation with minimum and maximum bounds.

## Unity Equivalent
- **Primary**: Clamp node
- **Implementation**: 1:1 direct mapping

## Conversion Process

### Step 1: Create Clamp Node
- Add Clamp node in Unity

### Step 2: Connect Value
- Connect Value input

### Step 3: Set Bounds
- Set Min and Max values

## Parameters

| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Value | Float | In | Direct |
| Min | Float | Min | Direct |
| Max | Float | Max | Direct |

## Visual Graph Layout

```
// Basic Clamp
[Value] ──> [Clamp] ──> [Output]
              ^   ^
              │   │
         [Min: 0] [Max: 1]

// Dynamic Clamp with inputs
[Value] ──> [Clamp] ──> [Output]
              ^   ^   ^
              │   │   │
[Dynamic Min]┘   │   │
              [Dynamic Max] ┘
```

## Pseudocode for Conversion Logic

```python
def convert_clamp_node(blender_node):
    """
    Converts Blender ShaderNodeClamp to Unity ShaderGraph Clamp node.
    1-1 direct mapping - perfect compatibility.
    """
    # 1. Create Unity Clamp node
    unity_clamp = create_shadergraph_node("Clamp")
    
    # 2. Get inputs
    value_input = get_input_connection(blender_node.inputs["Value"])
    min_input = get_input_connection(blender_node.inputs["Min"])
    max_input = get_input_connection(blender_node.inputs["Max"])
    
    # 3. Get default values
    min_default = blender_node.inputs["Min"].default_value
    max_default = blender_node.inputs["Max"].default_value
    
    # 4. Connect or set Value
    if value_input:
        connect_nodes(value_input, unity_clamp, "In")
    else:
        unity_clamp.set_input("In", blender_node.inputs["Value"].default_value)
    
    # 5. Connect or set Min
    if min_input:
        connect_nodes(min_input, unity_clamp, "Min")
    else:
        unity_clamp.set_input("Min", min_default)
    
    # 6. Connect or set Max
    if max_input:
        connect_nodes(max_input, unity_clamp, "Max")
    else:
        unity_clamp.set_input("Max", max_default)
    
    return unity_clamp
```

## Compatibility Notes
- 100% compatible - direct 1:1 mapping
- No limitations

## Limitations
- None
