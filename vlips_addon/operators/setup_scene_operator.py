import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class SetupSceneOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup scene operator"""

    bl_idname = SETUP_SCENE_OPERATOR_NAME
    bl_label = "Setup Scene"
    bl_options = {"REGISTER", "UNDO"}

    tile_side: bpy.props.FloatProperty(
        name="Tile Side",
        description="Length of the side of each tile (millimeters)",
        unit="LENGTH",
        default=DEFAULT_TILE_SIDE,
        min=MIN_TILE_SIDE,
        soft_max=MAX_TILE_SIDE
    )
    floor_side_tiles: bpy.props.IntProperty(
        name="Floor Side Tiles",
        description="Tiles on each side of the floor",
        default=DEFAULT_FLOOR_SIDE_TILES,
        min=MIN_FLOOR_SIDE_TILES,
        soft_max=MAX_FLOOR_SIDE_TILES
    )

    def execute(self, context):
        VLIPSSimulation.setup_scene(
            context=context,
            tile_side=self.tile_side,
            floor_side_tiles=self.floor_side_tiles)

        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
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
            scene_properties=self,
            room_properties=room_properties)

        return {"FINISHED"}
