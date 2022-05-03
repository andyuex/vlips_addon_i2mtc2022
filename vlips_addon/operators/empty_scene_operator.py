import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class EmptySceneOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: empty scene operator"""

    bl_idname = EMPTY_SCENE_OPERATOR_NAME
    bl_label = "Empty Scene"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        VLIPSSimulation.empty_scene(context)
        return {"FINISHED"}
