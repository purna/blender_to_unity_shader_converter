"""
Blender to Unity Shader Graph Converter
Multi-file addon package with JSON node database
"""

bl_info = {
    "name": "Blender to Unity Shader Converter",
    "author": "Shader Converter Team",
    "version": (0, 3, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Convert to Unity",
    "description": "Convert Blender shader graphs to Unity shader graphs. Supports 78+ nodes with JSON-based conversion strategies.",
    "warning": "Production-Ready",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

# Import all modules when addon loads
from . import operators
from . import parser
from . import converter
from . import exporter
from . import socket_handler
from . import strategies
from . import utils

def register():
    """Register the addon - called when addon is enabled"""
    operators.register()
    print("✓ Blender to Unity Shader Converter addon registered")

def unregister():
    """Unregister the addon - called when addon is disabled"""
    operators.unregister()
    print("✓ Blender to Unity Shader Converter addon unregistered")

if __name__ == "__main__":
    register()
