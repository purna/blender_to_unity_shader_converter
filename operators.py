"""
Blender Operator Definition
Handles the "Convert to Unity" operator in the UI
"""

import bpy
from . import parser, converter, exporter, utils

# Load node mappings from JSON at addon startup
NODE_MAPPING = utils.load_node_mappings()

class SHADER_OT_convert_to_unity(bpy.types.Operator):
    """Convert selected object's shader to Unity shader graph"""
    bl_idname = "shader.convert_to_unity"
    bl_label = "Convert to Unity"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export converted shader",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        """Execute the operator"""
        obj = context.active_object
        
        # Validate object and material
        if not obj or not obj.data.materials:
            self.report({'ERROR'}, "No material found on active object")
            return {'CANCELLED'}

        material = obj.data.materials[0]
        if not material.use_nodes:
            self.report({'ERROR'}, "Material does not use shader nodes")
            return {'CANCELLED'}

        try:
            # Parse Blender shader
            print(f"\n📊 Parsing shader: {material.name}")
            parser_instance = parser.BlenderShaderParser(material)
            blender_data = parser_instance.parse()
            print(f"   Nodes: {len(blender_data['nodes'])}")
            print(f"   Connections: {len(blender_data['connections'])}\n")

            # Convert to Unity
            print("🔄 Converting to Unity...")
            converter_instance = converter.ShaderGraphConverter(blender_data, NODE_MAPPING)
            unity_graph = converter_instance.convert()
            
            # Export
            print("💾 Exporting assets...")
            export_instance = exporter.UnityExporter(self.filepath)
            export_instance.setup_folders()
            export_instance.export_shader_graph(unity_graph, material.name)
            export_instance.export_material(material.name, material.name + "_Material")
            export_instance.export_fbx_with_material(obj, material.name)

            print(f"\n✅ Conversion complete!\n")
            self.report({'INFO'}, f"Shader converted to {self.filepath}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Conversion failed: {str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def invoke(self, context, event):
        """Open file browser to select directory"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    """Add operator to Object menu"""
    self.layout.operator(SHADER_OT_convert_to_unity.bl_idname)


def register():
    """Register operator and menu"""
    bpy.utils.register_class(SHADER_OT_convert_to_unity)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    print("  ✓ Operator registered")


def unregister():
    """Unregister operator and menu"""
    bpy.utils.unregister_class(SHADER_OT_convert_to_unity)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    print("  ✓ Operator unregistered")
