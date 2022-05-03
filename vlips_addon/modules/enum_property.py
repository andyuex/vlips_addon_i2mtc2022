from collections import namedtuple
from enum import Enum

EnumPropertyItem = namedtuple("EnumPropertyItem", ["identifier", "name", "description"])


class EnumProperty(EnumPropertyItem, Enum):
    @classmethod
    def to_list(cls):
        values = [tuple(member.value) for role, member in cls.__members__.items()]
        return values
