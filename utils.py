"""
Utility Functions
Helper functions for logging, file I/O, etc.
"""

import json
from pathlib import Path
from typing import Dict, Any

def load_node_mappings() -> Dict[str, Any]:
    """
    Load node mappings from JSON file
    
    This is called by operators.py to load the conversion strategies.
    Uses node_mappings_with_params.json which includes detailed parameter
    mappings for converting Blender nodes to Unity ShaderGraph.
    """
    json_file = Path(__file__).parent / "data" / "node_mappings_with_params.json"
    
    if not json_file.exists():
        raise FileNotFoundError(f"Node mappings not found: {json_file}")
    
    try:
        with open(json_file, 'r') as f:
            mappings = json.load(f)
            print(f"✓ Loaded {len(mappings)} node mappings from JSON")
            return mappings
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in node_mappings.json: {e}")


def log_conversion_stats(report: Dict[str, int]):
    """Log conversion statistics"""
    print("\nConversion Statistics:")
    print(f"  Converted:     {report['nodes_converted']}")
    print(f"  Decomposed:    {report['nodes_decomposed']}")
    print(f"  Approximated:  {report['nodes_approximated']}")
    print(f"  Incompatible:  {report['nodes_incompatible']}")


def validate_blender_object(obj) -> bool:
    """Validate that object has a material with nodes"""
    if not obj:
        return False
    if not obj.data or not hasattr(obj.data, 'materials'):
        return False
    if not obj.data.materials:
        return False
    
    material = obj.data.materials[0]
    if not material.use_nodes:
        return False
    
    return True


def get_addon_version() -> str:
    """Get addon version from __init__.py"""
    # Version is stored in __init__.py bl_info dictionary
    return "0.5.0"
