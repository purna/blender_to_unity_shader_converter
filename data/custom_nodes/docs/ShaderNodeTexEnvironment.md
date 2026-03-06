# ShaderNodeTexEnvironment - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 90%

## Blender Node Description
Environment texture - loads HDR or image as environment/IBL lighting.

## Unity Equivalent
- **Primary**: HDRI / Environment Texture
- **Implementation**: Use Unity's Environment Lighting

## Conversion Process

### Step 1: Load Environment Map
- Import HDR/EXR image to Unity
- Use as Skybox or Reflection Probe

### Step 2: Configure Lighting
- Set up Environment Lighting
- Use for ambient/IBL

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Texture | Direct |
| Vector | Vector | Not used | N/A |

## Compatibility Notes
- 90% compatible - image loading works
- HDR format support varies

## Limitations
- Not a real-time texture node in Unity
- Requires manual setup in Unity
