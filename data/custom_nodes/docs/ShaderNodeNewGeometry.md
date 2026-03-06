# ShaderNodeNewGeometry

## Overview
- **Blender Node**: ShaderNodeNewGeometry
- **Category**: Input
- **Compatibility**: 90%

## Conversion Process

### Step 1: Identify Output Needs
- **Description**: Determine which geometry outputs are needed
- **Blender Input**: Geometry node with multiple outputs
- **Unity Output**: Separate nodes for each output

### Step 2: Create Unity Nodes
- **Description**: Create appropriate Unity nodes for each output
- **Blender Input**: Output selection
- **Unity Output**: Position, Normal, UV, Tangent nodes

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Position | Position node | 100% |
| Normal | Normal node | 100% |
| Tangent | Tangent node | 90% |
| True Normal | Normal (calculate) | 80% |
| Incoming | View Direction | 100% |
| Parametric | UV node | 90% |

## Build Instructions

1. Create Position node (Input > Position)
2. Create Normal node (Input > Normal)
3. Create Tangent node (Input > Tangent)
4. Create View Direction (Input > View Direction)
5. Create UV node (Input > UV)

## Notes
- Multi-output node - creates separate nodes in Unity
- Most outputs map directly
- 90% compatible overall
