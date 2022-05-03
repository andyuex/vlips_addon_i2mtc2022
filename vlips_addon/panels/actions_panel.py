import bpy

from vlips_addon.modules.constants import *


class VIEW3D_PT_actions(bpy.types.Panel):
    """
    Visible Light Indoor Positioning Simulation: actions panel
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VLIPS"
    bl_label = "Actions"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            EMPTY_SCENE_OPERATOR_NAME,
            text="Empty Scene",
            icon="TRASH"
        )
        column.operator(
            CREATE_SCENE_OPERATOR_NAME,
            text="Create Simulation",
            icon="WORLD"
        )
        column.operator(
            LOAD_SETTINGS_OPERATOR_NAME,
            text="Load Settings",
            icon="IMPORT"
        )
        column.operator(
            SAVE_SETTINGS_OPERATOR_NAME,
            text="Save Settings",
            icon="EXPORT"
        )
