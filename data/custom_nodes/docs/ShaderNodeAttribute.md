# ShaderNodeAttribute

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 85% |
| **Category** | Input |
| **Complexity** | Medium |

## Summary
Access mesh custom attributes (vertex color, UVs, etc.) - reads custom mesh attributes and maps to Unity equivalent.

## Unity Equivalent
**Vertex Attribute** - Vertex Color, UV nodes

## Conversion Process

### Step 1: Identify Attribute Name
- **Blender Input**: Name (attribute name to read)
- **Unity Output**: Identify target node type
- **Description**: Read the attribute name from Blender node

### Step 2: Map to Unity Equivalent
- **Blender Input**: Attribute type (Col, UVMap, CustomData)
- **Unity Output**: Corresponding Unity node
- **Description**: Map Blender attribute to Unity:
  - Col → VertexColor node
  - UVMap → UV node (channel 0)
  - UV2 → UV node (channel 1)

### Step 3: Handle Custom Attributes
- **Blender Input**: Custom attribute data
- **Unity Output**: Custom Function or Property Block from C#
- **Description**: For custom attributes, use Material Property Block from C# script

## Parameters
| Blender | Description |
|---------|-------------|
| Name | Attribute name to read |
| Col | Vertex color |
| UVMap | UV coordinates |
| CustomData | Custom attribute data |

## Common Mappings
| Blender | Unity |
|---------|-------|
| Col | VertexColor |
| UVMap | UV (channel 0) |
| UV2 | UV (channel 1) |

## Compatibility
- **Fully Compatible**: Vertex color, UV coordinates
- **Partially Compatible**: Custom attributes (require C# scripting)
- **Incompatible**: Some specialized Blender attributes

## Limitations
- Custom attributes not native to ShaderGraph
- May require C# scripting for custom data
