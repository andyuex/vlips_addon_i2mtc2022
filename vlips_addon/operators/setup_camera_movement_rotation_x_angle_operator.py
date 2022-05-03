import bpy

from vlips_addon.modules.constants import *


class SetupCameraMovementRotationXAngle(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup camera movement, rotation X angle operator"""

    bl_idname = SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME
    bl_label = "Rotation X"
    bl_options = {"REGISTER", "UNDO"}

    camera_rotation_x_angle_start: bpy.props.FloatProperty(
        name="Start",
        description="Starting camera rotation X angle in degrees (pitch)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_X_ANGLE_START,
        min=MIN_CAMERA_ROTATION_X_ANGLE_START,
        soft_max=MAX_CAMERA_ROTATION_X_ANGLE_START
    )
    camera_rotation_x_angle_end: bpy.props.FloatProperty(
        name="End",
        description="Ending camera rotation X angle in degrees (pitch)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_X_ANGLE_END,
        min=MIN_CAMERA_HORIZONTAL_ROTATION_ANGLE_END,
        soft_max=MAX_CAMERA_HORIZONTAL_ROTATION_ANGLE_END
    )
    camera_rotation_x_angle_step: bpy.props.FloatProperty(
        name="Step",
        description="Step in rotation X angle relative to the beacon (degrees)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_X_ANGLE_STEP,
        soft_max=MAX_CAMERA_ROTATION_X_ANGLE_STEP
    )

    def execute(self, context):
        return {"FINISHED"}
