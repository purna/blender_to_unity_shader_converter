# ShaderNodeTexIES - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 50%

## ⚠️ IMPORTANT: No ShaderGraph Example Exists!

**Reason:** Unity Light Cookies are NOT a ShaderGraph node - they are a **Light Component property**.

| Blender IES Texture | Unity Light Cookies |
|---------------------|-------------------|
| Loads .ies files as texture | Applied to Light component |
| Used in material shaders | Controls light attenuation |
| Cycles/Eevee feature | URP/HDRP light property |

## Blender Node Description
IES Texture - loads IES light profile files for realistic lighting falloff.

## Unity Equivalent
- **NOT a ShaderGraph node**
- **Light Component property**: Apply IES as Cookie on Spotlight/Point light
- **Location**: Unity Editor > Light Component > Cookie field

## Why No Example Exists

1. **Light Cookies are NOT ShaderGraph** - They're configured on the Light component
2. **No shader required** - It's a light-level setting
3. **Workflow**: Import IES → Apply to Light → Configure spotlight
4. **Verified**: Searched all Unity ShaderGraph examples - no cookie shader examples exist

## Unity Setup Instructions

### Option 1: Native IES Import (HDRP)
1. Import .ies file to Unity project
2. Select Spotlight/Point light
3. In Light component, assign IES to "Cookie" field
4. Adjust cookie size and other settings

### Option 2: URP/Built-in (Pre-bake)
1. Convert IES to grayscale texture in Blender
2. Import texture to Unity
3. Apply to Light > Cookie field
4. Use as lookup for light intensity

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Strength | Float | Intensity | Direct |

## Compatibility Notes
- 50% compatible - requires light setup
- NOT a ShaderGraph feature
- Example: N/A (Light Component, not shader)

## Limitations
- No shader example can be provided
- Requires Light Component configuration
- Different workflow than material shaders
