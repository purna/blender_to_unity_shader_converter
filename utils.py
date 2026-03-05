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


def load_shadergraph_template() -> list:
    """
    Load the shadergraph template file and return as list of JSON strings.
    Each line in the template file is a separate JSON object.
    """
    template_file = Path(__file__).parent / "data" / "shadergraph_template.xml"
    
    if not template_file.exists():
        print(f"[WARN] Shadergraph template not found: {template_file}")
        return None
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract JSON lines from between <ShaderGraph> tags
        import re
        match = re.search(r'<ShaderGraph>(.*?)</ShaderGraph>', content, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
            lines = json_content.split('\n')
            # Filter out empty lines and return
            return [line.strip() for line in lines if line.strip()]
        
        return None
    except Exception as e:
        print(f"[ERROR] Failed to load shadergraph template: {e}")
        return None


def load_material_template() -> str:
    """
    Load the material template file and return as string.
    """
    template_file = Path(__file__).parent / "data" / "material_template.xml"
    
    if not template_file.exists():
        print(f"[WARN] Material template not found: {template_file}")
        return None
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract content between <Material> tags
        import re
        match = re.search(r'<Material>(.*?)</Material>', content, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return None
    except Exception as e:
        print(f"[ERROR] Failed to load material template: {e}")
        return None


def populate_shadergraph_template(template_lines: list, values: dict) -> list:
    """
    Populate shadergraph template with values.
    
    Args:
        template_lines: List of JSON template lines
        values: Dictionary of placeholder values
    
    Returns:
        List of populated JSON lines
    """
    result = []
    for line in template_lines:
        populated = line
        for key, value in values.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, str):
                populated = populated.replace(placeholder, value)
            elif isinstance(value, (int, float)):
                populated = populated.replace(placeholder, str(value))
            elif value is None:
                populated = populated.replace(placeholder, "")
        result.append(populated)
    
    return result


def populate_material_template(template: str, values: dict) -> str:
    """
    Populate material template with values.
    
    Args:
        template: YAML template string
        values: Dictionary of placeholder values
    
    Returns:
        Populated YAML string
    """
    result = template
    for key, value in values.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    
    return result
