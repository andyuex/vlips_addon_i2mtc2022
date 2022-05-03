import bpy

from vlips_addon.modules.constants import *


class VIEW3D_PT_render(bpy.types.Panel):
    """
    Visible Light Indoor Positioning Simulation: render
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VLIPS"
    bl_label = "Render"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            RENDER_SCENE_OPERATOR_NAME,
            text="Current Scene",
            icon="SCENE"
        )
        column.operator(
            RENDER_CAMERA_MOVEMENT_OPERATOR_NAME,
            text="Camera Movement",
            icon="GIZMO"
        )
        column.operator(
            RENDER_CAMERA_FOV_CORNERS_NAME,
            text="FOV Corners",
            icon="SHADING_BBOX"
        )
