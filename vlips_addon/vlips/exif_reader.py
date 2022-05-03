import json
import logging

import piexif
import piexif.helper

log = logging.getLogger(__name__)


class ExifReader:
    file_path = ""

    def __init__(self, filepath):
        """
        Create an instance of the camera class with the given parameters.

        :param filepath: path to the file to read the EXIF data from.
        """

        log.info("Get a string representation of the camera")
        log.debug(f"__init__("
                  f"filepath={filepath})")

        self.filepath = filepath

    def get_user_comment(self) -> dict:
        """
        Load user comment dictionary from EXIF data.

        :return: user comment dictionary from EXIF data.
        :rtype: dict
        """

        log.info("Get user comments from EXIF data")
        log.debug("get_user_comment()")

        exif_dictionary = piexif.load(self.file_path)
        user_comment_string = piexif.helper.UserComment.load(exif_dictionary["Exif"][piexif.ExifIFD.UserComment])
        user_comment_dictionary = json.loads(user_comment_string)

        return user_comment_dictionary
