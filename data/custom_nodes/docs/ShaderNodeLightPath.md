# ShaderNodeLightPath

## Overview
- **Blender Node**: ShaderNodeLightPath
- **Category**: Input
- **Compatibility**: 0%

## Conversion Process

### Step 1: Identify Light Path Usage
- **Description**: This node provides ray type information - unavailable in real-time
- **Blender Input**: Light path node outputs
- **Unity Output**: N/A - cannot be converted

### Step 2: Replace with Constants or Properties
- **Description**: Use constant values or material properties instead
- **Blender Input**: Is Camera Ray, Is Shadow Ray, etc.
- **Unity Output**: Fixed boolean values or shader keywords

### Step 3: Manual Shader Adjustments
- **Description**: Restructure the shader to work without ray information
- **Blender Input**: Complex ray-type dependent logic
- **Unity Output**: Simplified single-pass shader

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Is Camera Ray | Not available | 0% |
| Is Shadow Ray | Not available | 0% |
| Is Diffuse Ray | Not available | 0% |
| Is Glossy Ray | Not available | 0% |
| Ray Length | Not available | 0% |

## Build Instructions

1. This node has NO Unity equivalent
2. Identify what behavior the LightPath node was controlling
3. Replace with constant values or material properties
4. Simplify the shader to remove ray-type dependent logic
5. Use shader variants or keywords if different behaviors are needed

## Notes
- LightPath is a Cycles-specific node unavailable in real-time rendering
- Real-time rendering does not track ray history
- This node cannot be directly ported - requires shader restructuring
- Recommended: Remove and replace with simplified logic
