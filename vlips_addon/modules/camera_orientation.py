from vlips_addon.modules.enum_property import EnumProperty, EnumPropertyItem


class CameraOrientation(EnumProperty):
    PORTRAIT = EnumPropertyItem(
        identifier="portrait",
        name="Portrait",
        description="Camera is in portrait mode (taller than wider)")
    LANDSCAPE = EnumPropertyItem(
        identifier="landscape",
        name="Landscape",
        description="Camera is landscape mode (wider than taller)")

    @classmethod
    def from_str(cls, value):
        if value.lower() == cls.PORTRAIT.value.identifier:
            return cls.PORTRAIT
        else:
            return cls.LANDSCAPE
