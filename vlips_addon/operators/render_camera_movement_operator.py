import logging
from pathlib import Path

import bpy
from numpy import arange

from vlips_addon.modules.camera_movement import CameraMovement
from vlips_addon.modules.constants import *
from vlips_addon.modules.settings import Settings
from vlips_addon.modules.vlips_simulation import VLIPSSimulation

log = logging.getLogger(__name__)


class RenderCameraMovementOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: render camera movement operator"""

    bl_idname = RENDER_CAMERA_MOVEMENT_OPERATOR_NAME
    bl_label = "Render Camera Movement"
    bl_options = {"REGISTER", "UNDO"}

    _camera_movement_fov_scan_enabled = None
    _camera_movement_beacon_distance_enabled = None
    _camera_movement_rotation_x_angle_enabled = None
    _camera_movement_rotation_z_angle_enabled = None

    _camera_properties_beacon_distance = None
    _camera_properties_rotation_x_angle = None
    _camera_properties_rotation_z_angle = None
    _previous_beacon_distance = None
    _previous_rotation_x_angle = None
    _previous_rotation_z_angle = None

    _camera_movement_steps = None
    _camera_movement_index = None
    _camera_movement_file_index = None
    _camera_movement_max_file_index_digits = None

    _file_prefix = None
    _output_path = None
    _camera_movement_max_index = None
    _camera_movement_max_index_digits = None

    _timer = None

    def execute(self, context):
        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)
        self._camera_movement_fov_scan_enabled = \
            camera_movement_properties.camera_movement_fov_scan_enabled
        self._camera_movement_beacon_distance_enabled = \
            camera_movement_properties.camera_movement_beacon_distance_enabled
        self._camera_movement_rotation_x_angle_enabled = \
            camera_movement_properties.camera_movement_rotation_x_angle_enabled
        self._camera_movement_rotation_z_angle_enabled = \
            camera_movement_properties.camera_movement_rotation_z_angle_enabled

        if not self._camera_movement_fov_scan_enabled and \
                not self._camera_movement_beacon_distance_enabled and \
                not self._camera_movement_rotation_x_angle_enabled and \
                not self._camera_movement_rotation_z_angle_enabled:
            self.report({"ERROR"}, "No camera movement selected")
            return {"CANCELLED"}

        if not camera_movement_properties.output_path:
            self.report({"ERROR"}, "Output path is empty")
            return {"CANCELLED"}

        self._save_camera_status(context)

        if self._camera_movement_beacon_distance_enabled:
            camera_movement_beacon_distance_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME)
            if camera_movement_beacon_distance_properties.camera_beacon_distance_step == 0:
                self.report({"ERROR"}, "Distance step cannot be zero")
                return {"CANCELLED"}
            camera_movement_beacon_distance_steps = VLIPSSimulation.get_camera_movement_steps(
                context=context,
                camera_movement=CameraMovement.BEACON_DISTANCE)
        else:
            camera_movement_beacon_distance_steps = [self._camera_properties_beacon_distance]

        if self._camera_movement_rotation_x_angle_enabled:
            camera_movement_rotation_x_angle_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME)
            if camera_movement_rotation_x_angle_properties.camera_rotation_x_angle_step == 0:
                self.report({"ERROR"}, "Rotation X angle step cannot be zero")
                return {"CANCELLED"}
            camera_movement_rotation_x_angle_steps = VLIPSSimulation.get_camera_movement_steps(
                context=context,
                camera_movement=CameraMovement.ROTATION_X_ANGLE)
        else:
            camera_movement_rotation_x_angle_steps = [self._camera_properties_rotation_x_angle]

        if self._camera_movement_rotation_z_angle_enabled:
            camera_movement_rotation_z_angle_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME)
            if camera_movement_rotation_z_angle_properties.camera_rotation_z_angle_step == 0:
                self.report({"ERROR"}, "Horizontal rotation angle step cannot be zero")
                return {"CANCELLED"}
            camera_movement_rotation_z_angle_steps = VLIPSSimulation.get_camera_movement_steps(
                context=context,
                camera_movement=CameraMovement.ROTATION_Z_ANGLE)
        else:
            camera_movement_rotation_z_angle_steps = [self._camera_properties_rotation_z_angle]

        # Reset the index
        self._camera_movement_index = 0

        self._camera_movement_steps = []
        # Prepare all the combinations of camera placement in the FOV grid

        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        tile_side = scene_properties.tile_side

        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)

        camera_name = camera_properties.name
        camera = context.scene.objects[camera_name]
        camera_fov_name = CAMERA_FOV_EVEN_TILES_NAME

        for beacon_distance in camera_movement_beacon_distance_steps:
            for rotation_x_angle in camera_movement_rotation_x_angle_steps:
                for rotation_z_angle in camera_movement_rotation_z_angle_steps:

                    # Move camera to distance, so FOV gets update
                    if self._camera_movement_fov_scan_enabled:
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
                            beacon_distance=beacon_distance,
                            rotation_x_angle=rotation_x_angle,
                            rotation_z_angle=rotation_z_angle,
                            show_fov=camera_properties.show_fov)

                        # bpy.context.view_layer.update()
                        context.view_layer.update()

                        camera_fov = context.scene.objects[camera_fov_name]
                        camera_fov_width = camera_fov.dimensions[0]
                        camera_fov_height = camera_fov.dimensions[1]

                        range_start = -camera_fov_width / 2
                        range_stop = camera_fov_width / 2
                        range_step = tile_side
                        range_x = arange(range_start, range_stop + tile_side, range_step)

                        range_start = camera_fov_height / 2
                        range_stop = -camera_fov_height / 2
                        range_step = -tile_side
                        range_y = arange(range_start, range_stop - tile_side, range_step)
                    else:
                        range_x = [camera.location[0]]
                        range_y = [camera.location[1]]

                    for y in range_y:
                        for x in range_x:
                            camera_location = (x, y, beacon_distance)
                            fov_grid_coordinates = int(x / tile_side), int(y / tile_side)
                            self._camera_movement_steps.append({
                                CameraMovement.FOV_SCAN.value: camera_location,
                                CAMERA_MOVEMENT_FOV_GRID_COORDINATES: fov_grid_coordinates,
                                CAMERA_MOVEMENT_BEACON_DISTANCE: beacon_distance,
                                CAMERA_MOVEMENT_ROTATION_X_ANGLE: rotation_x_angle,
                                CAMERA_MOVEMENT_ROTATION_Z_ANGLE: rotation_z_angle
                            })

        self._restore_camera_status(context)

        # Recover the data needed to perform this task
        self._file_prefix = camera_movement_properties.file_prefix
        self._output_path = camera_movement_properties.output_path

        # Prepare the file suffix
        self._camera_movement_max_index = len(self._camera_movement_steps)
        self._camera_movement_max_index_digits = VLIPSSimulation.get_camera_movement_steps_digits(
            self._camera_movement_steps)

        # Prepare timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        filepath = Path(self._output_path)

        # Take screenshot
        screenshot_path_segment = str(filepath / "screenshot.png")
        bpy.ops.screen.screenshot(filepath=screenshot_path_segment)

        # Save settings
        settings_filepath = filepath / "settings.yml"
        Settings.save(
            context=context,
            filepath=settings_filepath)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        """
        Execute a step of the operator.

        :param context: Blender's current context.
        :param event: event that raised this action.
        """

        log.info("Execute step of the operator")
        log.debug(f"RenderCameraFOVCornersOperator.modal("
                  f"context={context}, "
                  f"event={event})")

        if event.type == "ESC":
            self.report({"WARNING"}, "Render cancelled")
            self._finish(context)
            return {"CANCELLED"}
        elif event.type == "TIMER":
            # Move a step and render the scene
            camera_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_OPERATOR_NAME)

            camera_movement_step = self._camera_movement_steps[self._camera_movement_index]

            camera_x = camera_movement_step[CameraMovement.FOV_SCAN.value][0]
            camera_y = camera_movement_step[CameraMovement.FOV_SCAN.value][1]
            beacon_distance = camera_movement_step[CAMERA_MOVEMENT_BEACON_DISTANCE]
            rotation_x_angle = camera_movement_step[CAMERA_MOVEMENT_ROTATION_X_ANGLE]
            rotation_z_angle = camera_movement_step[CAMERA_MOVEMENT_ROTATION_Z_ANGLE]

            camera_properties.beacon_distance = beacon_distance
            camera_properties.rotation_x_angle = rotation_x_angle
            camera_properties.rotation_z_angle = rotation_z_angle

            log.debug(f"- camera_movement_step: {camera_movement_step}")
            log.debug(f"- camera_x: {camera_x}")
            log.debug(f"- camera_y: {camera_y}")
            log.debug(f"- beacon_distance: {beacon_distance}")
            log.debug(f"- rotation_x_angle: {rotation_x_angle}")
            log.debug(f"- rotation_z_angle: {rotation_z_angle}")

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
                x=camera_x,
                y=camera_y)

            if camera_properties.beacon_distance != self._previous_beacon_distance or \
                    camera_properties.rotation_x_angle != self._previous_rotation_x_angle or \
                    camera_properties.rotation_z_angle != self._previous_rotation_z_angle:
                self._previous_beacon_distance = camera_properties.beacon_distance
                self._previous_rotation_x_angle = camera_properties.rotation_x_angle
                self._previous_rotation_z_angle = camera_properties.rotation_z_angle
                self._camera_movement_file_index = 0
                filtered_camera_movements = list(filter(
                    lambda step:
                    step[
                        CAMERA_MOVEMENT_BEACON_DISTANCE] == camera_properties.beacon_distance and
                    step[
                        CAMERA_MOVEMENT_ROTATION_X_ANGLE] == camera_properties.rotation_x_angle and
                    step[
                        CAMERA_MOVEMENT_ROTATION_Z_ANGLE] == camera_properties.rotation_z_angle,
                    self._camera_movement_steps))
                camera_movement_max_file_index_digits = VLIPSSimulation.get_camera_movement_steps_digits(
                    filtered_camera_movements)
                self._camera_movement_max_file_index_digits = camera_movement_max_file_index_digits
            else:
                self._camera_movement_file_index += 1

            filepath = VLIPSSimulation.get_camera_movement_file_path(
                index=self._camera_movement_file_index,
                max_index_digits=self._camera_movement_max_file_index_digits,
                file_prefix=self._file_prefix,
                output_path=self._output_path,
                fov_scan_enabled=self._camera_movement_fov_scan_enabled,
                beacon_distance_enabled=self._camera_movement_beacon_distance_enabled,
                rotation_x_angle_enabled=self._camera_movement_rotation_x_angle_enabled,
                rotation_z_angle_enabled=self._camera_movement_rotation_z_angle_enabled,
                camera_movement_step=camera_movement_step)

            log.debug(f"- filepath: {filepath}")

            VLIPSSimulation.render_scene(context, filepath)

            text_info = f"Render {self._camera_movement_index + 1}/{self._camera_movement_max_index} " \
                        f"saved to {filepath}"
            text_cancel = "ESC to cancel"
            context.workspace.status_text_set(f"{text_info} ({text_cancel})")

            self._camera_movement_index += 1
            if self._camera_movement_index == self._camera_movement_max_index:
                self.report({"INFO"}, "Render finished")
                self._finish(context)
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def _finish(self, context):
        """
        Finish the current modal operator with timer.

        :param context: Blender's current context.
        """

        log.info("Stop modal operator")
        log.debug(f"RenderCameraMovementOperator._finish("
                  f"context={context})")

        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self._restore_camera_status(context)
        context.workspace.status_text_set(None)

    def _save_camera_status(self, context: bpy.types.Context):
        """
        Save camera properties so they can be restored them.

        :param context: Blender's current context.
        """

        log.info("Save camera status")
        log.debug(f"RenderCameraMovementOperator._save_camera_status("
                  f"context={context})")

        camera_properties = context.window_manager.operator_properties_last(SETUP_CAMERA_OPERATOR_NAME)
        self._camera_properties_beacon_distance = camera_properties.beacon_distance
        self._camera_properties_rotation_x_angle = camera_properties.rotation_x_angle
        self._camera_properties_rotation_z_angle = camera_properties.rotation_z_angle

    def _restore_camera_status(self, context: bpy.types.Context):
        """
        Move the camera back to where it was before

        :param context: Blender's current context.
        """

        log.info("Restore camera status")
        log.debug(f"RenderCameraMovementOperator._restore_camera_status("
                  f"context={context})")

        camera_properties = context.window_manager.operator_properties_last(SETUP_CAMERA_OPERATOR_NAME)

        camera_properties.beacon_distance = self._camera_properties_beacon_distance

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
            beacon_distance=self._camera_properties_beacon_distance,
            rotation_x_angle=self._camera_properties_rotation_x_angle,
            rotation_z_angle=self._camera_properties_rotation_z_angle,
            show_fov=camera_properties.show_fov)
