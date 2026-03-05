# Blender to Unity Shader Converter - Addon Package

## Installation

Install package via the Addon Preferences in Blender: https://github.com/purna/[Blender to Unity Shader Converter Plugin](https://github.com/purna/blender_to_unity_shader_converter/releases/tag/Blender_to_Unity_Shader_Converter)


Then enable the addon in **Edit → Preferences → Add-ons**

## Folder Structure

```
blender_to_unity_shader_converter/
 ├─ __init__.py                     # Addon registration
 ├─ operators.py                    # Blender operator
 ├─ parser.py                       # Shader parser
 ├─ converter.py                    # Conversion engine
 ├─ socket_handler.py               # Type checking
 ├─ strategies.py                   # Conversion strategies
 ├─ exporter.py                     # Export functionality
 ├─ utils.py                        # Utility functions & template loading
 ├─ ui.py                           # UI panel
 ├─ fbx_helper.py                   # FBX export helper
 ├─ data/
 │  ├─ node_mappings.json           # 78+ node conversions
 │  ├─ node_mappings_with_params.json # Extended mappings with parameters
 │  ├─ shadergraph_template.xml     # Unity ShaderGraph template
 │  └─ material_template.xml         # Unity Material template
 └─ README.md                       # This file
```

## How JSON Loading Works

1. **Addon loads** → `__init__.py` runs
2. **__init__.py imports** → `from . import operators`
3. **operators.py imports utils** → `from . import utils`
4. **utils.load_node_mappings()** → Reads `data/node_mappings.json`
5. **JSON is stored** → `NODE_MAPPING` dictionary in operators.py
6. **Converter uses it** → Passed to `ShaderGraphConverter()`

### Template System

The exporter uses XML templates for generating Unity ShaderGraph and Material files:

1. **utils.py loads templates** → `load_shadergraph_template()` and `load_material_template()`
2. **Templates populated** → `populate_shadergraph_template()` and `populate_material_template()`
3. **Exporter uses templates** → Falls back to inline generation if templates unavailable

Templates provide maintainability - edit XML instead of Python code for Unity format changes.

## Updating Node Mappings

To add or update node conversions:

1. Edit `data/node_mappings.json`
2. Add entry for Blender node type:
```json
{
  "ShaderNodeCustom": {
    "unity_name": "Custom Node",
    "unity_type": "CustomType",
    "category": "Shader",
    "strategy": "direct",
    "compatibility": "85%",
    "description": "Your description here"
  }
}
```
3. **No code changes needed!** JSON is hot-reloaded next time operator runs

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| `__init__.py` | Registers addon, imports modules |
| `operators.py` | Defines "Convert to Unity" operator, loads JSON |
| `parser.py` | Extracts shader data from Blender |
| `converter.py` | Routes nodes to strategies, builds output |
| `socket_handler.py` | Validates socket type compatibility |
| `strategies.py` | Implements complex node conversions |
| `exporter.py` | Writes FBX, shader graphs, and materials |
| `utils.py` | Helper functions (JSON loading, template loading, logging) |
| `ui.py` | UI panel for viewing conversion results |

## Usage Flow

```
User selects object & clicks "Convert to Unity"
    ↓
operators.py invokes operator
    ↓
parser.py extracts shader nodes
    ↓
converter.py converts each node
    ├─ Looks up strategy in NODE_MAPPING (from JSON)
    ├─ Routes to strategies.py if needed
    └─ socket_handler.py validates connections
    ↓
exporter.py writes:
    ├─ Models/ (FBX)
    ├─ Materials/ (.mat)
    ├─ Shaders/ (.shadergraph)
    └─ Textures/
```

## JSON Schema

Each node entry has:

```json
{
  "ShaderNodeType": {
    "unity_name": "Name in Unity",           # String
    "unity_type": "Unity.Type",              # String
    "category": "Shader/Input/Vector/Color", # String
    "strategy": "direct/decompose/approx",   # String
    "compatibility": "100%/50%/0%",          # String
    "description": "What it does"            # String
  }
}
```

## Supported Strategies

- **direct** - 1:1 node mapping
- **decompose** - Split into multiple nodes
- **blend_mapping** - Blend mode conversion
- **normal_mapping** - Normal space handling
- **texture_reference** - Texture sampling
- **attribute_mapping** - Vertex attributes
- **uv_mapping** - UV transforms
- **procedural_texture** - Procedural patterns
- **bake_only** - Requires pre-baking
- **approximation** - Mathematical approximation
- **incompatible** - Cannot convert
- **vertex_displacement** - Vertex offsets
- **custom_attribute** - Custom setup needed

## Development

To add a new conversion strategy:

1. **Add method in strategies.py:**
```python
@staticmethod
def handle_custom_node(node_data):
    # Implementation
    return conversion_result
```

2. **Add entry to node_mappings.json:**
```json
"ShaderNodeCustom": {
  "strategy": "custom_strategy",
  ...
}
```

3. **Add case in converter.py:**
```python
elif strategy == 'custom_strategy':
    result = strategies.ConversionStrategy.handle_custom_node(node_data)
    # Create nodes
```

## Troubleshooting

### JSON Not Loading
- Check `data/node_mappings.json` exists
- Verify JSON is valid (use json validator)
- Check System Console for error messages

### Node Not Converting
- Add entry to `node_mappings.json`
- Restart Blender to reload JSON
- Check strategy is implemented in `strategies.py`

### Type Mismatch Errors
- Edit `socket_handler.py` COMPATIBILITY_MATRIX
- Add new type pair conversion
- Restart Blender

## File Sizes

| File | Size |
|------|------|
| __init__.py | ~1KB |
| operators.py | ~19KB |
| parser.py | ~7KB |
| converter.py | ~36KB |
| socket_handler.py | ~2KB |
| strategies.py | ~4KB |
| exporter.py | ~17KB |
| utils.py | ~2KB |
| ui.py | ~11KB |
| fbx_helper.py | ~3KB |
| node_mappings.json | ~97KB |
| node_mappings_with_params.json | ~143KB |
| shadergraph_template.xml | ~10KB |
| material_template.xml | ~9KB |
| **Total** | **~340KB** |

## Version

- **Version:** 0.7.0
- **Blender:** 5.1+
- **Python:** 3.9+
- **Unity:** 2021.1+ (URP supported)

## License

This addon is provided as-is for shader conversion from Blender to Unity.
