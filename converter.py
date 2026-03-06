"""
Shader Graph Converter
Main conversion engine – maps Blender node data to Unity ShaderGraph format.

Each Unity node is serialised with:
  - m_ObjectId  : stable GUID
  - m_Type      : fully-qualified Unity type string (from node_mappings.json unity_type)
  - m_Name      : display name
  - m_SerializableSlots : list of input/output port dicts with mapped values
  - conversion_chain    : step-by-step notes from node_mappings.json
"""

import uuid
from typing import Dict, List, Any
from . import socket_handler, strategies, utils


# ── Unity slot helpers ────────────────────────────────────────────────────────

def _make_slot(slot_id: int, display_name: str, slot_type: str,
               value: Any = None, binding: str = 'None') -> Dict:
    """Build a Unity SerializableSlot dict."""
    slot = {
        'm_Id': slot_id,
        'm_DisplayName': display_name,
        'm_SlotType': slot_type,   # '0' = input, '1' = output
        'm_Hidden': False,
        'm_ShaderOutputName': display_name,
        'm_StageCapability': 3,    # vertex + fragment
        'm_Value': _encode_value(value),
        'm_DefaultValue': _encode_value(value),
        'm_Labels': [],
    }
    return slot


def _encode_value(value: Any) -> Dict:
    """Encode a Python value into Unity's serialised value format."""
    if value is None:
        return {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
    if isinstance(value, bool):
        return {'x': float(value)}
    if isinstance(value, (int, float)):
        return {'x': float(value)}
    if isinstance(value, (list, tuple)):
        keys = ['x', 'y', 'z', 'w']
        return {keys[i]: float(v) for i, v in enumerate(value[:4])}
    # String (e.g. texture name) – store as label
    return {'x': 0.0, '_string': str(value)}


def _float_slot(slot_id, name, value=0.0):
    return _make_slot(slot_id, name, '0', value)


def _vec2_slot(slot_id, name, value=(0.0, 0.0)):
    return _make_slot(slot_id, name, '0', list(value) + [0.0, 0.0])


def _color_slot(slot_id, name, value=None):
    v = value if value is not None else [0.0, 0.0, 0.0, 1.0]
    return _make_slot(slot_id, name, '0', v)


def _out_slot(slot_id, name):
    return _make_slot(slot_id, name, '1', None)


# ── Node classes ──────────────────────────────────────────────────────────────

class UnityShaderGraphNode:
    """Represents one node in a Unity Shader Graph."""

    def __init__(self, unity_type: str, unity_name: str, guid: str = None):
        self.guid = guid or str(uuid.uuid4())
        self.unity_type = unity_type        # e.g. "UnityEditor.ShaderGraph.AddNode"
        self.unity_name = unity_name        # display name shown in the graph
        self.slots: List[Dict] = []         # serialised input/output slots
        self.conversion_chain = None        # step notes from JSON

    def add_slot(self, slot: Dict):
        self.slots.append(slot)

    def to_dict(self) -> Dict:
        return {
            'm_ObjectId': self.guid,
            'm_Type': self.unity_type,
            'm_Group': {'m_Id': ''},
            'm_Name': self.unity_name,
            'm_DrawState': {'m_Expanded': True, 'm_Position': {'x': 0, 'y': 0, 'width': 0, 'height': 0}},
            'm_Slots': [{'m_Id': s['m_Id']} for s in self.slots],
            'm_SerializableSlots': self.slots,
            'conversion_chain': self.conversion_chain,
        }


class UnityShaderGraph:
    """Manages a complete Unity Shader Graph."""

    def __init__(self, name: str = "ConvertedShader"):
        self.name = name
        self.guid = str(uuid.uuid4())
        self.nodes: Dict[str, UnityShaderGraphNode] = {}
        self.edges: List[Dict] = []
        self.properties: List[Dict] = []
        self.conversion_chains: Dict = {}

    def add_node(self, unity_type: str, unity_name: str,
                 guid: str = None) -> UnityShaderGraphNode:
        node = UnityShaderGraphNode(unity_type, unity_name, guid)
        self.nodes[node.guid] = node
        return node

    def add_edge(self, from_guid: str, from_slot: int,
                 to_guid: str, to_slot: int):
        self.edges.append({
            'm_OutputSlot': {'m_Node': {'m_Id': from_guid}, 'm_SlotId': from_slot},
            'm_InputSlot':  {'m_Node': {'m_Id': to_guid},  'm_SlotId': to_slot},
        })

    def add_conversion_chain(self, blender_name: str, data: dict):
        if data:
            self.conversion_chains[blender_name] = data


# ── Unity type registry ───────────────────────────────────────────────────────
# Maps the unity_type field from node_mappings.json to the full C# type string
# used in the .shadergraph JSON.

UNITY_TYPE_MAP = {
    'Vector1':           'UnityEditor.ShaderGraph.Vector1MaterialSlot',
    'Float':             'UnityEditor.ShaderGraph.FloatNode',
    'Color':             'UnityEditor.ShaderGraph.ColorNode',
    'SampleTexture2D':   'UnityEditor.ShaderGraph.SampleTexture2DNode',
    'SampleCubemap':     'UnityEditor.ShaderGraph.SampleCubemapNode',
    'UV':                'UnityEditor.ShaderGraph.UVNode',
    'TilingAndOffset':   'UnityEditor.ShaderGraph.TilingAndOffsetNode',
    'Lerp':              'UnityEditor.ShaderGraph.LerpNode',
    'Add':               'UnityEditor.ShaderGraph.AddNode',
    'Multiply':          'UnityEditor.ShaderGraph.MultiplyNode',
    'Subtract':          'UnityEditor.ShaderGraph.SubtractNode',
    'Divide':            'UnityEditor.ShaderGraph.DivideNode',
    'Minimum':           'UnityEditor.ShaderGraph.MinimumNode',
    'Maximum':           'UnityEditor.ShaderGraph.MaximumNode',
    'Clamp':             'UnityEditor.ShaderGraph.ClampNode',
    'Invert':            'UnityEditor.ShaderGraph.OneMinusNode',
    'Split':             'UnityEditor.ShaderGraph.SplitNode',
    'Combine':           'UnityEditor.ShaderGraph.CombineNode',
    'NormalFromTexture': 'UnityEditor.ShaderGraph.NormalReconstructZNode',
    'Fresnel':           'UnityEditor.ShaderGraph.FresnelNode',
    'VertexColor':       'UnityEditor.ShaderGraph.VertexColorNode',
    'Tangent':           'UnityEditor.ShaderGraph.TangentVectorNode',
    'MapRange':          'UnityEditor.ShaderGraph.RemapNode',
    'Noise':             'UnityEditor.ShaderGraph.SimpleNoiseNode',
    'Procedural':        'UnityEditor.ShaderGraph.VoronoiNode',
    'Gamma':             'UnityEditor.ShaderGraph.GammaNode',
    'VertexAttribute':   'UnityEditor.ShaderGraph.VertexColorNode',
    'Fragment':          'UnityEditor.ShaderGraph.MasterStackNode',
    'GroupInput':        'UnityEditor.ShaderGraph.GroupNode',
    'GroupOutput':       'UnityEditor.ShaderGraph.GroupNode',
    'Custom PBR':        'UnityEditor.ShaderGraph.PBRMasterNode',
    # Previously missing entries (unity_type values used in node_mappings.json)
    'Custom':            'UnityEditor.ShaderGraph.CustomFunctionNode',
    'Custom Normal':     'UnityEditor.ShaderGraph.NormalFromHeightNode',
    'Emission':          'UnityEditor.ShaderGraph.EmissionNode',
    'Integer':           'UnityEditor.ShaderGraph.IntegerNode',
    'Normal':            'UnityEditor.ShaderGraph.NormalVectorNode',
    'Position':          'UnityEditor.ShaderGraph.PositionNode',
    'Transparent':       'UnityEditor.ShaderGraph.TransparentNode',
    'Vector3':           'UnityEditor.ShaderGraph.Vector3Node',
    'N/A':               'UnityEditor.ShaderGraph.CustomFunctionNode',  # incompatible nodes
    # New entries for added node support
    'Rotate Vector':     'UnityEditor.ShaderGraph.RotateAboutAxisNode',
    'Vector Transform':  'UnityEditor.ShaderGraph.TransformNode',
    'Bevel':            'UnityEditor.ShaderGraph.BevelNode',
    'SSS':              'UnityEditor.ShaderGraph.CustomFunctionNode',
    'Sheen':            'UnityEditor.ShaderGraph.CustomFunctionNode',
    'Toon':             'UnityEditor.ShaderGraph.CustomFunctionNode',
    'Velvet':           'UnityEditor.ShaderGraph.CustomFunctionNode',
}

MATH_OP_TYPE_MAP = {
    'ADD':        'UnityEditor.ShaderGraph.AddNode',
    'SUBTRACT':   'UnityEditor.ShaderGraph.SubtractNode',
    'MULTIPLY':   'UnityEditor.ShaderGraph.MultiplyNode',
    'DIVIDE':     'UnityEditor.ShaderGraph.DivideNode',
    'POWER':      'UnityEditor.ShaderGraph.PowerNode',
    'LOGARITHM':  'UnityEditor.ShaderGraph.LogNode',
    'SQRT':       'UnityEditor.ShaderGraph.SquareRootNode',
    'ABSOLUTE':   'UnityEditor.ShaderGraph.AbsoluteNode',
    'MINIMUM':    'UnityEditor.ShaderGraph.MinimumNode',
    'MAXIMUM':    'UnityEditor.ShaderGraph.MaximumNode',
    'MODULO':     'UnityEditor.ShaderGraph.ModuloNode',
    'FLOOR':      'UnityEditor.ShaderGraph.FloorNode',
    'CEIL':       'UnityEditor.ShaderGraph.CeilingNode',
    'FRACTION':   'UnityEditor.ShaderGraph.FractionNode',
    'SNAP':       'UnityEditor.ShaderGraph.RoundNode',
    'SINE':       'UnityEditor.ShaderGraph.SineNode',
    'COSINE':     'UnityEditor.ShaderGraph.CosineNode',
    'TANGENT':    'UnityEditor.ShaderGraph.TangentNode',
}

BLEND_MODE_TYPE_MAP = {
    'MIX':        'UnityEditor.ShaderGraph.LerpNode',
    'ADD':        'UnityEditor.ShaderGraph.AddNode',
    'MULTIPLY':   'UnityEditor.ShaderGraph.MultiplyNode',
    'SUBTRACT':   'UnityEditor.ShaderGraph.SubtractNode',
    'DIVIDE':     'UnityEditor.ShaderGraph.DivideNode',
    'DARKEN':     'UnityEditor.ShaderGraph.MinimumNode',
    'LIGHTEN':    'UnityEditor.ShaderGraph.MaximumNode',
    'SCREEN':     'UnityEditor.ShaderGraph.AddNode',   # approximation
    'OVERLAY':    'UnityEditor.ShaderGraph.LerpNode',  # approximation
    'DIFFERENCE': 'UnityEditor.ShaderGraph.SubtractNode',
}


def _resolve_unity_type(unity_type_key: str, node_data: Dict) -> str:
    """Return the full C# type string for a node."""
    # Math nodes: use operation to pick correct Unity type
    if node_data['blender_type'] == 'ShaderNodeMath':
        op = node_data.get('properties', {}).get('operation', 'ADD')
        return MATH_OP_TYPE_MAP.get(op, 'UnityEditor.ShaderGraph.AddNode')

    if node_data['blender_type'] == 'ShaderNodeVectorMath':
        op = node_data.get('properties', {}).get('operation', 'ADD')
        return MATH_OP_TYPE_MAP.get(op, 'UnityEditor.ShaderGraph.AddNode')

    return UNITY_TYPE_MAP.get(unity_type_key,
                              f'UnityEditor.ShaderGraph.{unity_type_key}Node')


# ── Slot builders per node type ───────────────────────────────────────────────

def _build_slots_for_node(node_data: Dict, node_mapping: Dict) -> List[Dict]:
    """
    Build the m_SerializableSlots list for a Unity node, populated with
    actual values extracted from the Blender node_data.
    """
    ntype = node_data['blender_type']
    props = node_data.get('properties', {})
    inputs = node_data.get('inputs', {})

    def inp(name):
        """Shorthand: get default value of a Blender input socket."""
        return inputs.get(name, {}).get('default')

    slots = []

    # ── Output Material / Master Stack ───────────────────────────────
    if ntype == 'ShaderNodeOutputMaterial':
        slots = [
            _make_slot(0, 'Vertex', '0', None),
            _make_slot(1, 'BaseColor', '0', inp('Surface') or [0.8, 0.8, 0.8, 1.0]),
            _make_slot(2, 'Normal', '0', None),
            _make_slot(3, 'Metallic', '0', 0.0),
            _make_slot(4, 'Smoothness', '0', 0.5),
            _make_slot(5, 'Occlusion', '0', 1.0),
            _make_slot(6, 'Emission', '0', [0.0, 0.0, 0.0, 1.0]),
            _make_slot(7, 'Alpha', '0', 1.0),
        ]

    # ── Principled BSDF → PBR Master ─────────────────────────────────
    elif ntype == 'ShaderNodeBsdfPrincipled':
        roughness = inp('Roughness') or 0.5
        smoothness = 1.0 - (float(roughness) if isinstance(roughness, (int, float)) else 0.5)
        emission_color = inp('Emission') or [0.0, 0.0, 0.0, 1.0]
        emission_strength = inp('Emission Strength') or 0.0
        # Scale emission color by strength
        if isinstance(emission_color, list) and isinstance(emission_strength, (int, float)):
            emission_scaled = [c * emission_strength for c in emission_color[:3]] + [1.0]
        else:
            emission_scaled = [0.0, 0.0, 0.0, 1.0]

        slots = [
            _color_slot(0,  'BaseColor',  inp('Base Color')),
            _float_slot(1,  'Metallic',   inp('Metallic') or 0.0),
            _float_slot(2,  'Smoothness', smoothness),
            _make_slot(3,   'Normal',     '0', None),
            _color_slot(4,  'Emission',   emission_scaled),
            _float_slot(5,  'Alpha',      inp('Alpha') or 1.0),
            _float_slot(6,  'Occlusion',  1.0),
            _out_slot(7,    'Out'),
        ]

    # ── Diffuse BSDF ─────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfDiffuse':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Metallic',   0.0),
            _float_slot(2, 'Smoothness', 0.0),
            _out_slot(3,   'Out'),
        ]

    # ── Glossy BSDF ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfGlossy':
        roughness = inp('Roughness') or 0.5
        smoothness = 1.0 - float(roughness)
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Metallic',   1.0),
            _float_slot(2, 'Smoothness', smoothness),
            _out_slot(3,   'Out'),
        ]

    # ── Emission ─────────────────────────────────────────────────────
    # Unity emission is a single HDR color. Bake Blender's Strength into the
    # color intensity so the exported value is immediately usable.
    elif ntype == 'ShaderNodeEmission':
        strength = float(inp('Strength') or 1.0)
        color    = inp('Color') or [1.0, 1.0, 1.0, 1.0]
        if isinstance(color, list):
            emission = [c * strength for c in color[:3]] + [1.0]
        else:
            emission = [strength, strength, strength, 1.0]
        slots = [
            _color_slot(0, 'EmissionColor', emission),
            _out_slot(1,   'Out'),
        ]

    # ── Math node ────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeMath':
        a_val = inp('Value') or inp('Value_001') or 0.0
        b_val = inp('Value_001') or inp('Value_002') or 0.0
        slots = [
            _float_slot(0, 'A', a_val),
            _float_slot(1, 'B', b_val),
            _out_slot(2,   'Out'),
        ]

    # ── Vector Math ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeVectorMath':
        a_val = inp('Vector') or [0.0, 0.0, 0.0]
        b_val = inp('Vector_001') or [0.0, 0.0, 0.0]
        slots = [
            _make_slot(0, 'A', '0', a_val),
            _make_slot(1, 'B', '0', b_val),
            _out_slot(2,  'Out'),
        ]

    # ── Value (Float constant) ────────────────────────────────────────
    # ShaderNodeValue has no input sockets in Blender — the value lives on
    # the output socket's default_value, which parser.py stores in outputs.
    elif ntype == 'ShaderNodeValue':
        raw = node_data.get('outputs', {}).get('Value', {}).get('default', 0.0)
        val = float(raw) if isinstance(raw, (int, float)) else 0.0
        slots = [
            _float_slot(0, 'Out', val),
        ]

    # ── RGB (Color constant) ─────────────────────────────────────────
    elif ntype == 'ShaderNodeRGB':
        color = node_data.get('outputs', {}).get('Color', {}).get('default') or [1.0, 1.0, 1.0, 1.0]
        slots = [
            _color_slot(0, 'Out', color),
        ]

    # ── Texture Image ─────────────────────────────────────────────────
    # Unity SampleTexture2DNode port order: Texture(0 in), UV(1 in),
    # RGBA(2 out), R(3 out), G(4 out), B(5 out), A(6 out)
    elif ntype == 'ShaderNodeTexImage':
        slots = [
            _make_slot(0, 'Texture', '0', None),   # asset assigned manually
            _make_slot(1, 'UV',      '0', None),
            _out_slot(2,  'RGBA'),
            _out_slot(3,  'R'),
            _out_slot(4,  'G'),
            _out_slot(5,  'B'),
            _out_slot(6,  'Alpha'),
        ]

    # ── Texture Coordinate ───────────────────────────────────────────
    elif ntype == 'ShaderNodeTexCoord':
        slots = [
            _out_slot(0, 'UV'),
            _out_slot(1, 'Normal'),
            _out_slot(2, 'Object'),
            _out_slot(3, 'Camera'),
            _out_slot(4, 'Window'),
            _out_slot(5, 'Reflection'),
        ]

    # ── UV Map ───────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeUVMap':
        slots = [
            _make_slot(0, 'Channel', '0', 0.0),  # UV channel index
            _out_slot(1,  'Out'),
        ]

    # ── Mapping (Tiling and Offset) ──────────────────────────────────
    elif ntype == 'ShaderNodeMapping':
        location = props.get('location', [0.0, 0.0, 0.0])
        scale    = props.get('scale',    [1.0, 1.0, 1.0])
        slots = [
            _make_slot(0, 'UV',     '0', None),
            _vec2_slot(1, 'Tiling', (scale[0],    scale[1])),
            _vec2_slot(2, 'Offset', (location[0], location[1])),
            _out_slot(3,  'Out'),
        ]

    # ── Normal Map ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeNormalMap':
        strength = inp('Strength') or 1.0
        slots = [
            _make_slot(0, 'Texture', '0', None),
            _float_slot(1, 'Strength', strength),
            _out_slot(2,  'Out'),
        ]

    # ── Bump ─────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBump':
        strength = inp('Strength') or 1.0
        slots = [
            _make_slot(0, 'In',       '0', None),
            _float_slot(1, 'Strength', strength),
            _out_slot(2,  'Out'),
        ]

    # ── Mix RGB / Lerp ───────────────────────────────────────────────
    elif ntype == 'ShaderNodeMixRGB':
        fac = inp('Fac') or 0.5
        col1 = inp('Color1') or [0.0, 0.0, 0.0, 1.0]
        col2 = inp('Color2') or [1.0, 1.0, 1.0, 1.0]
        slots = [
            _float_slot(0,  'T', fac),
            _color_slot(1,  'A', col1),
            _color_slot(2,  'B', col2),
            _out_slot(3,    'Out'),
        ]

    # ── Mix (Blender 3.4+) ────────────────────────────────────────────
    # ShaderNodeMix uses 'blend_type' (not 'blend_mode' like the older MixRGB)
    elif ntype == 'ShaderNodeMix':
        fac = inp('Factor') or inp('Factor_Float') or 0.5
        a   = inp('A') or inp('A_Float') or inp('A_Vector') or 0.0
        b   = inp('B') or inp('B_Float') or inp('B_Vector') or 0.0
        slots = [
            _float_slot(0, 'T', fac),
            _make_slot(1,  'A', '0', a),
            _make_slot(2,  'B', '0', b),
            _out_slot(3,   'Out'),
        ]

    # ── Clamp ────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeClamp':
        slots = [
            _float_slot(0, 'In',  inp('Value') or 0.0),
            _float_slot(1, 'Min', inp('Min')   or 0.0),
            _float_slot(2, 'Max', inp('Max')   or 1.0),
            _out_slot(3,  'Out'),
        ]

    # ── Invert ───────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeInvert':
        slots = [
            _float_slot(0, 'In', inp('Color') or 0.0),
            _out_slot(1,  'Out'),
        ]

    # ── Separate RGB / XYZ ───────────────────────────────────────────
    elif ntype in ('ShaderNodeSeparateRGB', 'ShaderNodeSeparateXYZ'):
        val = inp('Image') or inp('Vector') or [0.0, 0.0, 0.0]
        slots = [
            _make_slot(0, 'In', '0', val),
            _out_slot(1, 'R' if 'RGB' in ntype else 'X'),
            _out_slot(2, 'G' if 'RGB' in ntype else 'Y'),
            _out_slot(3, 'B' if 'RGB' in ntype else 'Z'),
        ]

    # ── Combine RGB / XYZ ────────────────────────────────────────────
    elif ntype in ('ShaderNodeCombineRGB', 'ShaderNodeCombineXYZ'):
        labels = ('R', 'G', 'B') if 'RGB' in ntype else ('X', 'Y', 'Z')
        slots = [
            _float_slot(0, labels[0], inp(labels[0]) or 0.0),
            _float_slot(1, labels[1], inp(labels[1]) or 0.0),
            _float_slot(2, labels[2], inp(labels[2]) or 0.0),
            _out_slot(3,  'Out'),
        ]

    # ── Fresnel ──────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeFresnel':
        ior = inp('IOR') or 1.45
        # Convert IOR to Unity Fresnel power: power ≈ 5 / IOR
        power = round(5.0 / float(ior), 3) if ior else 3.3
        slots = [
            _float_slot(0, 'Power', power),
            _out_slot(1,  'Out'),
        ]

    # ── Layer Weight ─────────────────────────────────────────────────
    elif ntype == 'ShaderNodeLayerWeight':
        blend = inp('Blend') or 0.5
        power = max(1.0, round(10.0 * float(blend), 2))
        slots = [
            _float_slot(0, 'Power', power),
            _out_slot(1,  'Out'),
        ]

    # ── Map Range / Remap ────────────────────────────────────────────
    elif ntype == 'ShaderNodeMapRange':
        slots = [
            _float_slot(0, 'In',     inp('Value') or 0.0),
            _float_slot(1, 'InMin',  inp('From Min') or 0.0),
            _float_slot(2, 'InMax',  inp('From Max') or 1.0),
            _float_slot(3, 'OutMin', inp('To Min')   or 0.0),
            _float_slot(4, 'OutMax', inp('To Max')   or 1.0),
            _out_slot(5,  'Out'),
        ]

    # ── Vertex Color ─────────────────────────────────────────────────
    elif ntype == 'ShaderNodeVertexColor':
        slots = [
            _out_slot(0, 'Color'),
            _out_slot(1, 'Alpha'),
        ]

    # ── Gamma / Power ────────────────────────────────────────────────
    elif ntype == 'ShaderNodeGamma':
        slots = [
            _make_slot(0, 'In',    '0', inp('Color') or [0.0, 0.0, 0.0, 1.0]),
            _float_slot(1, 'Power', inp('Gamma') or 2.2),
            _out_slot(2,  'Out'),
        ]

    # ── Bright/Contrast ──────────────────────────────────────────────
    elif ntype == 'ShaderNodeBrightContrast':
        bright   = inp('Bright')   or 0.0
        contrast = inp('Contrast') or 1.0
        slots = [
            _make_slot(0, 'In',       '0', inp('Color') or [0.0, 0.0, 0.0, 1.0]),
            _float_slot(1, 'Contrast', contrast),
            _float_slot(2, 'Brightness', bright),
            _out_slot(3,  'Out'),
        ]

    # ── Hue Saturation ───────────────────────────────────────────────
    elif ntype == 'ShaderNodeHueSaturation':
        slots = [
            _make_slot(0, 'In',         '0', inp('Color') or [0.0, 0.0, 0.0, 1.0]),
            _float_slot(1, 'Hue',        inp('Hue')        or 0.5),
            _float_slot(2, 'Saturation', inp('Saturation') or 1.0),
            _float_slot(3, 'Value',      inp('Value')      or 1.0),
            _float_slot(4, 'Blend',      inp('Fac')        or 1.0),
            _out_slot(5,  'Out'),
        ]

    # ── Add Shader / Mix Shader ───────────────────────────────────────
    elif ntype == 'ShaderNodeAddShader':
        slots = [
            _make_slot(0, 'A', '0', None),
            _make_slot(1, 'B', '0', None),
            _out_slot(2,  'Out'),
        ]

    elif ntype == 'ShaderNodeMixShader':
        fac = inp('Fac') or 0.5
        slots = [
            _float_slot(0, 'T', fac),
            _make_slot(1,  'A', '0', None),
            _make_slot(2,  'B', '0', None),
            _out_slot(3,   'Out'),
        ]

    # ── Noise Texture ────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexNoise':
        scale = inp('Scale') or 5.0
        slots = [
            _make_slot(0, 'UV',    '0', None),
            _float_slot(1, 'Scale', scale),
            _out_slot(2,  'Out'),
            _out_slot(3,  'Color'),
        ]

    # ── Voronoi Texture ──────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexVoronoi':
        scale = inp('Scale') or 5.0
        slots = [
            _make_slot(0, 'UV',         '0', None),
            _float_slot(1, 'CellDensity', scale),
            _float_slot(2, 'AngleOffset', inp('Randomness') or 1.0),
            _out_slot(3,  'Out'),
        ]

    # ── Geometry (NewGeometry) ────────────────────────────────────────
    elif ntype == 'ShaderNodeNewGeometry':
        slots = [
            _out_slot(0, 'Position'),
            _out_slot(1, 'Normal'),
            _out_slot(2, 'Tangent'),
            _out_slot(3, 'Incoming'),
            _out_slot(4, 'Parametric'),
        ]

    # ── Normal input ─────────────────────────────────────────────────
    elif ntype == 'ShaderNodeNormal':
        normal_val = inp('Normal') or [0.0, 0.0, 1.0]
        slots = [
            _make_slot(0, 'In',  '0', normal_val),
            _out_slot(1,  'Out'),
        ]

    # ── Reroute (pass-through) ────────────────────────────────────────
    elif ntype == 'ShaderNodeReroute':
        slots = [
            _make_slot(0, 'Input',  '0', None),
            _out_slot(1,  'Output'),
        ]

    # ── Tangent ──────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTangent':
        slots = [_out_slot(0, 'Out')]

    # ── Blackbody ────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBlackbody':
        temp = inp('Temperature') or 3200.0
        slots = [
            _float_slot(0, 'Temperature', temp),
            _out_slot(1,  'Color'),
        ]

    # ── Color Ramp ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeColorRamp':
        slots = [
            _float_slot(0, 'Time', inp('Fac') or 0.5),
            _out_slot(1,  'Out'),
        ]

    # ── Transparent BSDF ─────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfTransparent':
        slots = [
            _float_slot(0, 'Alpha', inp('Fac') or 1.0),
            _out_slot(1,  'Out'),
        ]

    # ── Glass / Refraction ───────────────────────────────────────────
    elif ntype in ('ShaderNodeBsdfGlass', 'ShaderNodeBsdfRefraction'):
        roughness = inp('Roughness') or 0.0
        smoothness = 1.0 - float(roughness)
        slots = [
            _color_slot(0, 'BaseColor',  inp('Color')),
            _float_slot(1, 'Smoothness', smoothness),
            _float_slot(2, 'IOR',        inp('IOR') or 1.45),
            _out_slot(3,  'Out'),
        ]

    # ── SSS ───────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeSubsurfaceScattering':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Subsurface', inp('Subsurface') or 0.0),
            _float_slot(2, 'Radius', 1.0),
            _out_slot(3,  'Out'),
        ]

    # ── Sheen ─────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfSheen':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Sheen', inp('Sheen') or 0.0),
            _out_slot(2,  'Out'),
        ]

    # ── Toon ──────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfToon':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Smoothness', inp('Smoothness') or 0.5),
            _out_slot(2,  'Out'),
        ]

    # ── Velvet ─────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBsdfVelvet':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Sheen', inp('Sheen') or 0.0),
            _out_slot(2,  'Out'),
        ]

    # ── Hair BSDF ──────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeHairBsdf':
        slots = [
            _color_slot(0, 'BaseColor', inp('Color')),
            _float_slot(1, 'Roughness', inp('Roughness') or 0.5),
            _out_slot(2,  'Out'),
        ]

    # ── Separate HSV ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeSeparateHSV':
        slots = [
            _make_slot(0, 'In', '0', inp('Color') or [0.0, 0.0, 0.0, 1.0]),
            _out_slot(1, 'H'),
            _out_slot(2, 'S'),
            _out_slot(3, 'V'),
        ]

    # ── Combine HSV ────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeCombineHSV':
        slots = [
            _float_slot(0, 'H', inp('H') or 0.0),
            _float_slot(1, 'S', inp('S') or 0.0),
            _float_slot(2, 'V', inp('V') or 1.0),
            _out_slot(3,  'Out'),
        ]

    # ── Vector Curve ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeVectorCurve':
        slots = [
            _make_slot(0, 'Vector', '0', inp('Vector') or [0.0, 0.0, 0.0]),
            _out_slot(1,  'Out'),
        ]

    # ── Gradient Texture ───────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexGradient':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _out_slot(1,  'Fac'),
        ]

    # ── Wave Texture ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexWave':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _float_slot(1, 'Scale', inp('Scale') or 5.0),
            _float_slot(2, 'Distortion', inp('Distortion') or 0.0),
            _out_slot(3,  'Fac'),
        ]

    # ── Brick Texture ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexBrick':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _float_slot(1, 'Scale', inp('Scale') or 5.0),
            _out_slot(2,  'Fac'),
            _out_slot(3,  'Color1'),
            _out_slot(4,  'Color2'),
        ]

    # ── Checker Texture ────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexChecker':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _out_slot(1,  'Fac'),
        ]

    # ── Magic Texture ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexMagic':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _float_slot(1, 'Scale', inp('Scale') or 5.0),
            _out_slot(2,  'Fac'),
        ]

    # ── Sky Texture ────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeTexSky':
        slots = [
            _out_slot(0,  'Color'),
        ]

    # ── White Noise Texture ───────────────────────────────────────────
    elif ntype == 'ShaderNodeTexWhiteNoise':
        slots = [
            _make_slot(0, 'UV', '0', None),
            _float_slot(1, 'W', inp('W') or 1.0),
            _out_slot(2,  'Fac'),
        ]

    # ── Bevel ──────────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeBevel':
        slots = [
            _float_slot(0, 'Radius', inp('Radius') or 0.0),
            _out_slot(1,  'Normal'),
        ]

    # ── Object Info ────────────────────────────────────────────────────
    elif ntype == 'ShaderNodeObjectInfo':
        slots = [
            _out_slot(0,  'Location'),
            _out_slot(1,  'Color'),
            _out_slot(2,  'Random'),
        ]

    # ── Camera Data ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeCameraData':
        slots = [
            _out_slot(0,  'View Vector'),
            _out_slot(1,  'View Distance'),
        ]

    # ── Vector Rotate ──────────────────────────────────────────────────
    elif ntype == 'ShaderNodeVectorRotate':
        slots = [
            _make_slot(0, 'Vector', '0', inp('Vector') or [0.0, 0.0, 0.0]),
            _make_slot(1, 'Axis', '0', inp('Axis') or [0.0, 0.0, 1.0]),
            _float_slot(2, 'Angle', inp('Angle') or 0.0),
            _out_slot(3,  'Out'),
        ]

    # ── Vector Transform ────────────────────────────────────────────────
    elif ntype == 'ShaderNodeVectorTransform':
        slots = [
            _make_slot(0, 'Vector', '0', inp('Vector') or [0.0, 0.0, 0.0]),
            _out_slot(1,  'Out'),
        ]

    # ── Displacement ───────────────────────────────────────────────────
    elif ntype == 'ShaderNodeDisplacement':
        slots = [
            _make_slot(0, 'Height', '0', None),
            _float_slot(1, 'Midlevel', inp('Midlevel') or 0.5),
            _float_slot(2, 'Scale', inp('Scale') or 1.0),
            _out_slot(3,  'Displacement'),
        ]

    # ── Fallback: generic A + B + Out ────────────────────────────────
    else:
        slots = []
        slot_id = 0
        for in_name, in_data in node_data.get('inputs', {}).items():
            val = in_data.get('default')
            slots.append(_make_slot(slot_id, in_name, '0', val))
            slot_id += 1
        for out_name in node_data.get('outputs', {}):
            slots.append(_out_slot(slot_id, out_name))
            slot_id += 1

    return slots


