# ShaderNodeParticleInfo

## Overview
- **Blender Node**: ShaderNodeParticleInfo
- **Category**: Input
- **Compatibility**: 25%

## ✅ EXAMPLES FOUND!

Unity ShaderGraph has particle shader examples:

| Example | Path |
|---------|------|
| **Particle Effect** | [`ParticleEffect.shadergraph`](../../examples/ShaderNodeParticleInfo/ParticleEffect.shadergraph) |

## Key Differences

| Blender Particle Info | Unity Particle Shader |
|----------------------|----------------------|
| Gets live simulation data | Uses Particle System properties |
| Random, Age, Lifetime, Location | Particle ID, Age, Color, Size |
| Per-particle simulation | Pre-defined system properties |

## Conversion Process

### Unity Particle Shader Approach

1. **Use Particle Shader Templates** - Unity provides Particle Lit/Unlit templates
2. **Configure Particle System** - Set up custom data in Particle System
3. **Use Vertex Stage** - Access particle properties in shader vertex stage

### Available Particle Properties in Unity ShaderGraph:

| Unity Property | Description | Blender Equivalent |
|----------------|-------------|-------------------|
| Particle ID | Unique particle identifier | Index |
| Particle Age | Time since birth | Age |
| Particle Lifetime | Total life span | Lifetime |
| Particle Position | World position | Location |
| Particle Velocity | Movement direction | Velocity |
| Particle Color | RGBA from system | Color |
| Particle Size | Current size | Size |

## Build Instructions

1. Start with **Particle Lit** or **Particle Unlit** template
2. Configure Particle System with custom data if needed
3. Use Vertex Stage to access particle properties
4. Connect to shader outputs (Base Color, Alpha, etc.)

## Notes
- Cannot access Blender's live particle simulation
- Must use Unity Particle System properties instead
- Compatibility: 25% (different data model)
- Example files added to JSON configuration
