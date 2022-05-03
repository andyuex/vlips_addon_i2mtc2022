import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class CreateSceneOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: create scene operator"""

    bl_idname = CREATE_SCENE_OPERATOR_NAME
    bl_label = "Create Scene"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        VLIPSSimulation.create_scene(
            context=context)
        return {"FINISHED"}
