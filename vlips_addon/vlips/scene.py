import logging

log = logging.getLogger(__name__)


class Scene:
    tile_side = 0  # millimeters
    floor_sides_tiles = 0  # tiles

    def __init__(
            self,
            tile_side=tile_side,
            floor_sides_tiles=floor_sides_tiles
    ):
        """
        Create an instance of the Scene class, containing multiple
        scene parameters.

        :param tile_side: length of each tile in the scene, in millimeters.
        :param floor_sides_tiles: number of tiles in the scene's floor.
        """

        log.info("Create instance of Scene class")
        log.debug(f"Scene.__init__("
                  f"tile_side={tile_side}, "
                  f"floor_sides_tiles={floor_sides_tiles})")

        self.tile_side = tile_side
        self.floor_sides_tiles = floor_sides_tiles

    def as_dict(self) -> dict:
        """
        Return a copy of the instance's properties in a dictionary.

        :return: a copy of the instance's properties in a dictionary.
        """

        log.info("Get scene properties as dictionary")
        log.debug("as_dict()")

        return {
            "tile_side": self.tile_side,
            "floor_sides_tiles": self.floor_sides_tiles
        }

    def __str__(self):
        """
        Return a string representation of the object. Useful to show the details
        of the scene in logs.
        """

        log.info("Get a string representation of the scene")
        log.debug("__str__()")

        return (f"Scene\n"
                f"- Tile Side: {self.tile_side} mm\n"
                f"- Floor Sides Tiles: {self.floor_sides_tiles} tiles")
