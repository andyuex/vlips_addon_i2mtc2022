import logging

import bpy

from .modules.constants import ADDON_SHORT_NAME, CAMERA_SOFTWARE
from .operators.create_scene_operator import CreateSceneOperator
from .operators.empty_scene_operator import EmptySceneOperator
from .operators.load_settings_operator import LoadSettingsOperator
from .operators.render_camera_fov_corners_operator import RenderCameraFOVCornersOperator
from .operators.render_camera_movement_operator import RenderCameraMovementOperator
from .operators.render_scene_operator import RenderSceneOperator
from .operators.save_settings_operator import SaveSettingsOperator
from .operators.setup_beacon_operator import SetupBeaconOperator
from .operators.setup_camera_movement_distance_operator import SetupCameraMovementDistance
from .operators.setup_camera_movement_rotation_x_angle_operator import \
    SetupCameraMovementRotationXAngle
from .operators.setup_camera_movement_operator import SetupCameraMovementOperator
from .operators.setup_camera_movement_rotation_z_angle_operator import SetupCameraMovementRotationZAngle
from .operators.setup_camera_operator import SetupCameraOperator
from .operators.setup_room_operator import SetupRoomOperator
from .operators.setup_scene_operator import SetupSceneOperator
from .operators.setup_texts_operator import SetupTextsOperator
from .panels.actions_panel import VIEW3D_PT_actions
from .panels.camera_movement_panel import VIEW3D_PT_camera_movement
from .panels.preferences_panel import VIEW3D_PT_preferences
from .panels.render_panel import VIEW3D_PT_render

log = logging.getLogger(__name__)

bl_info = {
    "name": "VLIPS Simulation Tools (vlips)",
    "author": "Juan Diego Gutiérrez Gallardo <andy@unex.es>",
    "version": (2, 2, 0),
    "blender": (3, 0, 1),
    "category": "Scene",
    "location": "View3D > Sidebar > VLIPS Tab | Menu Search (F3) -> vlips",
    "description": "Visible Light Indoor Positioning System simulation tools"
}

addon_classes = [
    EmptySceneOperator,
    CreateSceneOperator,
    LoadSettingsOperator,
    SaveSettingsOperator,
    SetupSceneOperator,
    SetupRoomOperator,
    SetupBeaconOperator,
    SetupCameraOperator,
    SetupTextsOperator,
    SetupCameraMovementOperator,
    SetupCameraMovementDistance,
    SetupCameraMovementRotationXAngle,
    SetupCameraMovementRotationZAngle,
    RenderSceneOperator,
    RenderCameraMovementOperator,
    RenderCameraFOVCornersOperator,
    VIEW3D_PT_actions,
    VIEW3D_PT_preferences,
    VIEW3D_PT_camera_movement,
    VIEW3D_PT_render
]


def register():
    """
    Register operator and panels when add-on is enabled in Blender.
    """

    log.info("Register operators and panels")
    log.debug("register()")

    # Register classes
    for addon_class in addon_classes:
        bpy.utils.register_class(addon_class)


def unregister():
    """
    Unregister operators and panels when add-on is disabled in Blender.
    """

    log.info("Unregister operators and panels")
    log.debug("unregister()")

    # Unregister classes
    for addon_class in reversed(addon_classes):
        bpy.utils.unregister_class(addon_class)
