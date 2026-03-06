# White Noise Texture Node

## Overview
The White Noise node generates random values across the texture. Unlike other noise types, it produces completely uncorrelated random values for each point.

## Blender Node Inputs
- **Vector**: Position to generate noise (for deterministic randomness)
- **W**: Noise dimension (2D, 3D, or 4D)

## Blender Node Outputs
- **Value**: Single channel noise value (0-1)

## Unity Equivalent

### Option 1: Simple Random Function
Use a basic random/noise node in Shader Graph:

1. **Random** node (Shader Graph):
   - Input: UV or position vector
   - Output: Random value per pixel

2. **Simple Noise** node:
   - Set scale very high (e.g., 1000)
   - Creates high-frequency noise approaching white noise

### Option 2: Custom White Noise Function
```hlsl
// Simple hash-based white noise
float WhiteNoise(float2 uv)
{
    float2 i = floor(uv);
    float2 f = frac(uv);
    
    float a = frac(sin(dot(i, float2(12.9898, 78.233))) * 43758.5453);
    float b = frac(sin(dot(i + float2(1, 0), float2(12.9898, 78.233))) * 43758.5453);
    float c = frac(sin(dot(i + float2(0, 1), float2(12.9898, 78.233))) * 43758.5453);
    float d = frac(sin(dot(i + float2(1, 1), float2(12.9898, 78.233))) * 43758.5453);
    
    float2 u = f * f * (3 - 2 * f);
    
    return lerp(a, b, u.x) + (c - a) * u.y * (1 - u.x) + (d - b) * u.x * u.y;
}

// 3D White Noise
float3 WhiteNoise3D(float3 pos)
{
    return float3(
        frac(sin(dot(pos, float3(12.9898, 78.233, 45.164))) * 43758.5453),
        frac(sin(dot(pos, float3(93.989, 67.345, 56.182))) * 43758.5453),
        frac(sin(dot(pos, float3(45.33, 98.12, 34.234))) * 43758.5453)
    );
}
```

### Option 3: Gradient Noise at High Scale
Set Simple Noise node to very high scale:
```
1. Add "Simple Noise" node
2. Set Scale to 500-1000
3. Output approaches white noise
4. Adjust contrast if needed
```

## Conversion Strategy

### For Random Values per Pixel
1. Use Shader Graph's **Random** node
2. Input UV coordinates
3. Output: random value per pixel

### For Deterministic Randomness (Seed-based)
1. Create float property for seed
2. Add seed to UV coordinates
3. Pass through Random node

### For Animated White Noise
```
1. Add Time node
2. Combine with UV: UV + Time
3. Pass to Random node
4. Creates flickering white noise
```

## Common Uses

| Use Case | Unity Implementation |
|----------|---------------------|
| Procedural grain | Random node → Multiply → Add to color |
| Dithering | Random node → Dither node |
| Random offset | Random node → Offset texture UVs |
| Stochastic effects | Random node → Branch logic |

## Example: Dithering Effect
```hlsl
float Dither(float2 uv, float intensity)
{
    float noise = WhiteNoise(uv * _ScreenParams.xy);
    return noise > intensity ? 1 : 0;
}
```

## Parameters

| Blender | Description | Unity Equivalent |
|---------|-------------|------------------|
| Vector | Input position | UV / Position input |
| W | Dimension (2D-4D) | Use 2D or 3D function |

## Compatibility
- **Compatibility**: 80%
- **Notes**: Can be approximated with Random node or custom function. Full 4D not available but rarely needed.

## Shader Graph Setup

### Basic Random
```
[Simple Noise Node]
    Scale: 1000
    → [Power Node]
        Power: 10 (increases contrast)
    → Output
```

### With Seed
```
[UV Node] + [Vector] → [Add] → [Random Node] → Output
```

## Additional Resources
- [Unity Shader Graph Random Node](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Random-Noise-Node.html)
- [Hash Functions for Noise](https://www.shadertoy.com/view/4djSRW)
- [Blender White Noise Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/white_noise.html)
