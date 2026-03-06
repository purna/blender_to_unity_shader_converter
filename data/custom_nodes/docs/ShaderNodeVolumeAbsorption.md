# Volume Absorption Node

## Overview
The Volume Absorption node simulates the absorption of light as it passes through a volume. It's commonly used for colored glass, liquids, and atmospheric effects.

## Blender Node Inputs
- **Color**: Absorption color (RGB)
- **Density**: Volume density (higher = more absorption)
- **Anisotropy**: Not applicable for pure absorption
- **Volume**: Input volume shader (for chaining)

## Blender Node Outputs
- **Volume**: Shader output for volume

## Unity Equivalent

### The Challenge
Standard Unity rendering doesn't support volumetric absorption in the built-in pipeline. Options vary by render pipeline:

### Option 1: HDRP (High Definition Render Pipeline)
HDRP supports volumetric absorption natively:
- Enable "Volumetric" in Frame Settings
- Use "Refraction" with absorption
- Create custom volume for fog/absorption

### Option 2: URP (Universal Render Pipeline)
URP has limited volume support:
- Use Shader Graph's "Volume" master (URP 14+)
- Implement custom raymarching shader
- Use post-processing for screen-space effects

### Option 3: Custom Shader Implementation
Create a volume absorption shader:

```hlsl
// Volume Absorption Shader (Raymarching)
Shader "Custom/VolumeAbsorption"
{
    Properties
    {
        _Color ("Absorption Color", Color) = (1,1,1,1)
        _Density ("Density", Range(0, 10)) = 1
        _MaxDistance ("Max Distance", Range(0, 100)) = 10
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
            float _MaxDistance;
            
            struct appdata {
                float4 vertex : POSITION;
            };
            
            struct v2f {
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD0;
            };
            
            v2f vert(appdata v) {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                return o;
            }
            
            float4 frag(v2f i) : SV_Target {
                float3 viewDir = normalize(i.worldPos - _WorldSpaceCameraPos);
                float dist = min(_MaxDistance, length(i.worldPos - _WorldSpaceCameraPos));
                
                // Beer-Lambert law for absorption
                float absorption = exp(-_Density * dist);
                float3 color = _Color.rgb * (1 - absorption);
                
                return float4(color, absorption);
            }
            ENDCG
        }
    }
}
```

## Conversion Strategy

### Simple Approach: Transparent Material with Tint
1. Create transparent material
2. Set base color to absorption color
3. Adjust alpha for density effect
4. Use "Fade" or "Transparent" mode

### Advanced Approach: Custom Shader
1. Implement Beer-Lambert absorption
2. Add raymarching for volume depth
3. Connect to depth buffer for proper calculations

### For Colored Glass/Translucent Materials
```
1. Use Standard Shader with:
   - Rendering Mode: Transparent
   - Albedo: Tint color (low alpha)
   - Smoothness: High
   - Transmission: Enabled (if HDRP)
2. Adjust alpha to simulate density
```

## Beer-Lambert Law

The physics behind volume absorption:

```
I = I₀ × e^(-σ × d)

Where:
- I = transmitted light intensity
- I₀ = initial light intensity
- σ = absorption coefficient (related to density)
- d = distance through volume
```

In shader code:
```hlsl
float3 absorption = exp(-density * distance * (1 - absorptionColor));
```

## Compatibility
- **Compatibility**: 0%
- **Notes**: Truly impossible in real-time rendering without raymarching or volume system. Can be approximated with transparent materials but quality is limited.

## Alternative Solutions

### For Glass
- Use Standard/URP PBR with transmission
- Use "Transparent" mode with tint
- Bake transmission to texture for static objects

### For Fog/Atmosphere
- Use Unity's Fog system
- Use Post-Processing Volume Bloom/Color Grading
- Create plane with gradient for ground fog

### For Static Objects
- Bake lighting in Blender
- Export with baked absorption
- Use lightmaps in Unity

## Additional Resources
- [Beer-Lambert Law - Wikipedia](https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law)
- [Unity HDRP Volume System](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@latest/index.html?subfolder=/manual/Volumes.html)
- [URP Volume Master Stack](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/manual/Volume-Master-Stack.html)
- [Blender Volume Absorption Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_absorption.html)
