# ShaderNodeMath

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeMath
- **Category**: Converter
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP

## Unity Equivalent
**Math Node** - All operations map directly 1:1

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Math](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/One-Node-Math-Operator.html) | Math | Universal math node with operation dropdown |

### Individual Operation Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Add](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Add-Node.html) | Math/Basic | Addition |
| [Subtract](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Subtract-Node.html) | Math/Basic | Subtraction |
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Multiplication |
| [Divide](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Divide-Node.html) | Math/Basic | Division |
| [Power](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Power-Node.html) | Math/Exponential | Power/Exponent |
| [Square Root](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Square-Root-Node.html) | Math/Exponential | Square root |
| [Absolute](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Absolute-Node.html) | Math/Exponential | Absolute value |
| [Minimum](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Minimum-Node.html) | Math/Interp | Minimum value |
| [Maximum](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Maximum-Node.html) | Math/Interp | Maximum value |
| [Floor](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Floor-Node.html) | Math/Round | Floor value |
| [Ceiling](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Ceiling-Node.html) | Math/Round | Ceiling value |
| [Fraction](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Fraction-Node.html) | Math/Round | Fractional part |
| [Sine](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Sine-Node.html) | Math/Trig | Sine function |
| [Cosine](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Cosine-Node.html) | Math/Trig | Cosine function |
| [Tangent](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Tangent-Node.html) | Math/Trig | Tangent function |
| [Lerp](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Lerp-Node.html) | Math/Interpolation | Linear interpolation |
| [Smoothstep](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Smoothstep-Node.html) | Math/Interpolation | Smooth interpolation |
| [Remap](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Remap-Node.html) | Math/Interpolation | Value remapping |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Value1 (A) | Float/Vector | 0.0 | First input value |
| Value2 (B) | Float/Vector | 0.0 | Second input value |
| Operation | Enum | ADD | Math operation to perform |

## Conversion Process

### Step 1: Direct Operation Mapping
- **Description**: All math operations map directly to Unity Math node
- **Blender Input**: Math operation (Add, Multiply, Divide, etc.)
- **Unity Output**: Same operation in Unity

## Blender to Unity Mapping

| Blender Operation | Unity Node | Unity Socket | Compatibility |
|------------------|------------|--------------|---------------|
| ADD | Add | A, B | 100% |
| SUBTRACT | Subtract | A, B | 100% |
| MULTIPLY | Multiply | A, B | 100% |
| DIVIDE | Divide | A, B | 100% |
| POWER | Power | In, Exp | 100% |
| LOGARITHM | Log | In | 100% |
| SQRT | Square Root | In | 100% |
| ABSOLUTE | Absolute | In | 100% |
| MINIMUM | Minimum | A, B | 100% |
| MAXIMUM | Maximum | A, B | 100% |
| MODULO | Modulo | A, B | 100% |
| FLOOR | Floor | In | 100% |
| CEIL | Ceiling | In | 100% |
| FRACTION | Fraction | In | 100% |
| WRAP | Wrap | In, Min, Max | 100% |
| PINGPONG | Ping Pong | In, Min, Max | 100% |
| SINE | Sine | In | 100% |
| COSINE | Cosine | In | 100% |
| TANGENT | Tangent | In | 100% |
| ARCSINE | Arcsine | In | 100% |
| ARCCOSINE | Arccosine | In | 100% |
| ARCTANGENT | Arctangent | In | 100% |
| ARCTAN2 | Arctan2 | A, B | 100% |
| SMOOTHSTEP | Smoothstep | Edge0, Edge1, In | 100% |
| STEP | Step | Edge, In | 100% |
| LERP | Lerp | T, A, B | 100% |
| INVERSELERP | Inverse Lerp | T, A, B | 100% |
| REMAP | Remap | In, InMin, InMax, OutMin, OutMax | 100% |

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Value1          ──►     A (or In)           [Math Node]
Value2          ──►     B                    │
                           │                │
                           ▼                ▼
                      Out ───────────► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| A | Dynamic | 0 | First input |
| B | Dynamic | 0 | Second input |
| Operation | Enum | Add | Math operation |
| Clamp | Boolean | False | Clamp result |

## Build Instructions

1. Create Math node in Unity Shader Graph
2. Set Operation property to match Blender
3. Connect Value1 and Value2 inputs
4. Connect output to destination

## Visual Graph Layout

```
// Example: Adding two values
[Float Node: 5.0] ──────────────┐
                                  ├─> [Add] ──> [Output]
[Float Node: 3.0] ──────────────┘

// Example: Multiply with Clamp
[Color Node] ──> [Multiply] ──> [Clamp: 0-1] ──> [Output]
                  ^
                  │
[Float Node: 2.0] ┘
```

## Pseudocode for Conversion Logic

```python
def convert_math_node(blender_node):
    """
    Converts Blender ShaderNodeMath to Unity ShaderGraph Math node.
    This is a 1-1 direct mapping for all operations.
    """
    # 1. Get the operation type from Blender
    blender_operation = blender_node.operation  # e.g., 'ADD', 'MULTIPLY', etc.
    
    # 2. Map Blender operation to Unity operation
    operation_mapping = {
        'ADD': 'Add',
        'SUBTRACT': 'Subtract',
        'MULTIPLY': 'Multiply',
        'DIVIDE': 'Divide',
        'POWER': 'Power',
        'LOGARITHM': 'Log',
        'SQRT': 'SquareRoot',
        'ABSOLUTE': 'Absolute',
        'MINIMUM': 'Minimum',
        'MAXIMUM': 'Maximum',
        'MODULO': 'Modulo',
        'FLOOR': 'Floor',
        'CEIL': 'Ceiling',
        'FRACTION': 'Fraction'
    }
    
    unity_operation = operation_mapping.get(blender_operation)
    
    # 3. Create Unity Math node
    unity_math_node = create_shadergraph_node("Math", {
        "operation": unity_operation
    })
    
    # 4. Get input connections from Blender
    input1 = get_input_connection(blender_node.inputs[0])
    input2 = get_input_connection(blender_node.inputs[1])
    
    # 5. Connect inputs to Unity node
    if input1:
        connect_nodes(input1, unity_math_node, "A")
    if input2:
        connect_nodes(input2, unity_math_node, "B")
    
    # 6. Handle 'Use Clamp' option if present
    if blender_node.use_clamp:
        unity_math_node.set_property("clamp", True)
    
    return unity_math_node
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Converter/BlenderMath.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeMath/Scrolling Texture Cutout.shader` | Example shader |
| `data/custom_nodes/examples/ShaderNodeMath/Sine Vertex Displacement.shader` | Example shader |

## Notes
- Perfect 1:1 mapping for all operations
- Direct port to Unity Math node
- Use Clamp option if needed
