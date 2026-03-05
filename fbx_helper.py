"""
FBX Export Helper
Version-aware wrapper around bpy.ops.export_scene.fbx.

Blender 5.0 rewrote the FBX exporter and removed several parameters that
existed in 3.x/4.x:
  - mesh_smooth_type       → removed (normals handled differently)
  - apply_scale_options    → removed
  - bake_space_transform   → removed
  - axis_forward / axis_up → removed (always exports Y-up, Z-forward for Unity)
  - use_custom_properties  → removed
  - apply_unit_scale       → removed (always on)
  - add_leaf_bones         → removed

Parameters that still exist in all supported versions:
  filepath, use_selection, object_types
"""

import bpy


def _blender_version():
    return bpy.app.version  # e.g. (5, 0, 0)


def export_collection_fbx(filepath: str, objects_to_select: list) -> None:
    """
    Export the given objects as FBX, using only parameters valid for the
    running Blender version.
    """
    ver = _blender_version()

    # Shared params available in every supported version
    base_kwargs = dict(
        filepath=filepath,
        use_selection=True,
        object_types={'MESH', 'ARMATURE', 'EMPTY'},
    )

    if ver >= (5, 0, 0):
        # Blender 5.0+ — stripped-down FBX exporter
        bpy.ops.export_scene.fbx(**base_kwargs)
    elif ver >= (4, 0, 0):
        # Blender 4.x
        bpy.ops.export_scene.fbx(
            **base_kwargs,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            add_leaf_bones=False,
            axis_forward='-Z',
            axis_up='Y',
        )
    else:
        # Blender 3.x
        bpy.ops.export_scene.fbx(
            **base_kwargs,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            use_custom_properties=False,
            add_leaf_bones=False,
            axis_forward='-Z',
            axis_up='Y',
        )


def export_single_object_fbx(filepath: str) -> None:
    """
    Export the currently-active selected object as FBX.
    Used for single-mesh exports (exporter.export_fbx_with_material).
    """
    ver = _blender_version()

    base_kwargs = dict(
        filepath=filepath,
        use_selection=True,
        object_types={'MESH'},
    )

    if ver >= (5, 0, 0):
        bpy.ops.export_scene.fbx(**base_kwargs)
    elif ver >= (4, 0, 0):
        bpy.ops.export_scene.fbx(
            **base_kwargs,
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_triangles=True,
            add_leaf_bones=False,
        )
    else:
        bpy.ops.export_scene.fbx(
            **base_kwargs,
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_triangles=True,
            use_custom_properties=False,
            add_leaf_bones=False,
        )
