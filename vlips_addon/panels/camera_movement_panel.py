import bpy

from vlips_addon.modules.constants import *


class VIEW3D_PT_camera_movement(bpy.types.Panel):
    """
    Visible Light Indoor Positioning Simulation: camera movement panel
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VLIPS"
    bl_label = "Camera Movement"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME,
            text="Distance",
            icon="DRIVER_DISTANCE"
        )
        column.operator(
            SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME,
            text="Rotation X",
            icon="DRIVER_ROTATIONAL_DIFFERENCE"
        )
        column.operator(
            SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME,
            text="Rotation Z",
            icon="FORCE_MAGNETIC"
        )
