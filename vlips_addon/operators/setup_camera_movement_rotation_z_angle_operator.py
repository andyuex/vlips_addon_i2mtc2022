import bpy

from vlips_addon.modules.constants import *


class SetupCameraMovementRotationZAngle(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup camera movement, rotation Z angle operator"""

    bl_idname = SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME
    bl_label = "Rotation Z"
    bl_options = {"REGISTER", "UNDO"}

    camera_rotation_z_angle_start: bpy.props.FloatProperty(
        name="Start",
        description="Starting camera rotation Z angle in degrees (yaw)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_Z_ANGLE_START,
        min=MIN_CAMERA_ROTATION_Z_ANGLE_START,
        soft_max=MAX_CAMERA_ROTATION_Z_ANGLE_START
    )
    camera_rotation_z_angle_end: bpy.props.FloatProperty(
        name="End",
        description="Ending camera rotation Z angle in degrees (yaw)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_Z_ANGLE_END,
        min=MIN_CAMERA_ROTATION_Z_ANGLE_END,
        soft_max=MAX_CAMERA_ROTATION_Z_ANGLE_END
    )
    camera_rotation_z_angle_step: bpy.props.FloatProperty(
        name="Step",
        description="Step in camera rotation Z angle in degrees (yaw)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_Z_ANGLE_STEP,
        soft_max=MAX_CAMERA_ROTATION_Z_ANGLE_STEP
    )

    def execute(self, context):
        return {"FINISHED"}
