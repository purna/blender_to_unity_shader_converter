# ShaderNodeMapRange

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeMapRange
- **Category**: Converter
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP

## Unity Equivalent
- **Primary**: Remap node
- **Alternative**: Multiply/Add chain

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Remap](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Remap-Node.html) | Math/Interpolation | Remaps value from input range to output range |

### Alternative Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Scale for range conversion |
| [Add](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Add-Node.html) | Math/Basic | Offset for range conversion |
| [Subtract](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Subtract-Node.html) | Math/Basic | Offset for range conversion |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Value | Float | 0.0 | Input value to remap |
| From Min | Float | 0.0 | Input minimum |
| From Max | Float | 1.0 | Input maximum |
| To Min | Float | 0.0 | Output minimum |
| To Max | Float | 1.0 | Output maximum |

## Conversion Process

### Step 1: Set Range
- **Description**: Define input and output ranges
- **Blender Input**: From Min, From Max, To Min, To Max
- **Unity Output**: Remapped value

### Step 2: Apply Remap
- **Description**: Map value from source to target range
- **Blender Input**: Value
- **Unity Output**: Remapped value

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Value           ──►     In                    Remap
From Min        ──►     InMin                │
From Max        ──►     InMax                │
To Min         ──►     OutMin               │
To Max         ──►     OutMax               │
                                           │
                                           ▼
                                      Out ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| In | Float | 0 | Input value |
| InMin | Float | 0 | Input minimum |
| InMax | Float | 1 | Input maximum |
| OutMin | Float | 0 | Output minimum |
| OutMax | Float | 1 | Output maximum |

## Visual Graph Layout

```
// Basic Map Range
[Value] ──> [Map Range] ──> [Output]
              ^   ^   ^   ^
              │   │   │   │
         [From Min] [From Max] [To Min] [To Max]

// Using Remap (simpler)
[Value] ──> [Remap: From Min, From Max, To Min, To Max] ──> [Output]

// Manual implementation (Multiply/Add chain)
// Formula: output = (input - fromMin) * ((toMax - toMin) / (fromMax - fromMin)) + toMin
[Value] ──> [Subtract: From Min] ──> [Multiply: Scale] ──> [Add: To Min] ──> [Output]
                 ^                           ^                        ^
                 │                           │                        │
           [From Min]              [(ToMax-ToMin)/(FromMax-FromMin)]  [To Min]
```

## Pseudocode for Conversion Logic

```python
def convert_maprange_node(blender_node):
    """
    Converts Blender ShaderNodeMapRange to Unity ShaderGraph Remap/Map Range.
    1-1 direct mapping - value remapping between ranges.
    """
    # 1. Get range parameters
    from_min = blender_node.inputs["From Min"].default_value
    from_max = blender_node.inputs["From Max"].default_value
    to_min = blender_node.inputs["To Min"].default_value
    to_max = blender_node.inputs["To Max"].default_value
    
    # 2. Get interpolation mode
    # Blender: 'LINEAR', 'SMOOTH', 'SMOOTHER'
    # Unity: Linear, Smooth
    blend_mode = blender_node.interpolation
    
    # 3. Create Remap node
    # Unity Remap: Remap(In, InMin, InMax OutMax)
    remap_node = create_shadergraph_node("Remap")
    
    # 4. Get input value
    value_input = get_input_connection(blender_node.inputs[0])  # Value
    
    if value_input:
        connect_nodes(value_input, remap_node, "In")
    else:
        remap_node.set_input("In", blender_node.inputs[0].default_value)
    
    # 5. Set range values
    remap_node.set_input("InMin", from_min)
    remap_node.set_input("InMax", from_max)
    remap_node.set_input("OutMin", to_min)
    remap_node.set_input("OutMax", to_max)
    
    # Note: Unity Remap doesn't have smooth modes like Blender
    # For SMOOTH/SMOOTHER, would need additional nodes
    
    return remap_node.outputs["Out"]
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Converter/MapRange.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeMapRange/Procedural-Color-PingPong.ShaderGraph` | Example shader |
| `data/custom_nodes/examples/ShaderNodeMapRange/Procedural-UV-OffsetPingPong.ShaderGraph` | Example shader |

## Compatibility Notes
- 100% compatible for basic linear remap
- Smooth/Smoother interpolation requires extra nodes

## Limitations
- Unity Remap is always linear
- Smooth interpolation needs approximation
