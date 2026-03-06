# Blender to Unity: ShaderNodeAmbientOcclusion Conversion Guide

## ✅ SOLUTION FOUND!

**Unity ShaderGraph HAS a built-in Ambient Occlusion node!**

Reference: https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Ambient-Node.html

## Overview
- **Blender Node**: `ShaderNodeAmbientOcclusion`
- **Unity ShaderGraph Equivalent**: **Ambient Occlusion Node (built-in!)**
- **Category**: Input / Rendering
- **Compatibility**: 75%

## Unity's Ambient Occlusion Node

Unity ShaderGraph includes a native **Ambient Occlusion** node that provides:
- Baked ambient occlusion from lightmapping
- Screen space ambient occlusion (SSAO)

## Conversion

### Step 1: Add Ambient Occlusion Node
In Unity ShaderGraph:
1. Right-click → Add Node
2. Search for "Ambient Occlusion"
3. Add the node

### Step 2: Connect to Your Shader
```
[Ambient Occlusion] → [Multiply] → [Base Color/PBR Master]
```

## Differences

| Blender AO | Unity AO Node |
|------------|---------------|
| Real-time ray tracing | Baked or SSAO |
| Scene-dependent | Requires lightmapping/SSAO |
| Cycles/Eevee feature | Built-in ShaderGraph node |

## Post-Processing Alternative

For real-time AO without baking:
- **URP**: Add Screen Space Ambient Occlusion renderer feature
- **HDRP**: Use Volume settings for AO

These are global post-processing effects, not material-specific.
