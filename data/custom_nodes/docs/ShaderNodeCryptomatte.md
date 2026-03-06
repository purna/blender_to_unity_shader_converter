# ShaderNodeCryptomatte - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Input
- **Compatibility**: 0%

## Blender Node Description
Cryptomatte ID pass - Blender Cycles compositing only. Provides object ID-based mattes for compositing.

## Unity Equivalent
- **Primary**: N/A
- **Implementation**: Not supported

## Conversion Process

### Step 1: Remove Node
- Cryptomatte is a compositor-only feature
- Remove from shader - not supported in Unity

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Matte | Color | N/A | Not supported |
| ID | Float | N/A | Not supported |

## Compatibility Notes
- 0% compatible - completely incompatible
- Requires post-processing in Unity

## Limitations
- Not available in ShaderGraph
- Requires post-processing or custom shader
- Compositor-only feature
