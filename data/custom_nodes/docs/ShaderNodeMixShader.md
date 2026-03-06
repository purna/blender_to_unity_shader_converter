# ShaderNodeMixShader

## Overview
- **Blender Node**: ShaderNodeMixShader
- **Category**: Shader
- **Compatibility**: 85%

## Conversion Process

### Step 1: Decompose Shaders
- **Description**: Extract material properties from both shaders
- **Blender Input**: Shader1, Shader2, Factor
- **Unity Output**: Base color, Metallic, Smoothness values

### Step 2: Blend Properties
- **Description**: Lerp between property values using factor
- **Blender Input**: Property values from both shaders
- **Unity Output**: Blended property values

### Step 3: Connect to Master
- **Description**: Connect blended properties to PBR Master
- **Blender Input**: Blended values
- **Unity Output**: Final material

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Fac | Lerp factor | 100% |
| Shader1 | Property set 1 | 85% |
| Shader2 | Property set 2 | 85% |

## Build Instructions

1. Extract properties from first shader (Color, Metallic, Smoothness, etc.)
2. Extract properties from second shader
3. Create Lerp nodes for each property
4. Connect factor to all Lerp nodes
5. Connect blended outputs to PBR Master inputs

## Notes
- Blends PBR properties, not complete shaders
- Works for simple material transitions
- 15% loss - cannot blend complex features (SSS, anisotropy)
