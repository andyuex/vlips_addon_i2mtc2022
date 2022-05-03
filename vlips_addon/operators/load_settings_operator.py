import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.settings import Settings
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class LoadSettingsOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: load settings operator"""

    bl_idname = LOAD_SETTINGS_OPERATOR_NAME
    bl_label = "Load Settings"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="Input Path",
        description="Path where the settings will be read from (YAML)",
        subtype="FILE_PATH",
        default=DEFAULT_SETTINGS_PATH
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        Settings.load(
            context=context,
            filepath=self.filepath)

        VLIPSSimulation.empty_scene(context)

        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        VLIPSSimulation.setup_scene(
            context=context,
            tile_side=scene_properties.tile_side,
            floor_side_tiles=scene_properties.floor_side_tiles)

        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
        VLIPSSimulation.setup_room(
            context=context,
            name=room_properties.name,
            width=room_properties.width,
            depth=room_properties.depth,
            height=room_properties.height,
            thickness=room_properties.thickness)

        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)
        VLIPSSimulation.setup_beacon(
            context=context,
            name=beacon_properties.name,
            width=beacon_properties.width,
            height=beacon_properties.height,
            room_properties=room_properties)

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
            room_properties=room_properties)

        # Let the view port show the whole scene
        VLIPSSimulation.zoom_to_scene()

        # HACK: change from "Layout" context to "Modeling" makes the operator
        # UI (in the left lower corner) disappear. Next time you open the
        # operator it will show the values loaded from settings.
        context.window.workspace = bpy.data.workspaces["Modeling"]
        context.window.workspace = bpy.data.workspaces["Layout"]

        self.report({"INFO"}, f"Settings loaded from {self.filepath}")
        return {"FINISHED"}
