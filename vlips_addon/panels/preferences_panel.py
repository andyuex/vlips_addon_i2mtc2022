import bpy

from vlips_addon.modules.constants import *


class VIEW3D_PT_preferences(bpy.types.Panel):
    """
    Visible Light Indoor Positioning Simulation: preferences panel
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VLIPS"
    bl_label = "Preferences"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            SETUP_SCENE_OPERATOR_NAME,
            text="Scene",
            icon="TOOL_SETTINGS"
        )
        column.operator(
            SETUP_ROOM_OPERATOR_NAME,
            text="Room",
            icon="CUBE"
        )
        column.operator(
            SETUP_BEACON_OPERATOR_NAME,
            text="Beacon",
            icon="OUTLINER_DATA_LIGHTPROBE"
        )
        column.operator(
            SETUP_CAMERA_OPERATOR_NAME,
            text="Camera",
            icon="CAMERA_DATA"
        )
        column.operator(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME,
            text="Camera Movement",
            icon="GIZMO"
        )
