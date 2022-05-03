import logging
import time
from pathlib import Path

import addon_utils
import yaml
from vlips.constants import DECIMAL_PRECISION

from .constants import *

log = logging.getLogger(__name__)


# TODO: room_properties.keys() has que keys to the user-defined properties!
#  Which means I can remove lots of code!


class Settings:
    @staticmethod
    def load(
            context,
            filepath: Path
    ):
        """
        Load add-on settings from a YAML file.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param filepath: path to the file where the settings should be loaded
        from.
        """

        log.info("Load add-on settings")
        log.debug(f"Settings.load("
                  f"context={context}, "
                  f"filepath={filepath})")

        with open(filepath, "r") as file:
            settings = yaml.safe_load(file)

        scene_settings = settings[SETTINGS_SCENE_KEY]
        log.debug(scene_settings)
        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        scene_properties.tile_side = scene_settings[SETTINGS_SCENE_TILE_SIDE_KEY]
        scene_properties.floor_side_tiles = scene_settings[SETTINGS_SCENE_FLOOR_SIDE_TILES_KEY]

        room_settings = settings[SETTINGS_ROOM_KEY]
        log.debug(room_settings)
        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
        room_properties.name = room_settings[SETTINGS_ROOM_NAME_KEY]
        room_properties.width = room_settings[SETTINGS_ROOM_WIDTH_KEY]
        room_properties.depth = room_settings[SETTINGS_ROOM_DEPTH_KEY]
        room_properties.height = room_settings[SETTINGS_ROOM_HEIGHT_KEY]
        room_properties.thickness = room_settings[SETTINGS_ROOM_THICKNESS_KEY]

        beacon_settings = settings[SETTINGS_BEACON_KEY]
        log.debug(beacon_settings)
        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)
        beacon_properties.name = beacon_settings[SETTINGS_BEACON_NAME_KEY]
        beacon_properties.width = beacon_settings[SETTINGS_BEACON_WIDTH_KEY]
        beacon_properties.height = beacon_settings[SETTINGS_BEACON_HEIGHT_KEY]

        camera_settings = settings[SETTINGS_CAMERA_KEY]
        log.debug(camera_settings)
        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)
        camera_properties.name = camera_settings[SETTINGS_CAMERA_NAME_KEY]
        camera_properties.make = camera_settings[SETTINGS_CAMERA_MAKE_KEY]
        camera_properties.model = camera_settings[SETTINGS_CAMERA_MODEL_KEY]
        camera_properties.orientation = camera_settings[SETTINGS_CAMERA_ORIENTATION_KEY]
        camera_properties.facing = camera_settings[SETTINGS_CAMERA_FACING_KEY]
        camera_properties.resolution_width = camera_settings[SETTINGS_CAMERA_RESOLUTION_WIDTH_KEY]
        camera_properties.resolution_height = camera_settings[SETTINGS_CAMERA_RESOLUTION_HEIGHT_KEY]
        camera_properties.focal_length = camera_settings[SETTINGS_CAMERA_FOCAL_LENGTH_KEY]
        camera_properties.pixel_size = camera_settings[SETTINGS_CAMERA_PIXEL_SIZE_KEY]
        camera_properties.grid_x = camera_settings[SETTINGS_CAMERA_GRID_X_KEY]
        camera_properties.grid_y = camera_settings[SETTINGS_CAMERA_GRID_Y_KEY]
        camera_properties.beacon_distance = camera_settings[SETTINGS_CAMERA_BEACON_DISTANCE_KEY]
        camera_properties.rotation_x_angle = camera_settings[SETTINGS_CAMERA_ROTATION_X_ANGLE_KEY]
        camera_properties.rotation_z_angle = camera_settings[SETTINGS_CAMERA_ROTATION_Z_ANGLE_KEY]
        camera_properties.show_fov = camera_settings[SETTINGS_CAMERA_SHOW_FOW_KEY]

        camera_movement_settings = settings[SETTINGS_CAMERA_MOVEMENT_KEY]
        log.debug(camera_movement_settings)
        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)
        camera_movement_properties.camera_movement_fov_scan_enabled = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_FOV_SCAN_ENABLED_KEY]
        camera_movement_properties.camera_movement_beacon_distance_enabled = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_BEACON_DISTANCE_ENABLED_KEY]
        camera_movement_properties.camera_movement_rotation_x_angle_enabled = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_ANGLE_ENABLED_KEY]
        camera_movement_properties.camera_movement_rotation_z_angle_enabled = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_ANGLE_ENABLED_KEY]
        camera_movement_properties.output_path = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_OUTPUT_PATH_KEY]
        camera_movement_properties.file_prefix = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_FILE_PREFIX_KEY]

        camera_movement_distance_settings = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_DISTANCE_KEY]
        log.debug(camera_movement_distance_settings)
        camera_movement_distance_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME)
        camera_movement_distance_properties.camera_beacon_distance_start = \
            camera_movement_distance_settings[SETTINGS_CAMERA_MOVEMENT_DISTANCE_START_KEY]
        camera_movement_distance_properties.camera_beacon_distance_end = \
            camera_movement_distance_settings[SETTINGS_CAMERA_MOVEMENT_DISTANCE_END_KEY]
        camera_movement_distance_properties.camera_beacon_distance_step = \
            camera_movement_distance_settings[SETTINGS_CAMERA_MOVEMENT_DISTANCE_STEP_KEY]

        camera_movement_horizontal_rotation_settings = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_KEY]
        log.debug(camera_movement_horizontal_rotation_settings)
        camera_movement_horizontal_rotation_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME)
        camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_start = \
            camera_movement_horizontal_rotation_settings[SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_START_KEY]
        camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_end = \
            camera_movement_horizontal_rotation_settings[SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_END_KEY]
        camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_step = \
            camera_movement_horizontal_rotation_settings[SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_STEP_KEY]

        camera_movement_vertical_rotation_settings = \
            camera_movement_settings[SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_KEY]
        log.debug(camera_movement_vertical_rotation_settings)
        camera_movement_vertical_rotation_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME)
        camera_movement_vertical_rotation_properties.camera_rotation_z_angle_start = \
            camera_movement_vertical_rotation_settings[SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_START_KEY]
        camera_movement_vertical_rotation_properties.camera_rotation_z_angle_end = \
            camera_movement_vertical_rotation_settings[SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_END_KEY]
        camera_movement_vertical_rotation_properties.camera_rotation_z_angle_step = \
            camera_movement_vertical_rotation_settings[SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_STEP_KEY]

        # TODO: refresh properties panel and viewport when settings are loaded.

    @staticmethod
    def save(
            context,
            filepath: Path
    ):
        """
        Save add-on settings to a YAML file.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param filepath: path to the file where the settings should be saved
        to.
        """

        log.info("Save add-on settings")
        log.debug(f"Settings.save("
                  f"context={context}, "
                  f"filepath={filepath})")

        module_version = ""
        modules = addon_utils.modules()
        for module in modules:
            if module.bl_info.get("name") == "VLIPS Simulation Tools (vlips)":
                module_version = module.bl_info.get("version")
                break
        addon_version = f"{module_version[0]}.{module_version[1]}.{module_version[2]}"

        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)
        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)
        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)
        camera_movement_distance_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME)
        camera_movement_horizontal_rotation_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME)
        camera_movement_vertical_rotation_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME)

        scene_properties_dictionary = {
            SETTINGS_SCENE_TILE_SIDE_KEY:
                scene_properties.tile_side,
            SETTINGS_SCENE_FLOOR_SIDE_TILES_KEY:
                scene_properties.floor_side_tiles
        }
        room_properties_dictionary = {
            SETTINGS_ROOM_NAME_KEY:
                room_properties.name,
            SETTINGS_ROOM_WIDTH_KEY:
                room_properties.width,
            SETTINGS_ROOM_DEPTH_KEY:
                room_properties.depth,
            SETTINGS_ROOM_HEIGHT_KEY:
                room_properties.height,
            SETTINGS_ROOM_THICKNESS_KEY:
                room_properties.thickness
        }
        beacon_properties_dictionary = {
            SETTINGS_BEACON_NAME_KEY:
                beacon_properties.name,
            SETTINGS_BEACON_WIDTH_KEY:
                beacon_properties.width,
            SETTINGS_BEACON_HEIGHT_KEY:
                beacon_properties.height
        }
        camera_properties_dictionary = {
            SETTINGS_CAMERA_NAME_KEY:
                camera_properties.name,
            SETTINGS_CAMERA_MAKE_KEY:
                camera_properties.make,
            SETTINGS_CAMERA_MODEL_KEY:
                camera_properties.model,
            SETTINGS_CAMERA_ORIENTATION_KEY:
                camera_properties.orientation,
            SETTINGS_CAMERA_FACING_KEY:
                camera_properties.facing,
            SETTINGS_CAMERA_RESOLUTION_WIDTH_KEY:
                camera_properties.resolution_width,
            SETTINGS_CAMERA_RESOLUTION_HEIGHT_KEY:
                camera_properties.resolution_height,
            SETTINGS_CAMERA_FOCAL_LENGTH_KEY:
                round(camera_properties.focal_length, DECIMAL_PRECISION),
            SETTINGS_CAMERA_PIXEL_SIZE_KEY:
                round(camera_properties.pixel_size, DECIMAL_PRECISION),
            SETTINGS_CAMERA_GRID_X_KEY:
                camera_properties.grid_x,
            SETTINGS_CAMERA_GRID_Y_KEY:
                camera_properties.grid_y,
            SETTINGS_CAMERA_BEACON_DISTANCE_KEY:
                round(camera_properties.beacon_distance, DECIMAL_PRECISION),
            SETTINGS_CAMERA_ROTATION_X_ANGLE_KEY:
                round(camera_properties.rotation_x_angle, DECIMAL_PRECISION),
            SETTINGS_CAMERA_ROTATION_Z_ANGLE_KEY:
                round(camera_properties.rotation_z_angle, DECIMAL_PRECISION),
            SETTINGS_CAMERA_SHOW_FOW_KEY:
                camera_properties.show_fov
        }
        camera_movement_distance_properties_dictionary = {
            SETTINGS_CAMERA_MOVEMENT_DISTANCE_START_KEY:
                round(camera_movement_distance_properties.camera_beacon_distance_start, DECIMAL_PRECISION),
            SETTINGS_CAMERA_MOVEMENT_DISTANCE_END_KEY:
                round(camera_movement_distance_properties.camera_beacon_distance_end, DECIMAL_PRECISION),
            SETTINGS_CAMERA_MOVEMENT_DISTANCE_STEP_KEY:
                round(camera_movement_distance_properties.camera_beacon_distance_step, DECIMAL_PRECISION)
        }
        camera_movement_horizontal_rotation_properties_dictionary = {
            SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_START_KEY:
                camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_start,
            SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_END_KEY:
                camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_end,
            SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_STEP_KEY:
                camera_movement_horizontal_rotation_properties.camera_rotation_x_angle_step
        }
        camera_movement_vertical_rotation_properties_dictionary = {
            SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_START_KEY:
                camera_movement_vertical_rotation_properties.camera_rotation_z_angle_start,
            SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_END_KEY:
                camera_movement_vertical_rotation_properties.camera_rotation_z_angle_end,
            SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_STEP_KEY:
                camera_movement_vertical_rotation_properties.camera_rotation_z_angle_step
        }
        camera_movement_properties_dictionary = {
            SETTINGS_CAMERA_MOVEMENT_FOV_SCAN_ENABLED_KEY:
                camera_movement_properties.camera_movement_fov_scan_enabled,
            SETTINGS_CAMERA_MOVEMENT_BEACON_DISTANCE_ENABLED_KEY:
                camera_movement_properties.camera_movement_beacon_distance_enabled,
            SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_ANGLE_ENABLED_KEY:
                camera_movement_properties.camera_movement_rotation_z_angle_enabled,
            SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_ANGLE_ENABLED_KEY:
                camera_movement_properties.camera_movement_rotation_x_angle_enabled,
            SETTINGS_CAMERA_MOVEMENT_OUTPUT_PATH_KEY:
                camera_movement_properties.output_path,
            SETTINGS_CAMERA_MOVEMENT_FILE_PREFIX_KEY:
                camera_movement_properties.file_prefix,
            SETTINGS_CAMERA_MOVEMENT_DISTANCE_KEY:
                camera_movement_distance_properties_dictionary,
            SETTINGS_CAMERA_MOVEMENT_HORIZONTAL_ROTATION_KEY:
                camera_movement_horizontal_rotation_properties_dictionary,
            SETTINGS_CAMERA_MOVEMENT_VERTICAL_ROTATION_KEY:
                camera_movement_vertical_rotation_properties_dictionary
        }

        settings = {
            SETTINGS_VERSION_KEY:
                addon_version,
            SETTINGS_DATE_KEY:
                date,
            SETTINGS_SCENE_KEY:
                scene_properties_dictionary,
            SETTINGS_ROOM_KEY:
                room_properties_dictionary,
            SETTINGS_BEACON_KEY:
                beacon_properties_dictionary,
            SETTINGS_CAMERA_KEY:
                camera_properties_dictionary,
            SETTINGS_CAMERA_MOVEMENT_KEY: camera_movement_properties_dictionary
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as file:
            yaml.dump(
                settings,
                file,
                default_flow_style=False,
                sort_keys=False)
