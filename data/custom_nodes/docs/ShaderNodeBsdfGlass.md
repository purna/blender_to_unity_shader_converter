# ShaderNodeBsdfGlass

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 70% |
| **Category** | Shader |

## Summary
Glass/transparent shader with refraction. Complex approximation required for real-time rendering.

## Unity Equivalent
**PBR Master with Transmission** or Refraction

## Conversion Process

### Step 1: Set Base Color
- **Blender Input**: Color
- **Unity Output**: Base Color on PBR Master
- **Description**: Connect glass tint color

### Step 2: Configure Roughness
- **Blender Input**: Roughness
- **Unity Output**: Smoothness
- **Description**: Smoothness = 1.0 - Roughness (higher smoothness = clearer glass)

### Step 3: Set IOR
- **Blender Input**: IOR (Index of Refraction)
- **Unity Output**: Index of Refraction
- **Description**: Configure IOR (typical: 1.5 for glass)

### Step 4: Enable Transparency
- **Blender Input**: BSDF output
- **Unity Output**: PBR Master (Transparent)
- **Description**: Set Surface Type to Transparent, enable Transmission

## Parameters
| Blender | Description | Unity Mapping |
|---------|-------------|--------------|
| Color | Glass tint color | → Base Color |
| Roughness | Surface roughness | → Smoothness = 1-Roughness |
| IOR | Index of Refraction | → IOR (1.0-3.0) |

## Common IOR Values
| Material | IOR |
|----------|-----|
| Air | 1.0 |
| Water | 1.33 |
| Glass | 1.5 |
| Diamond | 2.42 |

## Compatibility
- **Fully Compatible**: Basic glass appearance
- **Partially Compatible**: IOR-based refraction
- **Incompatible**: Full ray-traced refraction

## Limitations
- Full IOR-based refraction is difficult in real-time
- Requires transparent material setup
- Transmission may not work on all platforms
