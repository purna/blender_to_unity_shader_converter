# ShaderNodeLayerWeight

## Overview
- **Blender Node**: ShaderNodeLayerWeight
- **Category**: Input
- **Compatibility**: 75%

## Conversion Process

### Step 1: Implement Fresnel Output
- **Description**: Map Fresnel output to Unity Fresnel node
- **Blender Input**: Blend parameter (0-1)
- **Unity Output**: Fresnel Effect (0-1 edge brightness)

### Step 2: Transform Blend Parameter
- **Description**: Transform Blender's Blend to Fresnel Power using formula
- **Blender Input**: Blend value (0-1)
- **Unity Output**: Power value (1-10)

### Step 3: Implement Facing Output
- **Description**: Approximate Facing using Dot Product and math nodes
- **Blender Input**: View direction, Normal
- **Unity Output**: Surface orientation value

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Blend | Transform to Fresnel Power (1-10) | 85% |
| Fresnel | Fresnel Effect node | 85% |
| Facing | 1 - Dot(Normal, ViewDir) | 60% |

## Build Instructions

1. Create Fresnel node (Input > Fresnel Effect)
2. Create Multiply and Add nodes to transform Blend to Power
3. Formula: Power = 1 + (Blend * 9)
4. For Fresnel output: Connect transformed Power to Fresnel
5. For Facing output: Create Dot Product > One Minus chain

## Notes
- Fresnel output maps well to Unity's Fresnel Effect node
- Facing requires custom math (Dot Product + One Minus)
- Blend parameter transformation: Power = 1 + (Blend * 9)
- Use Custom Function for dynamic Blend control
