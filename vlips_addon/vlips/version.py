import logging
from typing import Tuple

log = logging.getLogger(__name__)


class Version:
    major: int = 0
    minor: int = 0
    patch: int = 0

    def __init__(
            self,
            major: int = None,
            minor: int = None,
            patch: int = None,
            components: Tuple[int, int, int] = None):
        """
        Create an instance of the class, given its three components, following
        semantic versioning described in https://semver.org.

        Parameter `as_tuple`

        :param major: major version number component.
        :param minor: minor version number component.
        :param patch: patch version number component.
        :param components: tuple with three int components, ordered as major,
        minor, and patch.

        :return: instance of Version class.
        """

        log.info("Create new instance of class Version")
        log.debug(f"Version.init("
                      f"major={major}"
                      f"minor={minor}"
                      f"minor={patch}"
                      f"components={components})")

        if components is None:
            self.major = major
            self.minor = minor
            self.patch = patch
        else:
            self.major = components[0]
            self.minor = components[1]
            self.patch = components[2]

    def to_string(self) -> str:
        """
        Return the three version components as a string separated with dots.

        :return: string composed by the three version components separated
        with dots.
        """

        log.info("Transform version components to string")
        log.debug(f"Version.to_string()")

        return f"{self.major}.{self.minor}.{self.patch}"

    def to_tuple(self) -> Tuple[int, int, int]:
        """
        Return the three version components as a tuple.

        :return: tuple composed by the three version components.
        """

        log.info("Transform version components to tuple")
        log.debug(f"Version.to_tuple()")

        return self.major, self.minor, self.patch
