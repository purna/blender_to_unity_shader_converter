# ShaderNodeTexBrick

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: ShaderNodeTexBrick
- **Category**: Texture
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
- **Primary**: Brick Node (Procedural) or Tiling/Offset + Custom

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Brick](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Brick-Node.html) | Procedural | Generates brick pattern |

### Alternative Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Tiling And Offset](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Tiling-And-Offset-Node.html) | UV | UV tiling |
| [Gradient](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Gradient-Node.html) | Procedural | Gradient for brick pattern |
| [Step](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Step-Node.html) | Math | Step function |
| [Smoothstep](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Smoothstep-Node.html) | Math | Smooth step |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color1 | Color | 0.8, 0.2, 0.2, 1 | Brick color |
| Color2 | Color | 0.5, 0.5, 0.5, 1 | Mortar color |
| Mortar | Float | 0.02 | Mortar width |
| Scale | Float | 5.0 | Pattern scale |
| Brick Width | Float | 0.5 | Width of each brick |
| Brick Height | Float | 0.25 | Height of each brick |
| Offset | Float | 0.5 | Row offset |
| Offset Frequency | Int | 2 | Offset frequency |
| Squash | Float | 1.0 | Squash factor |

## Conversion Process

### Step 1: Create Brick
- **Description**: Add Brick node in Unity ShaderGraph
- **Blender Input**: Offset, Row Height, Colors
- **Unity Output**: Brick pattern

### Step 2: Configure Pattern
- **Description**: Set brick and mortar colors
- **Blender Input**: Color1, Color2
- **Unity Output**: Configured pattern

### Step 3: Adjust Parameters
- **Description**: Set scale and offset
- **Blender Input**: Scale, Offset
- **Unity Output**: Final brick pattern

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Vector (UV)      ──►     UV                   Brick
Color1           ──►     Brick Color          │
Color2           ──►     Mortar Color         │
Scale            ──►     (internal)           │
Brick Width      ──►     (internal)           │
Brick Height     ──►     (internal)           │
Offset           ──►     (internal)           │
                                           │
                                           ▼
                           Out ────────────► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| UV | Vector2 | 0,0 | UV coordinates |
| Brick Color | Color | Gray | Brick tile color |
| Mortar Color | Color | White | Mortar color |
| Scale | Float | 5 | Pattern scale |

## Visual Graph Layout

```
// Using Unity's Brick node
[UV] ──> [Brick] ──> [Output]
              ^
              │
[Colors] ─────┘

// Alternative: Manual brick pattern
[UV] ──> [Gradient] ──> [Step] ──> [Lerp Colors] ──> [Output]
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Texture/BrickTexture.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeTexBrick/Procedural-Pattern-Shatter.ShaderGraph` | Example shader |
| `data/custom_nodes/examples/ShaderNodeTexBrick/Procedural-Pattern-Stripes.ShaderGraph` | Example shader |

## Compatibility Notes
- 100% compatible - basic brick works
- Unity has built-in Brick node
- Some advanced parameters may require custom implementation

## Limitations
- Different brick algorithm than Blender
- Squash factor not available
- Offset frequency limited
