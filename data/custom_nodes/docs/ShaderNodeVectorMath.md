# ShaderNodeVectorMath

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeVectorMath
- **Category**: Vector
- **Complexity**: Medium-High
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
Various Shader Graph math nodes

## Unity Shader Graph Nodes

### Primary Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Add](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Add-Node.html) | Math/Basic | Vector addition |
| [Subtract](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Subtract-Node.html) | Math/Basic | Vector subtraction |
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Vector multiplication |
| [Divide](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Divide-Node.html) | Math/Basic | Vector division |
| [Dot Product](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Dot-Product-Node.html) | Math/Vector | Dot product |
| [Cross Product](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Cross-Product-Node.html) | Math/Vector | Cross product |
| [Distance](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Distance-Node.html) | Math/Vector | Distance between vectors |
| [Length](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Length-Node.html) | Math/Vector | Vector length |
| [Normalize](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Normalize-Node.html) | Math/Vector | Normalize vector |
| [Reflect](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Reflect-Node.html) | Math/Vector | Reflect vector |

### Complex Operations (Require Custom Implementation)
| Unity Node | Category | Description |
|------------|----------|-------------|
| Code Function | Utilities | Custom HLSL for Project |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Vector1 | Vector3 | 0, 0, 0 | First input vector |
| Vector2 | Vector3 | 0, 0, 0 | Second input vector |
| Vector3 | Vector3 | 0, 0, 0 | Third input vector (for specific ops) |
| Scale | Float | 1.0 | Scalar scale factor |
| Operation | Enum | Add | Math operation to perform |

## Supported Operations

| Blender Operation | Unity Node | Unity Socket | Formula | Compatibility |
|------------------|------------|--------------|---------|---------------|
| Add | Add | A, B | Vector1 + Vector2 | 100% |
| Subtract | Subtract | A, B | Vector1 - Vector2 | 100% |
| Multiply | Multiply | A, B | Vector1 * Vector2 | 100% |
| Divide | Divide | A, B | Vector1 / Vector2 | 100% |
| Cross Product | Cross Product | A, B | cross(Vector1, Vector2) | 100% |
| Dot Product | Dot Product | A, B | dot(Vector1, Vector2) | 100% |
| Distance | Distance | A, B | distance(Vector1, Vector2) | 100% |
| Length | Length | In | length(Vector1) | 100% |
| Normalize | Normalize | In | normalize(Vector1) | 100% |
| Reflect | Reflect | In, Normal | reflect(Vector1, Vector2) | 100% |
| Project | Code Function | - | dot(v1,v2)/dot(v2,v2)*v2 | 100% |
| Scale | Multiply | A, B | Vector1 * Scale | 100% |

## Conversion Process

### Step 1: Identify Operation
- **Description**: Get the operation type from Blender node
- **Blender Input**: Operation enum
- **Unity Output**: Determine Unity node type

### Step 2: Create Unity Node
- **Description**: Create the corresponding Unity math node
- **Blender Input**: Operation
- **Unity Output**: Math node

### Step 3: Connect Inputs
- **Description**: Connect vectors to node inputs
- **Blender Input**: Vector1, Vector2
**: Wired node

## Unity Connections

```
Blender Socket- **Unity Output          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Vector1         ──►     A                    [Vector Math Node]
Vector2         ──►     B                    │
                           │                │
                           ▼                ▼
                      Out ───────────► [Output]
```

### Example: Dot Product
```
Vector1 (XYZ)    ──►     A                    Dot Product
Vector2 (XYZ)    ──►     B                    │
                                             ▼
                                        Out (Float) ──► [Output]
```

### Example: Cross Product
```
Vector1 (XYZ)    ──►     A                    Cross Product
Vector2 (XYZ)    ──►     B                    │
                                             ▼
                                        Out (XYZ) ──► [Output]
```

### Example: Normalize
```
Vector1 (XYZ)    ──►     In                   Normalize
                                             │
                                             ▼
                                        Out (XYZ) ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| A | Vector3 | 0,0,0 | First input |
| B | Vector3 | 0,0,0 | Second input |
| In | Vector3 | 0,0,0 | Single input |
| Normal | Vector3 | 0,0,1 | Normal for reflection |

## Build Instructions

### Option 1: Use Existing Subgraph (RECOMMENDED)
1. Import `BlenderVectorMath.shadersubgraph` from blender-nodes-for-unity3d package
2. Use the subgraph node directly in your shader
3. Connect vectors to input ports
4. Select operation via dropdown

### Option 2: Build Manually Using Native Nodes
1. Create Vector1 (Vector3 Property)
2. Create Vector2 (Vector3 Property)
3. Create Add/Subtract/Multiply/Divide node as needed
4. Connect vectors to appropriate sockets

### Option 3: Operation Selector Logic
1. Create Operation (Integer Property)
2. Use Branch nodes to select operation based on integer
3. Route to appropriate math node

## Visual Graph Layout

```
// Vector Addition
[Vector3: 1,0,0] ────────────┐
                               ├─> [Add] ──> [Output: 2,0,0]
[Vector3: 1,0,0] ────────────┘

// Vector Length
[Vector3: 3,4,0] ──> [Length] ──> [Output: 5]

// Dot Product
[Vector3: 1,0,0] ──┬─> [Dot Product] ──> [Output: 1]
[Vector3: 1,0,0] ──┘

// Cross Product
[Vector3: 1,0,0] ──┬─> [Cross Product] ──> [Output: 0,0,1]
[Vector3: 0,1,0] ──┘
```

## Pseudocode for Conversion Logic

```python
def convert_vector_math_node(blender_node):
    """
    Converts Blender ShaderNodeVectorMath to Unity ShaderGraph nodes.
    """
    # 1. Get operation
    operation = blender_node.operation
    
    # 2. Get vectors
    vector1_input = get_input_connection(blender_node.inputs["Vector1"])
    vector2_input = get_input_connection(blender_node.inputs["Vector2"])
    
    # 3. Map operation to Unity node
    if operation == "ADD":
        node = create_shadergraph_node("Add")
    elif operation == "SUBTRACT":
        node = create_shadergraph_node("Subtract")
    elif operation == "MULTIPLY":
        node = create_shadergraph_node("Multiply")
    elif operation == "DIVIDE":
        node = create_shadergraph_node("Divide")
    elif operation == "DOT_PRODUCT":
        node = create_shadergraph_node("DotProduct")
    elif operation == "CROSS_PRODUCT":
        node = create_shadergraph_node("CrossProduct")
    elif operation == "DISTANCE":
        node = create_shadergraph_node("Distance")
    elif operation == "LENGTH":
        node = create_shadergraph_node("Length")
    elif operation == "NORMALIZE":
        node = create_shadergraph_node("Normalize")
    elif operation == "REFLECT":
        node = create_shadergraph_node("Reflect")
    # ... etc
    
    # 4. Connect inputs
    if vector1_input:
        connect_nodes(vector1_input, node, "A")
    if vector2_input:
        connect_nodes(vector2_input, node, "B")
    
    return node
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Converter/BlenderVectorMath.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeVectorMath/Sine Vertex Displacement.shader` | Example shader |

## Notes
- Perfect 1:1 mapping for most operations
- Complex operations like Project require custom HLSL
- Recommended to use pre-built subgraph from blender-nodes-for-unity3d
- All vector operations can be recreated in Unity
