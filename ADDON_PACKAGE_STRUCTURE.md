# Blender to Unity Shader Converter - Multi-File Addon Package

## Folder Structure

After installation, the addon should look like this:

```
blender_addons/scripts/addons/
└─ blender_to_unity_shader_converter/          ← Main package folder
   ├─ __init__.py                              ← Package entry point (registration)
   ├─ operators.py                             ← Blender operator definitions
   ├─ parser.py                                ← Blender shader parser
   ├─ converter.py                             ← Conversion engine
   ├─ socket_handler.py                        ← Socket type compatibility
   ├─ strategies.py                            ← Conversion strategies
   ├─ exporter.py                              ← Unity asset export
   ├─ utils.py                                 ← Utility functions
   ├─ ui.py                                    ← UI panels (future)
   ├─ data/
   │  └─ node_mappings.json                    ← All 78 nodes + strategies
   └─ README.md                                ← Addon-specific docs
```

---

## Installation

Instead of copying a single `.py` file, you now **copy the entire folder**:

```bash
# Copy the entire folder to Blender addons directory
cp -r blender_to_unity_shader_converter ~/.config/blender/4.0/scripts/addons/
```

---

## Key Advantages

✅ **Modular code** - Each file has one responsibility  
✅ **JSON data** - Easy to update node mappings without touching code  
✅ **Scalability** - Easy to add new modules (ui.py, validation.py, etc.)  
✅ **Maintainability** - Clear separation of concerns  
✅ **Hot reload** - Update JSON without restarting Blender  
✅ **Testing** - Each module can be tested independently  

---

## File Responsibilities

| File | Purpose |
|------|---------|
| `__init__.py` | Loads bl_info, imports modules, registers/unregisters operator |
| `operators.py` | Defines the SHADER_OT_convert_to_unity operator |
| `parser.py` | Extracts data from Blender materials |
| `converter.py` | Main conversion engine with strategy routing |
| `socket_handler.py` | Socket type compatibility matrix |
| `strategies.py` | Conversion strategy implementations |
| `exporter.py` | Writes FBX and shader graphs to disk |
| `utils.py` | Helper functions (logging, file I/O, etc.) |
| `node_mappings.json` | Database of all 78 nodes + strategies |

---

## How It Works

### 1. Blender loads `__init__.py`

```python
# __init__.py
bl_info = { ... }

from . import operators, parser, converter, exporter

def register():
    operators.register()

def unregister():
    operators.unregister()
```

### 2. `__init__.py` imports all modules

Each module is imported with relative imports (`.`):
```python
from . import operators      # imports operators.py
from . import parser         # imports parser.py
from . import converter      # imports converter.py
```

### 3. Operator loads the JSON

```python
# operators.py
import json
from pathlib import Path

def load_node_mappings():
    """Load node mappings from JSON file"""
    json_path = Path(__file__).parent / "data" / "node_mappings.json"
    with open(json_path, 'r') as f:
        return json.load(f)

NODE_MAPPING = load_node_mappings()
```

### 4. Converter uses the JSON data

```python
# converter.py
from . import socket_handler
from . import strategies

def convert(blender_data):
    for node_data in blender_data['nodes']:
        strategy = NODE_MAPPING[node_type]['strategy']
        
        if strategy == 'direct':
            # Direct conversion
            pass
        elif strategy == 'decompose':
            # Use strategy
            strategies.handle_principled_bsdf(...)
```

---

## Module Imports

All modules use **relative imports** from the package:

```python
# In any file within the package
from . import parser           # Import from same package
from .converter import ShaderGraphConverter  # Import class from module
from .strategies import ConversionStrategy
from .socket_handler import SocketTypeHandler
```

**Never use absolute imports like:**
```python
import blender_to_unity_shader_converter  # ✗ Wrong
```

---

## Loading the JSON File

### Simple approach:
```python
import json
from pathlib import Path

# Get the folder where this Python file is located
addon_dir = Path(__file__).parent
json_file = addon_dir / "data" / "node_mappings.json"

with open(json_file, 'r') as f:
    NODE_MAPPING = json.load(f)
```

### Safe approach (with error handling):
```python
import json
from pathlib import Path

def load_node_mappings():
    json_file = Path(__file__).parent / "data" / "node_mappings.json"
    
    if not json_file.exists():
        raise FileNotFoundError(f"Node mappings not found: {json_file}")
    
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in node_mappings.json: {e}")

NODE_MAPPING = load_node_mappings()
```

---

## File Sizes (Expected)

| File | Size | Purpose |
|------|------|---------|
| `__init__.py` | ~1KB | Registration |
| `operators.py` | ~3KB | Operator definition |
| `parser.py` | ~8KB | Parser class |
| `converter.py` | ~10KB | Main converter |
| `socket_handler.py` | ~2KB | Type checking |
| `strategies.py` | ~15KB | Strategy methods |
| `exporter.py` | ~8KB | Export logic |
| `utils.py` | ~3KB | Helpers |
| `node_mappings.json` | ~25KB | All 78 nodes |
| **Total** | **~75KB** | Complete addon |

