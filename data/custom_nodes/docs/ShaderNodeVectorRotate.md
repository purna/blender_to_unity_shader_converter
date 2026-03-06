# Vector Rotate Node

## Overview
The Vector Rotate node rotates a vector around a specified axis by a given angle. It supports various rotation types including Axis-Angle, Euler, and Quaternion.

## Blender Node Inputs
- **Vector**: Input vector to rotate
- **Center**: Rotation center point
- **Axis**: Rotation axis (X, Y, or Z)
- **Angle**: Rotation angle in radians
- **Euler**: Rotation as Euler angles (for Euler type)
- **Axis X/Y/Z**: Axis vector components (for Axis-Angle type)
- **Quaternion**: Rotation as Quaternion (for Quaternion type)

## Blender Node Outputs
- **Vector**: Rotated output vector

## Rotation Types

| Type | Description | Unity Equivalent |
|------|-------------|------------------|
| Axis Angle | Rotate around arbitrary axis | Custom rotation matrix |
| Euler | Rotate using Euler angles (XYZ, XZY, YXZ, YZX, ZXY, ZYX) | Rotate Node |
| Quaternion | Rotate using quaternion | Custom implementation |

## Unity Equivalent

### Option 1: Rotate Node (Limited)
Unity Shader Graph has a "Rotate" node but it's limited:
- Only rotates around Z-axis by default
- Requires custom implementation for arbitrary axes

### Option 2: Custom Rotation Matrix
Create rotation matrices for each axis type:

```hlsl
// Rotate around X axis by angle
float3 RotateX(float3 v, float angle)
{
    float s = sin(angle);
    float c = cos(angle);
    float3x3 rotX = float3x3(
        1, 0, 0,
        0, c, -s,
        0, s, c
    );
    return mul(rotX, v);
}

// Rotate around Y axis by angle
float3 RotateY(float3 v, float angle)
{
    float s = sin(angle);
    float c = cos(angle);
    float3x3 rotY = float3x3(
        c, 0, s,
        0, 1, 0,
        -s, 0, c
    );
    return mul(rotY, v);
}

// Rotate around Z axis by angle
float3 RotateZ(float3 v, float angle)
{
    float s = sin(angle);
    float c = cos(angle);
    float3x3 rotZ = float3x3(
        c, -s, 0,
        s, c, 0,
        0, 0, 1
    );
    return mul(rotZ, v);
}
```

### Option 3: Arbitrary Axis Rotation
```hlsl
// Rotate around arbitrary axis
float3 RotateAroundAxis(float3 v, float3 axis, float angle)
{
    float s = sin(angle);
    float c = cos(angle);
    float t = 1 - c;
    float3x3 rot = float3x3(
        t * axis.x * axis.x + c,       t * axis.x * axis.y - s * axis.z,  t * axis.x * axis.z + s * axis.y,
        t * axis.x * axis.y + s * axis.z, t * axis.y * axis.y + c,         t * axis.y * axis.z - s * axis.x,
        t * axis.x * axis.z - s * axis.y,  t * axis.y * axis.z + s * axis.x, t * axis.z * axis.z + c
    );
    return mul(rot, v);
}
```

### Option 4: Euler Angles to Rotation Matrix
```hlsl
float3 RotateByEuler(float3 v, float3 euler)
{
    // Convert degrees to radians
    float3 rad = euler * 3.14159 / 180.0;
    return RotateZ(RotateY(RotateX(v, rad.x), rad.y), rad.z);
}
```

## Conversion Strategy

### Simple Rotations (X/Y/Z Axis)
1. Use built-in Rotate node in Shader Graph (around Z)
2. For X/Y axis: create custom RotateX/RotateY functions

### Complex Rotations (Arbitrary Axis)
1. Add custom HLSL function to Shader Graph
2. Use Code Function Node or custom shader
3. Pass axis and angle as properties

### Quaternion Rotations
Convert quaternion to rotation matrix:
```hlsl
float3 RotateByQuat(float3 v, float4 q)
{
    // Convert quaternion to rotation matrix
    float3 u = q.xyz;
    float s = q.w;
    return 2.0 * dot(u, v) * u + (s*s - dot(u, u)) * v + 2.0 * s * cross(u, v);
}
```

## Compatibility
- **Compatibility**: 80%
- **Notes**: Most common rotations (X/Y/Z) can be recreated. Arbitrary axis requires custom shader code.

## Additional Resources
- [Rotation Matrix Wikipedia](https://en.wikipedia.org/wiki/Rotation_matrix)
- [Unity Shader Graph Rotate Node](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Rotate-About-Axis-Node.html)
- [Blender Vector Rotate Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/vector_rotate.html)
