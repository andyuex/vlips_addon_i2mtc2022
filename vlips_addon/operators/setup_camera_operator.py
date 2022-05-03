import bpy

from vlips_addon.modules.camera_facing import CameraFacing
from vlips_addon.modules.camera_orientation import CameraOrientation
from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class SetupCameraOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup camera operator"""

    bl_idname = SETUP_CAMERA_OPERATOR_NAME
    bl_label = "Setup Camera"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(
        name="Name",
        description="Camera name",
        default=DEFAULT_CAMERA_NAME
    )
    make: bpy.props.StringProperty(
        name="Make",
        description="Camera make",
        default=DEFAULT_CAMERA_MAKE
    )
    model: bpy.props.StringProperty(
        name="Model",
        description="Camera model",
        default=DEFAULT_CAMERA_MODEL
    )
    orientation: bpy.props.EnumProperty(
        name="Orientation",
        description="Camera orientation",
        default=DEFAULT_CAMERA_ORIENTATION,
        items=CameraOrientation.to_list()
    )
    facing: bpy.props.EnumProperty(
        name="Facing",
        description="Camera facing",
        default=DEFAULT_CAMERA_FACING,
        items=CameraFacing.to_list()
    )
    resolution_width: bpy.props.IntProperty(
        name="Resolution Width",
        description="Camera resolution width (pixels)",
        subtype="PIXEL",
        default=DEFAULT_CAMERA_RESOLUTION_WIDTH,
        min=MIN_CAMERA_RESOLUTION_WIDTH,
        soft_max=MAX_CAMERA_RESOLUTION_WIDTH
    )
    resolution_height: bpy.props.IntProperty(
        name="Resolution Height",
        description="Camera resolution height (pixels)",
        subtype="PIXEL",
        default=DEFAULT_CAMERA_RESOLUTION_HEIGHT,
        min=MIN_CAMERA_RESOLUTION_HEIGHT,
        soft_max=MAX_CAMERA_RESOLUTION_HEIGHT
    )
    focal_length: bpy.props.FloatProperty(
        name="Focal Length",
        description="Camera focal length (millimeters)",
        subtype="DISTANCE_CAMERA",
        default=DEFAULT_CAMERA_FOCAL_LENGTH,
        min=MIN_CAMERA_FOCAL_LENGTH,
        soft_max=MAX_CAMERA_FOCAL_LENGTH
    )
    pixel_size: bpy.props.FloatProperty(
        name="Pixel Size",
        description="Camera pixel size (millimeters)",
        subtype="DISTANCE_CAMERA",
        default=DEFAULT_CAMERA_PIXEL_SIZE,
        min=MIN_CAMERA_PIXEL_SIZE,
        soft_max=MAX_CAMERA_PIXEL_SIZE
    )
    grid_x: bpy.props.IntProperty(
        name="Grid X",
        description="X coordinate of the grid the camera should be at. Center of the FOV is at 0, 0",
        default=0
    )
    grid_y: bpy.props.IntProperty(
        name="Grid Y",
        description="Y coordinate of the grid the camera should be at. Center of the FOV is at 0, 0",
        default=0
    )
    beacon_distance: bpy.props.FloatProperty(
        name="Beacon Distance",
        description="Distance to beacon (meters)",
        unit="LENGTH",
        step=1000,
        default=DEFAULT_CAMERA_BEACON_DISTANCE,
        min=MIN_CAMERA_BEACON_DISTANCE,
        soft_max=MAX_CAMERA_BEACON_DISTANCE
    )
    rotation_x_angle: bpy.props.FloatProperty(
        name="Rotation X",
        description="Rotation around X axis in degrees (pitch)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_X_ANGLE,
        min=MIN_CAMERA_ROTATION_X_ANGLE,
        soft_max=MAX_CAMERA_ROTATION_X_ANGLE
    )
    rotation_z_angle: bpy.props.FloatProperty(
        name="Rotation Z",
        description="Rotation around Z axis in degrees (yaw)",
        precision=2,
        step=10,
        default=DEFAULT_CAMERA_ROTATION_Z_ANGLE,
        min=MIN_CAMERA_ROTATION_Z_ANGLE,
        soft_max=MAX_CAMERA_ROTATION_Z_ANGLE
    )
    show_fov: bpy.props.BoolProperty(
        name="Show FOV",
        description="Draw camera's field of vision on the floor",
        default=DEFAULT_SHOW_CAMERA_FOV
    )

    def execute(self, context):

        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        tile_side = scene_properties.tile_side

        x = tile_side * self.grid_x
        y = tile_side * self.grid_y

        VLIPSSimulation.setup_camera(
            context=context,
            name=self.name,
            make=self.make,
            model=self.model,
            orientation=self.orientation,
            facing=self.facing,
            resolution_width=self.resolution_width,
            resolution_height=self.resolution_height,
            focal_length=self.focal_length,
            pixel_size=self.pixel_size,
            beacon_distance=self.beacon_distance,
            rotation_z_angle=self.rotation_z_angle,
            rotation_x_angle=self.rotation_x_angle,
            show_fov=self.show_fov,
            x=x,
            y=y)
        return {"FINISHED"}
