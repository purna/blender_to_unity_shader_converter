# ShaderNodeTexVoronoi

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeTexVoronoi
- **Category**: Texture
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Reference**: [blender-nodes-for-unity3d](https://github.com/Warwlock/blender-nodes-for-unity3d)

## Unity Equivalent
- **Primary**: Voronoi Node (Procedural)

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Voronoi](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Voronoi-Node.html) | Procedural | Generates Voronoi/cellular pattern |

### Supporting Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [UV](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/UV-Node.html) | Input | UV coordinates |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Vector | Vector | 0, 0 | UV coordinates |
| Scale | Float | 5.0 | Pattern scale |
| Randomness | Float | 1.0 | Randomness factor |

## Conversion Process

### Step 1: Create Voronoi
- **Description**: Add Voronoi node in Unity ShaderGraph
- **Blender Input**: Scale, Randomness
- **Unity Output**: Voronoi pattern

### Step 2: Configure Parameters
- **Description**: Set scale for cell size
- **Blender Input**: Scale
- **Unity Output**: Configured Voronoi

### Step 3: Adjust Output
- **Description**: Use outputs for cell edges or colors
- **Unity Output**: Distance (cell edges), Color (cell colors)

## Unity Connections

```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Vector (UV)      ──►     UV                   Voronoi
Scale            ──►     Scale                │
Randomness       ──►     Jitter               │
                                           │
                                           ▼
                           Distance / Color ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| UV | Vector2 | 0,0 | UV coordinates |
| Scale | Float | 5 | Cell size scale |
| Jitter | Float | 1 | Randomness (0-1) |

## Visual Graph Layout

```
// Basic Voronoi
[UV] ──> [Voronoi] ──> [Output]
              ^
              │
[Float: 5.0] ─┘

// With Randomness
[UV] ──> [Voronoi] ──> [Cell Color / Distance]
              ^   ^
              │   │
[Float: 5.0]  │   │
              │   │
[Float: 0.5] ─┴───┘
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Texture/VoronoiTexture.shadersubgraph` | Unity Shader Graph subgraph |
| `data/custom_nodes/examples/ShaderNodeTexVoronoi/Procedural-Noise-Voronoi.ShaderGraph` | Example shader |
| `data/custom_nodes/examples/ShaderNodeTexVoronoi/Procedural-Noise-VoronoiShuffle.ShaderGraph` | Example shader |

## Compatibility Notes
- 100% compatible - basic Voronoi works
- Distance metrics differ slightly
- Unity has built-in Voronoi node

## Limitations
- Different distance metrics
- Less randomness control than Blender
