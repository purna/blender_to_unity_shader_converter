# ShaderNodeMapping

## Overview
- **Blender Node**: ShaderNodeMapping
- **Category**: Vector
- **Compatibility**: 90%

## Conversion Process

### Step 1: Apply Location (Translation)
- **Description**: Translate UV coordinates by location offset
- **Blender Input**: UV coordinates, Location (X, Y, Z)
- **Unity Output**: Offset UV coordinates

### Step 2: Apply Scale
- **Description**: Scale UV coordinates by scale factor
- **Blender Input**: Translated UV, Scale (X, Y, Z)
- **Unity Output**: Scaled UV coordinates

### Step 3: Apply Rotation
- **Description**: Rotate UV coordinates (more complex - may need custom function)
- **Blender Input**: Scaled UV, Rotation (X, Y, Z in degrees)
- **Unity Output**: Rotated UV coordinates

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Vector | Input UV | 100% |
| Location | Tiling and Offset (Offset) | 90% |
| Rotation | Custom rotation matrix | 80% |
| Scale | Tiling and Offset (Tiling) | 90% |

## Build Instructions

1. Create Tiling And Offset node (UV > Tiling And Offset)
2. Connect UV to the node
3. Set Offset for Location (X, Y)
4. Set Tiling for Scale (X, Y)
5. For rotation: Use custom rotation matrix or Rotate node

## Notes
- Unity's Tiling and Offset handles Location and Scale directly
- 3D rotation requires custom function or rotation matrix nodes
- For best results: use custom function for full 3D transformation
- Unity typically uses 2D UV, but can work with 3D for projections
