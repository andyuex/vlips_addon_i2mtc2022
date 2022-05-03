from vlips_addon.modules.enum_property import EnumProperty, EnumPropertyItem


class CameraFacing(EnumProperty):
    BACK = EnumPropertyItem(
        identifier="back",
        name="Back",
        description="Camera is located in the back of the device")
    FRONT = EnumPropertyItem(
        identifier="front",
        name="Front",
        description="Camera is located in the front of the device")
