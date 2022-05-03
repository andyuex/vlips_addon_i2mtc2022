import bpy

from vlips_addon.modules.constants import *
from vlips_addon.modules.vlips_simulation import VLIPSSimulation


class SetupTextsOperator(bpy.types.Operator):
    """Visible Light Indoor Positioning Simulation: setup texts operator"""

    bl_idname = SETUP_TEXTS_OPERATOR_NAME
    bl_label = "Setup Texts"
    bl_options = {"REGISTER", "UNDO"}

    font_size: bpy.props.FloatProperty(
        name="Font Size",
        description="Size of the font used to display text in the room floor (millimeters)",
        unit="LENGTH",
        default=DEFAULT_FONT_SIZE,
        min=MIN_FONT_SIZE,
        soft_max=MAX_FONT_SIZE
    )

    def execute(self, context):
        VLIPSSimulation.setup_texts(
            context=context,
            font_size=self.font_size)
        return {"FINISHED"}
