import bpy

from vlips_addon.modules.constants import *


class SetupCameraMovementDistance(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup camera movement, beacon distance operator"""

    bl_idname = SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME
    bl_label = "Distance"
    bl_options = {"REGISTER", "UNDO"}

    camera_beacon_distance_start: bpy.props.FloatProperty(
        name="Start",
        description="Starting distance form the camera to the beacon (millimeters)",
        unit="LENGTH",
        default=DEFAULT_CAMERA_DISTANCE_START,
        min=MIN_CAMERA_DISTANCE_START,
        soft_max=MAX_CAMERA_DISTANCE_START
    )
    camera_beacon_distance_end: bpy.props.FloatProperty(
        name="End",
        description="Ending distance form the camera to the beacon (millimeters)",
        unit="LENGTH",
        default=DEFAULT_CAMERA_DISTANCE_END,
        min=MIN_CAMERA_DISTANCE_END,
        soft_max=MAX_CAMERA_DISTANCE_END
    )
    camera_beacon_distance_step: bpy.props.FloatProperty(
        name="Step",
        description="Step in distance form the camera to the beacon (millimeters)",
        unit="LENGTH",
        default=DEFAULT_CAMERA_DISTANCE_STEP,
        min=MIN_CAMERA_DISTANCE_STEP,
        soft_max=MAX_CAMERA_DISTANCE_STEP
    )

    def execute(self, context):
        return {"FINISHED"}
