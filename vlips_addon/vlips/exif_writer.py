import json
import logging

import piexif
import piexif.helper

from .beacon import Beacon
from .camera import Camera
from .scene import Scene

log = logging.getLogger(__name__)


class ExifWriter:
    """
    user_comment -> dictionary with miscellaneous information
    """

    @staticmethod
    def save_exif_data(
            filepath: str,
            scene: Scene,
            beacon: Beacon,
            camera: Camera):
        """
        Save the data from the classes passed as parameters as EXIF data in the
        file which path has been indicated.

        :param filepath: path to the file where the data must be stored.
        :param scene: instance of class Scene, with details about the scene.
        :param beacon: instance of class Beacon, with details about the beacon.
        :param camera: instance of class Camera, with details about the camera.
        """

        log.info(f"Save EXIF data to render file")
        log.debug(f"ExifWriter.save_exif_data("
                  f"filepath={filepath}, "
                  f"scene={scene}, "
                  f"beacon={beacon}, "
                  f"camera={camera})")

        user_comment = {
            "scene": scene.as_dict(),
            "beacon": beacon.as_dict(),
            "camera": camera.as_dict()
        }

        exif_dictionary = {
            "0th": {
                piexif.ImageIFD.Make: camera.make,
                piexif.ImageIFD.Model: f"{camera.model} ({camera.facing.value})",
                piexif.ImageIFD.Software: camera.software
            },
            "Exif": {
                piexif.ExifIFD.FocalLength: camera.get_focal_length_rational(),
                piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(json.dumps(user_comment))
            }
        }

        exif_bytes = piexif.dump(exif_dictionary)
        log.debug(f"exif_dictionary: {exif_dictionary}")

        piexif.insert(exif_bytes, filepath)

    @staticmethod
    def replace_in_user_comment(
            file_path: str,
            old_value: str,
            new_value: str):
        """

        :param file_path:
        :param old_value:
        :param new_value:
        """

        log.info(f"Replace string in user comment")
        log.debug(f"ExifWriter.replace_in_user_comment("
                  f"filepath={file_path}, "
                  f"scene={old_value}, "
                  f"beacon={new_value})")

        exif_dictionary = piexif.load(file_path)
        user_comment_string: str = piexif.helper.UserComment.load(exif_dictionary["Exif"][piexif.ExifIFD.UserComment])
        user_comment_string = user_comment_string.replace(old_value, new_value)
        exif_dictionary = {
            "Exif": {
                piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(user_comment_string)
            }
        }
        exif_bytes = piexif.dump(exif_dictionary)
        piexif.insert(exif_bytes, file_path)
