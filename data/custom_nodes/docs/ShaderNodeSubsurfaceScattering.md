# ShaderNodeSubsurfaceScattering

## Overview
- **Blender Node**: ShaderNodeSubsurfaceScattering
- **Category**: Shader
- **Compatibility**: 30%

## Conversion Process

### Step 1: Enable SSS in PBR
- **Description**: Enable Subsurface Scattering in Unity PBR Master
- **Blender Input**: Color, Radius, IOR, Anisotropy
- **Unity Output**: SSS-enabled material

### Step 2: Configure Scatter
- **Description**: Set scatter distance and color
- **Blender Input**: SSS parameters
- **Unity Output**: Subsurface configuration

## Notes
- 30% compatibility - requires screen-space approximation
- Use HDRP's built-in SSS or custom fake SSS
- URP has limited SSS support
