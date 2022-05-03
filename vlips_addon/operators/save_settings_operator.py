from pathlib import Path

import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.settings import Settings


class SaveSettingsOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: save settings operator"""

    bl_idname = SAVE_SETTINGS_OPERATOR_NAME
    bl_label = "Save Settings"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="Output Path",
        description="Path where the settings will be saved to (YAML)",
        subtype="FILE_PATH",
        default=DEFAULT_SETTINGS_PATH
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        Settings.save(
            context=context,
            filepath=Path(self.filepath))
        self.report({"INFO"}, f"Settings saved to {self.filepath}")
        return {"FINISHED"}
