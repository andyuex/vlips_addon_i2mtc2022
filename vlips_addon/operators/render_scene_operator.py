from pathlib import Path

import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.settings import Settings
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class RenderSceneOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: render scene operator"""

    bl_idname = RENDER_SCENE_OPERATOR_NAME
    bl_label = "Render Scene"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="Output Path",
        description="Path where the render will be saved to (JPEG)",
        subtype="FILE_PATH",
        default=DEFAULT_RENDER_SCENE_OUTPUT_PATH
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        filepath = Path(self.filepath)

        # Take screenshot
        screenshot_path_segment = str(filepath.parent / "screenshot.png")
        bpy.ops.screen.screenshot(filepath=screenshot_path_segment)

        # Save settings
        settings_filepath = filepath.parent / "settings.yml"
        Settings.save(
            context=context,
            filepath=settings_filepath)

        # Render scene
        VLIPSSimulation.render_scene(
            context=context,
            filepath=self.filepath)
        self.report({"INFO"}, f"Render saved to {self.filepath}")
        return {"FINISHED"}
