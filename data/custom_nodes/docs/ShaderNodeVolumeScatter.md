# ShaderNodeVolumeScatter

## Conversion Type: 4 (Incompatible - Requires Custom Solution)

## Overview
- **Blender Node**: ShaderNodeVolumeScatter
- **Category**: Shader
- **Compatibility**: 0%
- **Unity Version**: URP/HDRP
- **Complexity**: Very High (Volumetric)
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
- **HDRP**: HDRP Volumetric Fog
- **URP**: Custom Raymarching or Particles

## The Challenge

Volume scatter requires raymarching or volumetric rendering, which is computationally expensive. Direct conversion is not possible in standard Unity rendering pipelines.

## Unity Shader Graph Nodes

### For HDRP
| Unity Node | Category | Description |
|------------|----------|-------------|
| Volume | Rendering | HDRP Volume component |
| Fog Volume | Volume | Volumetric fog |

### For URP (Alternative Approaches)
| Approach | Description |
|----------|-------------|
| Particle System | Soft particles with scatter color |
| Custom Shader | Raymarching shader |
| Post-Processing | Screen-space fog approximation |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color | Color | 1, 1, 1, 1 | Scattering color |
| Density | Float | 1 | Volume density (0-100) |
| Anisotropy | Float | 0 | Scattering direction bias (-1 to 1) |

## Conversion Process

### Option 1: HDRP Volumetrics
1. Enable "Volumetric Fog" in Frame Settings
2. Create Volume component
3. Add Fog override
4. Configure density and color

### Option 2: URP Particles
1. Create Particle System
2. Enable Soft Particles
3. Apply scatter color to particles
4. Adjust density via emission rate

### Option 3: Custom Raymarching Shader
1. Create custom HLSL shader
2. Implement Henyey-Greenstein phase function
3. Use raymarching loop

## Unity Connections

### Using HDRP Volume
```
[Volume Component]
    │
    ├── Fog (enabled)
    │    ├── Mean Free Path → Density
    │    ├── Tint → Color
    │    └── Anisotropy → Anisotropy
    │
    └── [Scene Objects affected]
```

### Using Custom Shader
```
[Raymarching Shader]
    │
    ├── Properties
    │    ├── _Color (Scatter Color)
    │    ├── _Density (Volume Density)
    │    ├── _Anisotropy (Direction Bias)
    │    └── _MaxDistance (Max Ray Distance)
    │
    └── Output ──► [Transparent Material]
```

## Henyey-Greenstein Phase Function

For anisotropic scattering, use the formula:

```
P(θ) = (1 - g²) / (4π × (1 + g² - 2g×cos(θ))^1.5)

Where:
- θ = angle between light and view direction
- g = anisotropy parameter
  - g = 0: Isotropic (uniform)
  - g > 0: Forward scattering
  - g < 0: Backward scattering
```

## Custom Shader Example

```hlsl
// Volume Scatter Raymarching
Shader "Custom/VolumeScatter"
{
    Properties
    {
        _Color ("Scatter Color", Color) = (1,1,1,1)
        _Density ("Density", Range(0, 10)) = 1
        _Anisotropy ("Anisotropy", Range(-1, 1)) = 0
        _MaxDistance ("Max Distance", Range(0, 100)) = 50
    }
    
    SubShader
    {
        Tags { "Queue"="Transparent" "RenderType"="Transparent" }
        
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            
            float4 _Color;
            float _Density;
            float _Anisotropy;
            float _MaxDistance;
            
            struct appdata {
                float4 vertex : POSITION;
            };
            
            struct v2f {
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 viewDir : TEXCOORD1;
            };
            
            // Henyey-Greenstein phase function
            float HG_Phase(float cosTheta, float g)
            {
                float g2 = g * g;
                return (1 - g2) / (4 * 3.14159 * pow(1 + g2 - 2 * g * cosTheta, 1.5));
            }
            
            v2f vert(appdata v) {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.viewDir = normalize(_WorldSpaceCameraPos - o.worldPos);
                return o;
            }
            
            float4 frag(v2f i) : SV_Target {
                float3 rayDir = -i.viewDir;
                float dist = min(_MaxDistance, length(i.worldPos - _WorldSpaceCameraPos));
                
                // Simple scattering approximation
                float scatter = 1 - exp(-_Density * dist);
                
                // Apply phase function for anisotropy
                float phase = HG_Phase(dot(rayDir, float3(0, 1, 0)), _Anisotropy);
                
                float3 color = _Color.rgb * scatter * phase;
                return float4(color, scatter * _Color.a);
            }
            ENDCG
        }
    }
}
```

## Quick Approximation (Non-Volumetric)

For simple effects without raymarching:

1. Add a large sphere around scene
2. Use transparent material with:
   - Soft particles enabled
   - Gradient texture (dense to transparent)
   - Scatter color with low alpha
3. Adjust scale and position

## Example Approximation Setup

```
[Transparent Material]
    │
    ├── Base Color → Scatter Color
    ├── Alpha → Low value (0.1-0.3)
    ├── Soft Particles → Enabled
    │
    └── [Apply to sphere/plane]
```

## Compatibility
- **Compatibility**: 0%
- **Notes**: Truly impossible in standard real-time rendering. Requires raymarching or volume system. Approximation possible via particles or post-processing.

## Alternative Solutions

### For Real-time Applications
- Use particle systems for localized effects
- Use screen-space fog
- Bake volumetric effects to textures
- Use fog planes with custom shaders

### For High-Quality (HDRP)
- Enable native volumetric fog
- Use raymarching
- Leverage GPU compute

## Limitations
- Volumetric scatter requires HDRP or custom shaders
- Not available in standard URP without custom implementation
- Performance-intensive
- Requires custom raymarching shader for accurate results
