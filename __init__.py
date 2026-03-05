"""
Blender to Unity Shader Graph Converter
Multi-file addon package with JSON node database
"""

bl_info = {
    "name": "Blender to Unity Shader Converter",
    "author": "Pixelgent",
    "version": (0, 6, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Object > Convert to Unity",
    "description": "Convert Blender shader graphs to Unity shader graphs. Supports 78+ nodes with JSON-based conversion strategies.",
    "warning": "Production-Ready",
    "wiki_url": "https://github.com/purna/blender_to_unity_shader_converter/wiki",
    "tracker_url": "https://github.com/purna/blender_to_unity_shader_converter/issues",
    "category": "Import-Export"
}

# Import all modules when addon loads
import bpy

from . import operators
from . import parser
from . import converter
from . import exporter
from . import socket_handler
from . import strategies
from . import utils
from . import fbx_helper
from . import ui

def register():
    """Register the addon - called when addon is enabled"""
    
    # Register scene properties for shader type selection
    bpy.types.Scene.unity_shader_type = bpy.props.EnumProperty(
        name="Unity Shader Type",
        description="Type of Unity shader to generate",
        items=[
            ('UNIVERSAL', 'Universal (URP)', 'Universal Render Pipeline'),
            ('BUILTIN', 'Built-in', 'Built-in Render Pipeline'),
            ('CUSTOM_RT', 'Custom Render Texture', 'Custom Render Texture'),
        ],
        default='UNIVERSAL',
    )
    
    operators.register()
    ui.register()
    print("✓ Blender to Unity Shader Converter addon registered")

def unregister():
    """Unregister the addon - called when addon is disabled"""
    operators.unregister()
    ui.unregister()
    
    # Remove scene property
    del bpy.types.Scene.unity_shader_type
    
    print("✓ Blender to Unity Shader Converter addon unregistered")

if __name__ == "__main__":
    register()
