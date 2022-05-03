import datetime
import logging

log = logging.getLogger(__name__)


class Timestamp:
    @staticmethod
    def get(format_string: str) -> str:
        """
        Get a timestamp with the format specified.

        :param format_string: format the timestamp must have.
        :return: timestamp with the format specified.
        :rtype: str
        """

        log.info("Get timestamp with format")
        log.debug(f"Timestamp.get("
                  f"format_string={format_string}")

        timestamp = datetime.datetime.now().strftime(format_string)

        return timestamp

    @staticmethod
    def file() -> str:
        """
        Get a file timestamp.

        :return: timestamp for a file
        :rtype: str
        """

        log.info("Get timestamp for a file")
        log.debug(f"Timestamp.file()")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        return timestamp

    @staticmethod
    def gps() -> str:
        """
        Get a GPS timestamp.

        :return: timestamp for GPS.
        :rtype: str
        """

        log.info("Get timestamp for a GPS")
        log.debug(f"Timestamp.gps()")

        return Timestamp.get("%Y:%m:%d")
