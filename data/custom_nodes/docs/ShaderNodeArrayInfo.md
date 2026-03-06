# ShaderNodeArrayInfo

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 0% |
| **Category** | Utility |

## Summary
Geometry array information - not available in Unity. Blender specific node with no equivalent in Unity.

## Unity Equivalent
**N/A** - Not supported

## Conversion Process

### Step 1: Identify Array Source
- **Blender Input**: Geometry array info
- **Unity Output**: N/A
- **Description**: Blender-specific feature for geometry nodes

### Step 2: Determine Alternative
- **Blender Input**: Array information request
- **Unity Output**: Custom implementation required
- **Description**: Requires geometry nodes or custom code

### Step 3: Implement Custom Solution
- **Blender Input**: Array metadata
- **Unity Output**: C# script or custom shader
- **Description**: Implement custom solution for instancing metadata

## Parameters
| Blender | Description |
|---------|-------------|
| Array Info | Geometry array information |

## Compatibility
- **Fully Compatible**: None
- **Partially Compatible**: None
- **Incompatible**: All features

## Limitations
- Blender-specific node
- No equivalent in Unity ShaderGraph
- Requires geometry nodes or custom code
