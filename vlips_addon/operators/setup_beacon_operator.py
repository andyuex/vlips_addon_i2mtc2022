import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class SetupBeaconOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup beacon operator"""

    bl_idname = SETUP_BEACON_OPERATOR_NAME
    bl_label = "Setup Beacon"
    bl_options = {"REGISTER", "UNDO"}

    room_properties = bpy.context.window_manager.operator_properties_last(
        SETUP_ROOM_OPERATOR_NAME)
    if room_properties is None:
        room_height = DEFAULT_ROOM_HEIGHT
    else:
        room_height = room_properties.height

    name: bpy.props.StringProperty(
        name="Name",
        description="Beacon name",
        default=DEFAULT_BEACON_NAME
    )
    width: bpy.props.FloatProperty(
        name="Width",
        description="Beacon width (millimeters)",
        unit="LENGTH",
        default=DEFAULT_BEACON_WIDTH,
        min=MIN_BEACON_WIDTH,
        soft_max=MAX_BEACON_WIDTH
    )
    height: bpy.props.FloatProperty(
        name="Height",
        description="Beacon height (millimeters)",
        unit="LENGTH",
        default=DEFAULT_BEACON_HEIGHT,
        min=MIN_BEACON_HEIGHT,
        soft_max=MAX_BEACON_HEIGHT
    )

    def execute(self, context):
        VLIPSSimulation.setup_beacon(
            context=context,
            name=self.name,
            width=self.width,
            height=self.height
        )

        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)

        VLIPSSimulation.setup_camera(
            context=context,
            name=camera_properties.name,
            make=camera_properties.make,
            model=camera_properties.model,
            orientation=camera_properties.orientation,
            facing=camera_properties.facing,
            resolution_width=camera_properties.resolution_width,
            resolution_height=camera_properties.resolution_height,
            focal_length=camera_properties.focal_length,
            pixel_size=camera_properties.pixel_size,
            beacon_distance=camera_properties.beacon_distance,
            rotation_z_angle=camera_properties.rotation_z_angle,
            rotation_x_angle=camera_properties.rotation_x_angle,
            show_fov=camera_properties.show_fov,
            beacon_properties=self)

        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)
        camera_movement_properties.camera_movement_beacon_distance_enabled = False
        camera_movement_properties.camera_movement_rotation_z_angle_enabled = False
        camera_movement_properties.camera_movement_rotation_x_angle_enabled = False

        return {"FINISHED"}
