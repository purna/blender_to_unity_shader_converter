# Vector Curve Node

## Overview
The Vector Curve node applies a curve adjustment to each vector component (X, Y, Z) independently. It allows for non-linear transformations of vector values.

## Blender Node Inputs
- **Vector**: Input vector (XYZ)
- **X Channel**: Curve control points for X component
- **Y Channel**: Curve control points for Y component  
- **Z Channel**: Curve control points for Z component

## Blender Node Outputs
- **Vector**: Curved/adjusted vector

## Unity Equivalent

### Primary Option: Spline-Based Custom Node
Unity Shader Graph doesn't have a direct Vector Curve equivalent. Options include:

1. **Three Separate Float Curves**
   - Use three Float properties with curve editing
   - Apply individually to each vector component

2. **Custom Code Function Node**
   - Implement Bezier curve evaluation in HLSL
   - Add as custom node in Shader Graph

### Curve Implementation in HLSL
```hlsl
// Bezier curve evaluation
float EvaluateCurve(float t, float4 p0, float4 p1, float4 p2, float4 p3)
{
    float u = 1 - t;
    float tt = t * t;
    float uu = u * u;
    float uuu = uu * u;
    float ttt = tt * t;
    
    return uuu * p0 + 3 * uu * t * p1 + 3 * u * tt * p2 + ttt * p3;
}

// Simple cubic interpolation
float CubicCurve(float t, float4 controlPoints)
{
    float t2 = t * t;
    float t3 = t2 * t;
    return controlPoints.x + 
           controlPoints.y * t + 
           controlPoints.z * t2 + 
           controlPoints.w * t3;
}
```

## Conversion Strategy

### Simple Curves (Linear Approximation)
1. For monotonic curves: use Remap node
2. Connect input through Multiply/Add nodes
3. Approximate with two-point linear interpolation

### Complex Curves (Full Implementation)
1. **Create Custom Node in Shader Graph**:
   - Add "Code Function Node" (requires Shader Graph package)
   - Write HLSL for curve evaluation
   - Expose control points as properties

2. **Alternative: Pre-Baked Texture**:
   - Create gradient texture representing curve
   - Sample texture with vector component as UV
   - Use texture lookup for non-linear mapping

### Implementation Using Texture Lookup
```
1. Create 256x1 gradient texture
2. Map curve values to grayscale (0-1)
3. In shader, sample texture using vector.x as UV.x
4. Repeat for y and z channels
```

## Compatibility
- **Compatibility**: 50%
- **Notes**: Complex curves difficult to replicate exactly. Simple curves can be approximated with Remap.

## Recommendations

### For Simple Non-Linear Adjustments
- Use **Remap** node with non-linear input
- Chain multiple Remap nodes
- Use **Smoothstep** for S-curves

### For Complex Curves
- Implement custom HLSL function
- Use texture-based curve lookup
- Consider baking to texture in Blender first

### Workflow
1. Evaluate curve complexity in Blender
2. For simple curves: approximate with math nodes
3. For complex curves: pre-bake to texture
4. Import texture and use as lookup table

## Additional Resources
- [Blender Vector Curve Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/vector_curve.html)
- [Unity Shader Graph Documentation](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html)
- [Bezier Curve Mathematics](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)
