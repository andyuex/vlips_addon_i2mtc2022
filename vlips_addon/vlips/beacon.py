import logging
import math
from typing import Tuple

from .constants import DECIMAL_PRECISION

log = logging.getLogger(__name__)


class Beacon:
    name = "Beacon"
    dimensions = (0, 0, 0)  # millimeters
    location = (0, 0, 0)  # millimeters
    rotation = (0.0, 0.0, 0.0)  # degrees

    def __init__(
            self,
            name=name,
            dimensions=dimensions,
            location=location,
            rotation=rotation
    ):
        """
        Create an instance of the Beacon class with the given properties.

        :param name: beacon name.
        :param dimensions: beacon LED panel's width, height, depth in millimeters.
        :param location: beacon's X, Y, and Z location in millimeters.
        :param rotation: beacon's Y, Y, and X rotation in degrees.
        """

        log.info("Create instance of Beacon class")
        log.debug(f"Beacon.__init__("
                  f"name={name}, "
                  f"dimensions={dimensions}, "
                  f"location={location}, "
                  f"rotation={rotation})")

        self.name = name
        self.dimensions = dimensions
        self.location = location
        self.rotation = rotation

    def as_dict(self) -> dict:
        """
        Return a copy of the instance's properties in a dictionary.

        :return: a copy of the instance's properties in a dictionary.
        """

        log.info("Get beacon properties as dictionary")
        log.debug("as_dict()")

        return {
            "name": self.name,
            "dimensions": (
                self.dimensions[0],
                self.dimensions[1],
                self.dimensions[2]),
            "location": (
                self.location[0],
                self.location[1],
                self.location[2]),
            "rotation": (
                round(self.rotation[0], DECIMAL_PRECISION),
                round(self.rotation[1], DECIMAL_PRECISION),
                round(self.rotation[2], DECIMAL_PRECISION))
        }

    def __str__(self):
        """
        Return a string representation of the object. Useful to show the details
        of the beacon in logs.
        """

        log.info("Get a string representation of the beacon")
        log.debug("__str__()")

        return (f"Beacon\n"
                f"- Name: {self.name}\n"
                f"- Dimensions: {self.dimensions} mm\n"
                f"- Location: {self.location} mm\n"
                f"- Rotation: {self.rotation} deg"
                )

    @property
    def rotation_euler(self) -> Tuple[float, float, float]:
        """
        Transform the rotation of the beacon from degrees to radians, exposing
        it as a property.

        :return: rotation angles of the beacon for axes X, Y, and Z in radians.
        :rtype: Tuple[float, float, float]
        """

        log.info("Get beacon rotation in radians")
        log.debug("rotation_euler()")

        return (
            math.radians(self.rotation[0]),
            math.radians(self.rotation[1]),
            math.radians(self.rotation[2])
        )
