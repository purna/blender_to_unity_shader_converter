"""
Blender UI Panels
Shows conversion analysis and warnings before export
"""

import bpy
from . import parser, converter, utils

class SHADER_PT_conversion_analysis(bpy.types.Panel):
    """Panel showing shader conversion analysis"""
    bl_label = "Shader Conversion Analysis"
    bl_idname = "SHADER_PT_conversion_analysis"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    @classmethod
    def poll(cls, context):
        """Show panel only if material with shader nodes is selected"""
        if not context.material:
            return False
        return context.material.use_nodes
    
    def draw(self, context):
        """Draw the panel"""
        layout = self.layout
        material = context.material
        
        if not material or not material.use_nodes:
            layout.label(text="No shader material selected")
            return
        
        # Title
        layout.label(text="Shader Conversion Preview", icon='INFO')
        layout.separator()
        
        # Load node mappings
        try:
            node_mapping = utils.load_node_mappings()
        except Exception as e:
            layout.label(text=f"Error loading node data: {str(e)}", icon='ERROR')
            return
        
        # Parse the shader
        try:
            parser_instance = parser.BlenderShaderParser(material)
            blender_data = parser_instance.parse()
        except Exception as e:
            layout.label(text=f"Error parsing shader: {str(e)}", icon='ERROR')
            return
        
        # Analyze compatibility
        analysis = self._analyze_shader(blender_data, node_mapping)
        
        # Display statistics
        self._draw_statistics(layout, analysis)
        
        # Display nodes
        self._draw_node_analysis(layout, analysis, node_mapping)
        
        # Display warnings
        if analysis['warnings']:
            self._draw_warnings(layout, analysis)
        
        # Display conversion recommendations
        if analysis['incompatible_nodes']:
            self._draw_recommendations(layout, analysis)
        
        layout.separator()
        
        # Export button
        row = layout.row()
        row.scale_y = 1.5
        row.operator("shader.convert_to_unity", text="Export to Unity", icon='EXPORT')

    @staticmethod
    def _analyze_shader(blender_data, node_mapping):
        """Analyze shader and return analysis data"""
        analysis = {
            'total_nodes': len(blender_data['nodes']),
            'direct_nodes': 0,
            'decompose_nodes': 0,
            'approximation_nodes': 0,
            'incompatible_nodes': [],
            'type_mismatches': [],
            'warnings': [],
            'success_rate': 0
        }
        
        # Analyze each node
        for node_data in blender_data['nodes']:
            node_type = node_data['blender_type']
            node_mapping_data = node_mapping.get(node_type, {})
            strategy = node_mapping_data.get('strategy', 'incompatible')
            
            if strategy == 'direct':
                analysis['direct_nodes'] += 1
            elif strategy == 'decompose':
                analysis['decompose_nodes'] += 1
            elif strategy in ['approximation', 'blend_mapping', 'normal_mapping', 'uv_mapping', 'texture_reference']:
                analysis['approximation_nodes'] += 1
            else:
                analysis['incompatible_nodes'].append({
                    'name': node_data['name'],
                    'type': node_type,
                    'reason': node_mapping_data.get('description', 'Unknown')
                })
                analysis['warnings'].append(f"{node_data['name']} ({node_type}) - No direct Unity equivalent")
        
        # Analyze connections for type mismatches
        from . import socket_handler
        for conn in blender_data['connections']:
            is_compat, method = socket_handler.SocketTypeHandler.check_compatibility(
                conn['from_type'], conn['to_type']
            )
            if not is_compat:
                analysis['type_mismatches'].append({
                    'from': f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']})",
                    'to': f"{conn['to_node']}.{conn['to_socket']} ({conn['to_type']})"
                })
                analysis['warnings'].append(
                    f"Type mismatch: {conn['from_type']} → {conn['to_type']}"
                )
        
        # Calculate success rate
        convertible = analysis['direct_nodes'] + analysis['decompose_nodes'] + analysis['approximation_nodes']
        if analysis['total_nodes'] > 0:
            analysis['success_rate'] = int((convertible / analysis['total_nodes']) * 100)
        
        return analysis

    @staticmethod
    def _draw_statistics(layout, analysis):
        """Draw conversion statistics"""
        box = layout.box()
        
        # Overall success rate
        row = box.row()
        row.label(text="Conversion Success Rate:")
        row.label(text=f"{analysis['success_rate']}%", icon='CHECKMARK')
        
        # Node breakdown
        row = box.row()
        row.label(text=f"Total Nodes: {analysis['total_nodes']}")
        
        col = box.column()
        col.label(text="Node Breakdown:", icon='NODE')
        
        row = col.row()
        row.label(text=f"  ✓ Direct: {analysis['direct_nodes']}")
        row.label(text=f"  ⊕ Decompose: {analysis['decompose_nodes']}")
        
        row = col.row()
        row.label(text=f"  ≈ Approximated: {analysis['approximation_nodes']}")
        row.label(text=f"  ✗ Incompatible: {len(analysis['incompatible_nodes'])}")

    @staticmethod
    def _draw_node_analysis(layout, analysis, node_mapping):
        """Draw detailed node analysis"""
        if analysis['incompatible_nodes']:
            box = layout.box()
            box.label(text="⚠ Incompatible Nodes", icon='ERROR')
            
            for node_info in analysis['incompatible_nodes']:
                row = box.row()
                row.label(text=f"  • {node_info['name']}", icon='NODE')
                row.label(text=f"({node_info['type']})")

    @staticmethod
    def _draw_warnings(layout, analysis):
        """Draw warnings"""
        if analysis['warnings']:
            box = layout.box()
            box.label(text=f"⚠ Warnings ({len(analysis['warnings'])})", icon='INFO')
            
            # Show first few warnings
            for i, warning in enumerate(analysis['warnings'][:5]):
                row = box.row()
                row.label(text=f"  {warning}")
            
            if len(analysis['warnings']) > 5:
                row = box.row()
                row.label(text=f"  ... and {len(analysis['warnings']) - 5} more warnings")

    @staticmethod
    def _draw_recommendations(layout, analysis):
        """Draw recommendations for fixing issues"""
        box = layout.box()
        box.label(text="💡 Recommendations", icon='INFO')
        
        recommendations = []
        
        if analysis['incompatible_nodes']:
            recommendations.append("Remove or replace incompatible nodes")
        
        if analysis['type_mismatches']:
            recommendations.append("Check socket type connections (may need converter nodes)")
        
        if analysis['success_rate'] < 70:
            recommendations.append("Consider simplifying the shader for better compatibility")
        
        for rec in recommendations[:3]:
            row = box.row()
            row.label(text=f"  • {rec}")


class SHADER_UL_node_list(bpy.types.UIList):
    """UIList for displaying nodes"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Draw node list item"""
        row = layout.row()
        row.label(text=f"{item['name']}", icon='NODE')
        row.label(text=f"({item['type']})")


def register():
    """Register UI panels"""
    bpy.utils.register_class(SHADER_PT_conversion_analysis)
    bpy.utils.register_class(SHADER_UL_node_list)
    print("  ✓ UI panels registered")


def unregister():
    """Unregister UI panels"""
    bpy.utils.unregister_class(SHADER_PT_conversion_analysis)
    bpy.utils.unregister_class(SHADER_UL_node_list)
    print("  ✓ UI panels unregistered")
