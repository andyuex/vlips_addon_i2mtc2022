import logging
import math
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import Tuple

from .constants import DECIMAL_PRECISION

log = logging.getLogger(__name__)


class Camera:
    class Facing(str, Enum):
        FRONT = "front"
        BACK = "back"
        UNKNOWN = "unknown"

        @classmethod
        def from_str(cls, value):
            if value.lower() == cls.FRONT.value:
                return cls.FRONT
            elif value.lower() == cls.BACK.value:
                return cls.BACK
            else:
                return cls.UNKNOWN

    name = "Camera"
    facing = Facing.UNKNOWN
    resolution_width = 0  # pixels
    resolution_height = 0  # pixels
    focal_length = 0  # millimeters
    pixel_size = 0  # millimeters
    sensor_width = 0  # millimeters
    sensor_height = 0  # millimeters

    make = ""
    model = ""
    software = ""

    location = (0.0, 0.0, 0.0)  # millimeters
    rotation = (0.0, 0.0, 0.0)  # degrees

    grid_location = (0.0, 0.0)
    rotation_x_angle = 0.0  # degrees
    rotation_z_angle = 0.0  # degrees

    def __init__(
            self,
            name=name,
            facing=facing,
            resolution_width=resolution_width,
            resolution_height=resolution_height,
            focal_length=focal_length,
            pixel_size=pixel_size,
            make=make,
            model=model,
            software=software,
            location=location,
            rotation=rotation,
            grid_location=grid_location,
            rotation_x_angle=rotation_x_angle,
            rotation_z_angle=rotation_z_angle
    ):
        """
        Create an instance of the camera class with the given parameters. Also,
        sensor width and height are calculated from the parameters provided.

        :param name: camera name.
        :param facing: where is the camera facing to. If it is in a smartphone,
        it could be the front or back camera. Use Location enum for values.
        :param resolution_width: width in pixels of the photos taken by this
        camera.
        :param resolution_height: height in pixels of the photos taken by this
        camera.
        :param focal_length: distance from sensor to lens in millimeters.
        :param pixel_size: size of the side of each pixel in the camera sensor,
        in millimeters.
        :param make: camera's make.
        :param model: camera's model.
        :param software: camera's software.
        :param location: camera's X, Y, and Z location in millimeters.
        :param rotation: camera's Y, Y, and X rotation in degrees.
        :param grid_location: camera's Y, Y location in grid coordinates.
        :param rotation_x_angle: rotation around X axis, relative to the default
        rotation of the camera.
        :param rotation_z_angle: rotation around Z axis, relative to the default
        rotation of the camera.
        """

        log.info("Create instance of Camera class")
        log.debug(f"Camera.__init__("
                  f"name={name}, "
                  f"facing={facing}, "
                  f"resolution_width={resolution_width}, "
                  f"resolution_height={resolution_height}, "
                  f"focal_length={focal_length}, "
                  f"pixel_size={pixel_size}, "
                  f"make={make}, "
                  f"model={model}, "
                  f"software={software}, "
                  f"location={location}, "
                  f"rotation={rotation}, "
                  f"grid_location={grid_location}, "
                  f"rotation_x_angle={rotation_x_angle}, "
                  f"rotation_z_angle={rotation_z_angle})")

        if not isinstance(facing, Camera.Facing):
            raise TypeError("facing must be an instance of Camera.facing enum")

        self.name = name
        self.facing = Camera.Facing.from_str(facing)
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.focal_length = focal_length
        self.pixel_size = pixel_size
        self.sensor_width = resolution_width * pixel_size
        self.sensor_height = resolution_height * pixel_size
        self.make = make
        self.model = model
        self.software = software
        self.location = location
        self.rotation = rotation
        self.grid_location = grid_location
        self.rotation_x_angle = rotation_x_angle
        self.rotation_z_angle = rotation_z_angle

    def as_dict(self) -> dict:
        """
        Return a copy of the instance's properties in a dictionary.

        :return: a copy of the instance's properties in a dictionary.
        """

        log.info("Get camera properties as dictionary")
        log.debug("as_dict()")

        return {
            "name": self.name,
            "facing": self.facing,
            "resolution_width": self.resolution_width,
            "resolution_height": self.resolution_height,
            "focal_length": round(self.focal_length, DECIMAL_PRECISION),
            "pixel_size": round(self.pixel_size, DECIMAL_PRECISION),
            "sensor_width": round(self.sensor_width, DECIMAL_PRECISION),
            "sensor_height": round(self.sensor_height, DECIMAL_PRECISION),
            "make": self.make,
            "model": self.model,
            "software": self.software,
            "location": (
                self.location[0],
                self.location[1],
                self.location[2]),
            "rotation": (
                round(self.rotation[0], DECIMAL_PRECISION),
                round(self.rotation[1], DECIMAL_PRECISION),
                round(self.rotation[2], DECIMAL_PRECISION)),
            "grid_location": (
                round(self.grid_location[0], DECIMAL_PRECISION),
                round(self.grid_location[1], DECIMAL_PRECISION)),
            "rotation_x_angle": round(self.rotation_x_angle, DECIMAL_PRECISION),
            "rotation_z_angle": round(self.rotation_z_angle, DECIMAL_PRECISION)
        }

    def __str__(self):
        """
        Return a string representation of the object. Useful to show the details
        of the camera in logs.
        """

        log.info("Get a string representation of the camera")
        log.debug("__str__()")

        return (f"Camera\n"
                f"- Name: {self.name}\n"
                f"- Facing: {self.facing.value}\n"
                f"- Resolution Width: {self.resolution_width} px\n"
                f"- Resolution Height: {self.resolution_height} px\n"
                f"- Focal Length: {self.focal_length} mm\n"
                f"- Pixel Size: {self.pixel_size} mm\n"
                f"- Sensor Width: {self.sensor_width} mm\n"
                f"- Sensor Height: {self.sensor_height} mm\n"
                f"- Make: {self.make}\n"
                f"- Model: {self.model}\n"
                f"- Software: {self.software}\n"
                f"- Location: {self.location} mm\n"
                f"- Rotation: {self.rotation} deg\n"
                f"- Grid Location: {self.grid_location} deg\n"
                f"- Rotation X: {self.rotation_x_angle} deg\n"
                f"- Rotation Z: {self.rotation_z_angle} deg")

    @property
    def rotation_euler(self) -> Tuple[float, float, float]:
        """
        Transform the rotation of the camera from degrees to radians, exposing
        it as a property.

        :return: rotation angles of the camera for axes X, Y, and Z in radians.
        :rtype: Tuple[float, float, float]
        """

        log.info("Get camera rotation in radians")
        log.debug("rotation_euler()")

        return (
            math.radians(self.rotation[0]),
            math.radians(self.rotation[1]),
            math.radians(self.rotation[2]))

    def get_focal_length_rational(self) -> Tuple[int, int]:
        """
        Return a fractional representation of the focal length. Used when saving
        camera details as EXIF data in a JPEG render of a Blender scene, so it
        can be later used to process the image.

        :return: fractional representation of the focal length.
        :rtype: Tuple[int, int]
        """

        log.info("Get fractional representation of focal length")
        log.debug("get_focal_length_rational()")

        focal_length_rational = Fraction(Decimal(self.focal_length)).limit_denominator()
        return focal_length_rational.numerator, focal_length_rational.denominator