---

## Example: Converting Single .py to Package

### Original Structure (Single File)
```python
# blender_to_unity_converter.py (800+ lines)
import bpy

class BlenderShaderParser:
    ...

class ShaderGraphConverter:
    ...

class UnityExporter:
    ...
```

### New Structure (Modular)
```
blender_to_unity_shader_converter/
├─ __init__.py                    # 20 lines - registration
├─ parser.py                      # 150 lines
├─ converter.py                   # 200 lines
├─ exporter.py                    # 120 lines
├─ strategies.py                  # 250 lines
├─ socket_handler.py              # 50 lines
├─ utils.py                       # 40 lines
├─ operators.py                   # 80 lines
└─ data/
   └─ node_mappings.json          # JSON with all nodes
```

---

## Migration from Single File

If you already have a single `.py` file:

1. **Create the package folder**
   ```bash
   mkdir blender_to_unity_shader_converter
   cd blender_to_unity_shader_converter
   ```

2. **Split the code**
   - Copy `bl_info` and registration to `__init__.py`
   - Copy classes to respective `.py` files
   - Extract NODE_MAPPING to `data/node_mappings.json`

3. **Add imports**
   - Update all imports to use relative imports (`.`)
   - Import modules in `__init__.py`

4. **Update paths**
   - Change NODE_MAPPING references to load from JSON
   - Use `Path(__file__).parent / "data" / "node_mappings.json"`

5. **Test**
   - Copy to Blender addons folder
   - Restart Blender
   - Check addon list

---

## JSON Structure Example

```json
{
  "ShaderNodeMath": {
    "unity_type": "Unity.Shader.Graph.Math",
    "node_name": "Math",
    "strategy": "direct",
    "compatibility": "100%",
    "operations": {
      "ADD": "Add",
      "MULTIPLY": "Multiply",
      "SUBTRACT": "Subtract"
    }
  },
  "ShaderNodeBsdfPrincipled": {
    "unity_type": "Custom",
    "node_name": "Principled BSDF",
    "strategy": "decompose",
    "compatibility": "50%",
    "components": ["Color", "Metallic", "Roughness", "Normal", "Emission"],
    "decomposition_note": "Splits into 5-7 nodes"
  }
}
```

---

## Updating Node Mappings at Runtime

Once using JSON, you can update nodes without code changes:

```python
def reload_node_mappings():
    """Hot-reload node mappings from JSON"""
    global NODE_MAPPING
    NODE_MAPPING = load_node_mappings()
    print(f"Reloaded {len(NODE_MAPPING)} node mappings")

# Call this whenever JSON is updated
reload_node_mappings()
```

---

## Creating the Package

### Option 1: Manual (Recommended for small changes)

1. Create folder: `blender_to_unity_shader_converter`
2. Create files: `__init__.py`, `operators.py`, etc.
3. Create subfolder: `data/`
4. Create file: `data/node_mappings.json`
5. Copy contents from this guide into each file

### Option 2: Automated (Using template)

```bash
# This would be a script to automate the split
python split_addon.py blender_to_unity_converter.py blender_to_unity_shader_converter/
```

---

## Version Control

The package structure is much better for git:

```
.gitignore
├─ __pycache__/
├─ *.pyc
├─ .vscode/

addon/
├─ __init__.py
├─ operators.py
├─ converter.py
├─ strategies.py
├─ socket_handler.py
├─ parser.py
├─ exporter.py
├─ utils.py
└─ data/
   └─ node_mappings.json
```

You can track each file separately, making collaboration easier.

---

## Testing Each Module

```python
# test_parser.py
from blender_to_unity_shader_converter.parser import BlenderShaderParser

def test_parser():
    # Test without Blender
    parser = BlenderShaderParser(mock_material)
    result = parser.parse()
    assert result['nodes'] == [...]

# test_converter.py
from blender_to_unity_shader_converter.converter import ShaderGraphConverter

def test_principled_decomposition():
    # Test conversion strategy
    converter = ShaderGraphConverter(test_data)
    result = converter.convert()
    assert len(result.nodes) >= 5  # Should decompose to 5+ nodes
```

---

## Distribution & Sharing

With the package structure:

```bash
# Easy to distribute
zip -r blender_to_unity_shader_converter.zip blender_to_unity_shader_converter/

# Users can install by extracting to addons folder
# Or use Blender's built-in addon installer
```

---

## Summary

| Aspect | Single File | Multi-File Package |
|--------|-------------|-------------------|
| **Files** | 1 (.py) | 8+ (.py) + 1 (.json) |
| **Modularity** | Low | High |
| **Code size** | 800+ lines | 50-250 per file |
| **JSON data** | Hardcoded dict | External file |
| **Updates** | Need reload | JSON hot-reload |
| **Testing** | Difficult | Easy per module |
| **Maintenance** | Hard | Easy |
| **Scalability** | Limited | Excellent |

**Recommendation:** Use the **multi-file package** structure for any addon you plan to maintain or distribute.

