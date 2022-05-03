import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class SetupRoomOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup room operator"""

    bl_idname = SETUP_ROOM_OPERATOR_NAME
    bl_label = "Setup Room"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(
        name="Name",
        description="Room name",
        default=DEFAULT_ROOM_NAME
    )
    width: bpy.props.FloatProperty(
        name="Width",
        description="Room width (Y axis, millimeters)",
        unit="LENGTH",
        default=DEFAULT_ROOM_WIDTH,
        min=MIN_ROOM_WIDTH,
        soft_max=MAX_ROOM_WIDTH,
        step=DISTANCE_STEP
    )
    depth: bpy.props.FloatProperty(
        name="Depth",
        description="Room depth (X axis, millimeters)",
        unit="LENGTH",
        default=DEFAULT_ROOM_DEPTH,
        min=MIN_ROOM_DEPTH,
        soft_max=MAX_ROOM_DEPTH,
        step=DISTANCE_STEP
    )
    height: bpy.props.FloatProperty(
        name="Height",
        description="Room height (Z axis, millimeters)",
        unit="LENGTH",
        default=DEFAULT_ROOM_HEIGHT,
        min=MIN_ROOM_HEIGHT,
        soft_max=MAX_ROOM_HEIGHT,
        step=DISTANCE_STEP
    )
    thickness: bpy.props.FloatProperty(
        name="Thickness",
        description="Room wireframe thickness (millimeters)",
        unit="LENGTH",
        default=DEFAULT_ROOM_THICKNESS,
        min=MIN_ROOM_THICKNESS,
        soft_max=MAX_ROOM_THICKNESS
    )

    def execute(self, context):
        VLIPSSimulation.setup_room(
            context=context,
            name=self.name,
            width=self.width,
            depth=self.depth,
            height=self.height,
            thickness=self.thickness)

        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)
        VLIPSSimulation.setup_beacon(
            context=context,
            name=beacon_properties.name,
            width=beacon_properties.width,
            height=beacon_properties.height,
            room_properties=self)

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
            rotation_x_angle=camera_properties.rotation_x_angle,
            rotation_z_angle=camera_properties.rotation_z_angle,
            show_fov=camera_properties.show_fov,
            room_properties=self)

        return {"FINISHED"}
