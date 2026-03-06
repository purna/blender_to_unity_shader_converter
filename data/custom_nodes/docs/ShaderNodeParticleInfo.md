# ShaderNodeParticleInfo

## Overview
- **Blender Node**: ShaderNodeParticleInfo
- **Category**: Input
- **Compatibility**: 10%

## Conversion Process

### Step 1: Identify Particle Usage
- **Description**: Particle system information is not accessible in Shader Graph
- **Blender Input**: Particle position, velocity, age, etc.
- **Unity Output**: N/A

### Step 2: Use Particle Properties
- **Description**: Use particle system custom data or vertex attributes
- **Blender Input**: Particle Info outputs
- **Unity Output**: Custom particle data

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Index | Not available | 0% |
| Random | Custom vertex data | 10% |
| Age | Custom vertex data | 10% |
| Lifetime | Not available | 0% |
| Location | Particle position | 10% |
| Velocity | Particle velocity | 10% |

## Build Instructions

1. This node has limited Unity equivalent
2. Use custom vertex data or particle system custom data
3. For complex particle effects, use VFX Graph or custom shaders

## Notes
- Particle data not directly accessible in Shader Graph
- Requires particle system integration
- Limited workaround options available
- 10% compatibility through custom data approaches
