# Vector Transform Node

## Overview
The Vector Transform node converts vectors between different coordinate spaces: Object, World, and View spaces. It also supports transformation between different coordinate systems (Blender to Unity).

## Blender Node Inputs
- **Vector**: Input vector to transform
- **Matrix**: Custom transformation matrix (optional)

## Blender Node Outputs
- **Vector**: Transformed output vector

## Coordinate Spaces

| From/To | Description |
|---------|-------------|
| Object | Local space relative to object |
| World | Global world space |
| View | Camera/view space |
| Tangent | Tangent space (for normal mapping) |

## Unity Coordinate System Differences

### Key Differences
- **Blender**: Right-handed, Z-up
- **Unity**: Left-handed, Y-up
- **Rotation**: 90° around X axis needed for conversion

### Conversion Matrix (Blender → Unity)
```
Unity = RotationX(-90°) × Blender
```

## Unity Equivalent

### Option 1: Transform Node (Partial)
Unity Shader Graph has limited transform capabilities:
- World to Object space (object space to world space)
- Tangent to World space
- View direction

### Option 2: Custom Transformation Matrix
```hlsl
// Transform vector from Blender (Z-up) to Unity (Y-up)
float3 TransformBlenderToUnity(float3 v)
{
    // Rotate -90 degrees around X axis
    return float3(v.x, v.z, -v.y);
}

// Transform vector from Unity (Y-up) to Blender (Z-up)
float3 TransformUnityToBlender(float3 v)
{
    // Rotate +90 degrees around X axis
    return float3(v.x, -v.z, v.y);
}
```

### Option 3: Space Conversion Nodes
Use Shader Graph space conversion:
```
1. Object Space → World Space: Transform Node (Object to World)
2. World Space → View Space: View Direction Node (inverse)
3. Tangent → World: Normal Vector Node (Tangent to World Space)
```

### Option 4: Custom Matrix Multiplication
```hlsl
float3 TransformVector(float3 v, float4x4 matrix)
{
    float4 homogeneous = float4(v, 0);
    float4 transformed = mul(matrix, homogeneous);
    return transformed.xyz;
}

// Unity's model matrix (Object to World)
float4x4 unity_ObjectToWorld;

// Inverse (World to Object)  
float4x4 unity_WorldToObject;
```

## Conversion Strategy

### Simple Space Transforms
1. **Object → World**: Use Transform Node (Object to World)
2. **World → Object**: Use Transform Node (World to Object)
3. **Tangent → World**: Use Normal Vector Node

### Blender to Unity Conversion
1. Add custom rotation matrix
2. Rotate vectors -90° around X axis
3. Convert from Z-up to Y-up

### For Normal Maps
```hlsl
// Transform normal from tangent to world space
float3 TransformNormalToWorld(float3 normal, float3x3 TBN)
{
    return normalize(mul(normal, TBN));
}
```

## Important Notes

### Normal Vectors vs Direction Vectors
- **Normals**: Must use inverse transpose matrix for correct scaling
- **Directions**: Use regular transformation matrix

### Transformation Matrix Setup in Shader
```hlsl
// In Unity shader properties
Properties {
    _MainTex ("Texture", 2D) = "white" {}
}

// Auto-defined Unity matrices
// unity_ObjectToWorld - Object to World transform
// unity_WorldToObject - World to Object transform
// unity_MatrixV - View matrix
// unity_MatrixIV - Inverse view matrix
```

## Compatibility
- **Compatibility**: 70%
- **Notes**: Basic space transforms available. Full matrix control requires custom shader implementation.

## Additional Resources
- [Coordinate Systems - Unity Manual](https://docs.unity3d.com/Manual/class-Transform.html)
- [Unity Shader Graph Transform Node](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Transform-Node.html)
- [Blender Vector Transform Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/vector_transform.html)
- [Right-hand to Left-hand Coordinate Conversion](https://docs.microsoft.com/en-us/windows/win32/direct3d9/coordinate-systems)
