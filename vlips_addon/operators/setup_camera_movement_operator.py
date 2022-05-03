import bpy

from vlips_addon.modules.constants import *


class SetupCameraMovementOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: camera movement operator"""

    bl_idname = SETUP_CAMERA_MOVEMENT_OPERATOR_NAME
    bl_label = "Setup Camera Movement"
    bl_options = {"REGISTER", "UNDO"}

    camera_movement_fov_scan_enabled: bpy.props.BoolProperty(
        name="FOV Scan",
        description="The camera will scan all tiles inside the field of vision (FOV), left to right, top to bottom",
        default=DEFAULT_CAMERA_MOVEMENT_FOV_SCAN_ENABLED
    )
    camera_movement_beacon_distance_enabled: bpy.props.BoolProperty(
        name="Distance",
        description="The camera distance relative to the beacon will change",
        default=DEFAULT_CAMERA_MOVEMENT_BEACON_DISTANCE_ENABLED
    )
    camera_movement_rotation_x_angle_enabled: bpy.props.BoolProperty(
        name="Rotation X",
        description="The camera's rotation X angle (pitch) will change",
        default=DEFAULT_CAMERA_MOVEMENT_ROTATION_X_ANGLE_ENABLED
    )
    camera_movement_rotation_z_angle_enabled: bpy.props.BoolProperty(
        name="Rotation Z",
        description="The camera's rotation Z angle (yaw) will change",
        default=DEFAULT_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_ENABLED
    )
    output_path: bpy.props.StringProperty(
        name="Output Path",
        description="Path where the renders will be saved to (JPEG)",
        subtype="DIR_PATH",
        default=DEFAULT_RENDER_CAMERA_MOVEMENT_OUTPUT_PATH
    )
    file_prefix: bpy.props.StringProperty(
        name="File Prefix",
        description="Prefix used in each render",
        default=DEFAULT_FILE_PREFIX
    )

    def execute(self, context):
        return {"FINISHED"}
