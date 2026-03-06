# ShaderNodeFresnel - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Input
- **Compatibility**: 95%

## Blender Node Description
Fresnel edge effect. Outputs fresnel weight based on view angle.

## Unity Equivalent
- **Primary**: Fresnel Effect node
- **Implementation**: Direct mapping

## Conversion Process

### Step 1: Create Fresnel Node
- Add Fresnel Effect node in Unity

### Step 2: Connect Normal
- Connect Normal input if available

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Normal | Vector3 | Normal | Optional |
| IOR | Float | Power | Direct |

## Compatibility Notes
- 95% compatible - direct mapping
- Uses Fresnel equation based on view angle

## Limitations
- None significant
