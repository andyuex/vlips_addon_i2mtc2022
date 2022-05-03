import os

from PIL import Image
from rich import print


class ArgumentParserHelper:

    @staticmethod
    def parse_data_file_path(data_file_path, check_is_file: bool = True):
        if data_file_path == "":
            print("[red]path to data file not provided")
            exit(1)

        if check_is_file:
            if not os.path.isfile(data_file_path):
                print(f"[red]cannot open data file {data_file_path}")
                exit(1)

        return data_file_path

    @staticmethod
    def parse_directory_path(directory_path):
        if directory_path == "":
            print("[red]path to directory not provided")
            exit(1)

        if not os.path.isdir(directory_path):
            print(f"[red]cannot open directory {directory_path}")
            exit(1)

        return directory_path

    @staticmethod
    def parse_code(code_as_string):
        code = -1

        if code_as_string == "":
            print("[red]code emitted not provided")
            exit(1)

        try:
            code = int(code_as_string)
        except ValueError:
            print("[red]code emitted is not a number")
            exit(1)

        if code < 0:
            print("[red]code emitted can't be negative")
            exit(1)

        return code

    @staticmethod
    def parse_image_path(image_path):
        if image_path == "" or image_path is None:
            print("[red]path to image not provided")
            exit(1)

        try:
            Image.open(image_path)
        except IOError:
            print("[red]cannot open {image_path}")
            exit(1)

        return image_path

    @staticmethod
    def parse_integer(integer_as_string):
        integer_value = 0

        if integer_as_string == "":
            print("[red]integer not provided")
            exit(1)

        try:
            integer_value = int(integer_as_string)
        except ValueError:
            print("[red]integer provided is not a number")
            exit(1)

        return integer_value

    @staticmethod
    def parse_float(float_as_string):
        float_value = 0.0

        if float_as_string == "":
            print("[red]float not provided")
            exit(1)

        try:
            float_value = float(float_as_string)
        except ValueError:
            print("[red]float provided is not a number")
            exit(1)

        return float_value
