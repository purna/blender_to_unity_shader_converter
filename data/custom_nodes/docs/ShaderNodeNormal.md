# ShaderNodeNormal

## Overview
- **Blender Node**: ShaderNodeNormal
- **Category**: Input
- **Compatibility**: 90%

## Conversion Process

### Step 1: Direct Port
- **Description**: Normal vector input - direct mapping to Unity Normal node
- **Blender Input**: Normal vector in selected space
- **Unity Output**: Normal vector

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Normal | Normal node | 100% |

## Build Instructions

1. Create Normal node in Unity Shader Graph (Input > Normal)
2. Select space (Object, World, Tangent)
3. Connect output to destination (Normal input on PBR)

## Notes
- Direct 1:1 mapping
- Supports Object, World, and Tangent spaces
- 90% compatible
