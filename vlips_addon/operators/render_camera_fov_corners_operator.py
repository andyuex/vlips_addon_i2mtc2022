import logging
import os
from pathlib import Path

import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.settings import Settings
from vlips_addon.modules.vlips_simulation import VLIPSSimulation

log = logging.getLogger(__name__)


class RenderCameraFOVCornersOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: movement render, FOV corners"""

    bl_idname = RENDER_CAMERA_FOV_CORNERS_NAME
    bl_label = "Render FOV Corners"
    bl_options = {"REGISTER", "UNDO"}

    _camera_location = None

    _camera_movement_steps = None
    _camera_movement_index = None

    _file_prefix = None
    _output_path = None
    _camera_movement_max_index = None
    _camera_movement_max_index_digits = None

    _timer = None

    def execute(self, context):

        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)

        if not camera_movement_properties.output_path:
            self.report({"ERROR"}, "Output path is empty")
            return {"CANCELLED"}

        self._save_camera_status(context)

        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)

        camera = context.scene.objects[camera_properties.name]
        camera_height = camera.location[2]

        fov_names = [
            CAMERA_FOV_FULL_NAME,
            CAMERA_FOV_BEACON_NAME,
            CAMERA_FOV_TILES_NAME,
            CAMERA_FOV_EVEN_TILES_NAME]

        # Reset the index
        self._camera_movement_index = 0

        # Prepare all the combinations of camera placement in the FOV corners
        self._camera_movement_steps = []
        for fov_name in fov_names:
            if fov_name in context.scene.objects:
                fov = context.scene.objects[fov_name]
                fov_width_halved = fov.dimensions[0] / 2
                fov_height_halved = fov.dimensions[1] / 2
                normalized_fov_name = fov_name[3:].lower()

                self._camera_movement_steps.append({
                    CAMERA_MOVEMENT_FOV_SCAN_LOCATION_KEY: [
                        -fov_width_halved,
                        fov_height_halved,
                        camera_height],
                    CAMERA_MOVEMENT_FOV_SCAN_FILE_NAME_KEY:
                        f"{normalized_fov_name}_upper_left.jpg"
                })

                self._camera_movement_steps.append({
                    CAMERA_MOVEMENT_FOV_SCAN_LOCATION_KEY: [
                        fov_width_halved,
                        fov_height_halved,
                        camera_height],
                    CAMERA_MOVEMENT_FOV_SCAN_FILE_NAME_KEY:
                        f"{normalized_fov_name}_upper_right.jpg"
                })

                self._camera_movement_steps.append({
                    CAMERA_MOVEMENT_FOV_SCAN_LOCATION_KEY: [
                        fov_width_halved,
                        -fov_height_halved,
                        camera_height],
                    CAMERA_MOVEMENT_FOV_SCAN_FILE_NAME_KEY:
                        f"{normalized_fov_name}_lower_right.jpg"
                })

                self._camera_movement_steps.append({
                    CAMERA_MOVEMENT_FOV_SCAN_LOCATION_KEY: [
                        -fov_width_halved,
                        -fov_height_halved,
                        camera_height],
                    CAMERA_MOVEMENT_FOV_SCAN_FILE_NAME_KEY:
                        f"{normalized_fov_name}_lower_left.jpg"
                })

        log.debug(f"- camera_movement_steps: {self._camera_movement_steps}")

        camera_movement_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_MOVEMENT_OPERATOR_NAME)
        self._file_prefix = camera_movement_properties.file_prefix
        self._output_path = camera_movement_properties.output_path

        # Prepare the file prefix
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
            camera_movement_step = self._camera_movement_steps[self._camera_movement_index]
            camera_location = camera_movement_step[CAMERA_MOVEMENT_FOV_SCAN_LOCATION_KEY]
            file_name = camera_movement_step[CAMERA_MOVEMENT_FOV_SCAN_FILE_NAME_KEY]

            log.debug(f"- camera_movement_step: {camera_movement_step}")
            log.debug(f"- camera_location: {camera_location}")
            log.debug(f"- file_name: {file_name}")

            camera_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_OPERATOR_NAME)
            camera = context.scene.objects[camera_properties.name]
            camera.location = camera_location

            file_number = str(self._camera_movement_index).zfill(self._camera_movement_max_index_digits)
            if self._file_prefix == "":
                render_file_name = f"{file_number}_{file_name}"
            else:
                render_file_name = f"{self._file_prefix}_{file_number}_{file_name}"
            file_path = os.path.join(self._output_path, render_file_name)

            log.debug(f"- file_path: {file_path}")

            VLIPSSimulation.render_scene(context=context, filepath=file_path)

            text_info = f"Render {self._camera_movement_index + 1}/{self._camera_movement_max_index} " \
                        f"saved to {file_path}"
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
        Stop the current modal operator with timer.

        :param context: Blender's current context.
        """

        log.info("Finish modal operator")
        log.debug(f"RenderCameraFOVCornersOperator._finish("
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
        log.debug(f"RenderCameraFOVCornersOperator._save_camera_status("
                  f"context={context})")

        camera_properties = context.window_manager.operator_properties_last(SETUP_CAMERA_OPERATOR_NAME)
        camera = context.scene.objects[camera_properties.name]
        self._camera_location = camera.location

    def _restore_camera_status(self, context: bpy.types.Context):
        """
        Move the camera back to where it was before.

        :param context: Blender's current context.
        """

        log.info("Restore camera status")
        log.debug(f"RenderCameraFOVCornersOperator._restore_camera_status("
                  f"context={context})")

        camera_properties = context.window_manager.operator_properties_last(SETUP_CAMERA_OPERATOR_NAME)
        camera = context.scene.objects[camera_properties.name]
        camera.location = self._camera_location

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
            show_fov=camera_properties.show_fov)
