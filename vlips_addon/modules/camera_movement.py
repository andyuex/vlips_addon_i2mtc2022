from enum import Enum


class CameraMovement(str, Enum):
    FOV_SCAN = "fov_scan"
    BEACON_DISTANCE = "beacon_distance"
    ROTATION_X_ANGLE = "rotation_x_angle"
    ROTATION_Z_ANGLE = "rotation_z_angle"
    UNKNOWN = "unknown"

    @classmethod
    def from_str(cls, value):
        if value.lower() == cls.FOV_SCAN.value:
            return cls.FOV_SCAN
        if value.lower() == cls.BEACON_DISTANCE.value:
            return cls.BEACON_DISTANCE
        elif value.lower() == cls.ROTATION_X_ANGLE.value:
            return cls.ROTATION_X_ANGLE
        elif value.lower() == cls.ROTATION_Z_ANGLE.value:
            return cls.ROTATION_Z_ANGLE
        else:
            return cls.UNKNOWN
