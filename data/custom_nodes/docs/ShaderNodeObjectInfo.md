# ShaderNodeObjectInfo

## Overview
- **Blender Node**: ShaderNodeObjectInfo
- **Category**: Input
- **Compatibility**: 30%

## Conversion Process

### Step 1: Position Output
- **Description**: Map Location to Unity Position node
- **Blender Input**: Object location
- **Unity Output**: Position node (Object or World space)

### Step 2: Random Output
- **Description**: Approximate with custom function using world position hash
- **Blender Input**: Random value per object
- **Unity Output**: Custom Function with hash formula

### Step 3: Object Index
- **Description**: Cannot dynamically get object index in Unity
- **Blender Input**: Object Index
- **Unity Output**: Material Property Block (requires C#)

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Location | Position node | 100% |
| Random | Custom Function (hash) | 85% |
| Object Index | Material Property Block | 10% |
| Color | Vertex Color | 20% |
| Alpha | Material Property | 0% |
| Material Index | Not available | 0% |

## Build Instructions

1. Create Position node for Location output
2. For Random: Create Custom Function with hash-based random
3. For Object Index: Use C# Material Property Block
4. For Color: Use Vertex Color node

## Notes
- Limited compatibility - several outputs unavailable
- Position maps directly (100%)
- Random can be approximated with custom function (85%)
- Object Index requires C# script per instance
- Most other outputs not available in Unity