# ── Module-level constants ────────────────────────────────────────────────────

# Strategies that produce a usable Unity node (even if approximate).
# Defined once here instead of being recreated inside _convert_node on every call.
_CONVERTIBLE_STRATEGIES = frozenset({
    'direct', 'decompose', 'blend_mapping', 'normal_mapping',
    'texture_reference', 'attribute_mapping', 'uv_mapping',
    'procedural_texture', 'approximation', 'bump_to_normal',
    'vertex_displacement', 'custom_attribute',
})

# ── Main converter ────────────────────────────────────────────────────────────

class ShaderGraphConverter:
    """Convert Blender shader graph to Unity format."""

    def __init__(self, blender_shader_data: Dict, node_mapping: Dict):
        self.blender_data = blender_shader_data
        self.unity_graph = UnityShaderGraph(blender_shader_data['name'])
        self.node_guid_map: Dict[str, str] = {}
        self.node_mapping = node_mapping
        self.conversion_warnings: List[str] = []
        self.conversion_report = {
            'nodes_converted': 0,
            'nodes_decomposed': 0,
            'nodes_approximated': 0,
            'nodes_incompatible': 0,
            'connections_validated': 0,
            'type_mismatches': 0,
        }

    def convert(self) -> UnityShaderGraph:
        print("\n" + "="*70)
        print("BLENDER TO UNITY SHADER CONVERSION")
        print("="*70 + "\n")

        for node_data in self.blender_data['nodes']:
            self._convert_node(node_data)

        for conn in self.blender_data['connections']:
            self._convert_connection(conn)

        self._generate_conversion_report()
        return self.unity_graph

    def _convert_node(self, node_data: Dict):
        ntype = node_data['blender_type']
        guid  = str(uuid.uuid4())
        # Blender guarantees node names are unique within a node tree
        # (duplicates get suffixes like ".001"), so a plain name→guid dict is safe
        # and gives O(1) lookups in _convert_connection.
        self.node_guid_map[node_data['name']] = guid

        mapping  = self.node_mapping.get(ntype, {})
        strategy = mapping.get('strategy', 'incompatible')
        unity_name = mapping.get('unity_name', ntype)
        unity_type_key = mapping.get('unity_type', 'Custom')
        compat   = mapping.get('compatibility', '0%')
        unity_chain = mapping.get('unity_chain', None)

        # Resolve the full C# type string
        full_type = _resolve_unity_type(unity_type_key, node_data)

        # Build slots from actual Blender values
        slots = _build_slots_for_node(node_data, mapping)

        if strategy in _CONVERTIBLE_STRATEGIES:
            node = self.unity_graph.add_node(full_type, unity_name, guid)
            for s in slots:
                node.add_slot(s)
            node.conversion_chain = unity_chain

            # Extra properties stored on the node dict for the exporter
            node.blender_props = {
                'blender_type': ntype,
                'operation':    node_data.get('properties', {}).get('operation'),
                'blend_mode':   node_data.get('properties', {}).get('blend_mode'),
                'image_name':   node_data.get('properties', {}).get('image_name'),
                'image_path':   node_data.get('properties', {}).get('image_path'),
                'colorspace':   node_data.get('properties', {}).get('colorspace'),
                'uv_map':       node_data.get('properties', {}).get('uv_map'),
                'tiling':       node_data.get('properties', {}).get('scale', [1,1,1])[:2],
                'offset':       node_data.get('properties', {}).get('location', [0,0,0])[:2],
            }

            if strategy == 'direct':
                self.conversion_report['nodes_converted'] += 1
                print(f"✓ {node_data['name']:30} → {unity_name:25} [{compat}]")
            elif strategy == 'decompose':
                self.conversion_report['nodes_decomposed'] += 1
                print(f"⊕ {node_data['name']:30} → {unity_name:25} [{compat}]")
            else:
                self.conversion_report['nodes_approximated'] += 1
                print(f"≈ {node_data['name']:30} → {unity_name:25} [{compat}]")

        elif strategy == 'bake_only':
            node = self.unity_graph.add_node(full_type, unity_name, guid)
            for s in slots:
                node.add_slot(s)
            node.conversion_chain = unity_chain
            node.blender_props = {}
            self.conversion_report['nodes_incompatible'] += 1
            desc = unity_chain.get('description', 'See steps in JSON') if unity_chain else ''
            self.conversion_warnings.append(
                f"BAKE REQUIRED: {node_data['name']} ({ntype}) – {desc}"
            )
            print(f"✗ {node_data['name']:30} → BAKE REQUIRED           [{compat}]")

        elif strategy == 'incompatible':
            node = self.unity_graph.add_node(
                'UnityEditor.ShaderGraph.CustomFunctionNode',
                f'UNSUPPORTED: {ntype}', guid
            )
            node.conversion_chain = unity_chain
            node.blender_props = {}
            self.conversion_report['nodes_incompatible'] += 1
            note = ''
            if unity_chain and unity_chain.get('steps'):
                note = unity_chain['steps'][0].get('note', '')
            self.conversion_warnings.append(
                f"MANUAL: {node_data['name']} ({ntype}) – {note}"
            )
            print(f"✗ {node_data['name']:30} → UNSUPPORTED               [{compat}]")

        else:
            node = self.unity_graph.add_node(
                'UnityEditor.ShaderGraph.CustomFunctionNode',
                f'UNKNOWN: {ntype}', guid
            )
            node.conversion_chain = None
            node.blender_props = {}
            self.conversion_report['nodes_incompatible'] += 1
            self.conversion_warnings.append(
                f"UNKNOWN STRATEGY '{strategy}': {node_data['name']} ({ntype})"
            )
            print(f"✗ {node_data['name']:30} → UNKNOWN STRATEGY         [{compat}]")

        # Store conversion chain summary on the graph
        if unity_chain:
            self.unity_graph.add_conversion_chain(node_data['name'], {
                'blender_node':  node_data['name'],
                'blender_type':  ntype,
                'unity_name':    unity_name,
                'unity_type':    full_type,
                'strategy':      strategy,
                'compatibility': compat,
                'description':   unity_chain.get('description', ''),
                'steps':         unity_chain.get('steps', []),
                'blender_notes': unity_chain.get('blender_conversion_notes', ''),
            })

    def _convert_connection(self, conn: Dict):
        from_guid = self.node_guid_map.get(conn['from_node'])
        to_guid   = self.node_guid_map.get(conn['to_node'])

        if not (from_guid and to_guid):
            return

        is_compat, method = socket_handler.SocketTypeHandler.check_compatibility(
            conn['from_type'], conn['to_type']
        )

        if is_compat:
            # Use slot IDs: find the output slot on 'from' node and input slot on 'to' node
            from_node = self.unity_graph.nodes.get(from_guid)
            to_node   = self.unity_graph.nodes.get(to_guid)
            from_slot_id = self._find_output_slot(from_node, conn['from_socket'])
            to_slot_id   = self._find_input_slot(to_node,   conn['to_socket'])

            self.unity_graph.add_edge(from_guid, from_slot_id, to_guid, to_slot_id)
            self.conversion_report['connections_validated'] += 1

            if method != 'direct':
                print(f"  ↔ {conn['from_node']:20} → {conn['to_node']:20} [{method}]")
        else:
            self.conversion_report['type_mismatches'] += 1
            warn = (f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']}) "
                    f"→ {conn['to_node']}.{conn['to_socket']} ({conn['to_type']})")
            self.conversion_warnings.append(warn)
            print(f"  ⚠ Type mismatch: {warn}")

    @staticmethod
    def _find_output_slot(node: UnityShaderGraphNode, socket_name: str) -> int:
        """Return the slot ID of the output slot best matching socket_name."""
        if node is None:
            return 0
        # 1. Exact case-insensitive name match
        for s in node.slots:
            if s['m_SlotType'] == '1' and s['m_DisplayName'].lower() == socket_name.lower():
                return s['m_Id']
        # 2. First output slot (any name)
        for s in node.slots:
            if s['m_SlotType'] == '1':
                return s['m_Id']
        return 0

    @staticmethod
    def _find_input_slot(node: UnityShaderGraphNode, socket_name: str) -> int:
        """Return the slot ID of the input slot best matching socket_name."""
        if node is None:
            return 0
        # 1. Exact case-insensitive name match
        for s in node.slots:
            if s['m_SlotType'] == '0' and s['m_DisplayName'].lower() == socket_name.lower():
                return s['m_Id']
        # 2. First input slot (any name)
        for s in node.slots:
            if s['m_SlotType'] == '0':
                return s['m_Id']
        return 0

    def _generate_conversion_report(self):
        print("\n" + "="*70)
        print("CONVERSION SUMMARY")
        print("="*70)
        print(f"Nodes converted (direct):    {self.conversion_report['nodes_converted']}")
        print(f"Nodes decomposed:            {self.conversion_report['nodes_decomposed']}")
        print(f"Nodes approximated:          {self.conversion_report['nodes_approximated']}")
        print(f"Nodes incompatible:          {self.conversion_report['nodes_incompatible']}")
        print(f"Connections validated:       {self.conversion_report['connections_validated']}")
        print(f"Type mismatches detected:    {self.conversion_report['type_mismatches']}")
        print("="*70 + "\n")

        if self.conversion_warnings:
            print("WARNINGS & REVIEW ITEMS:")
            for w in self.conversion_warnings:
                print(f"  ⚠ {w}")
            print()
