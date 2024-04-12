""" Вспомогательные перечисления. """

from enum import Enum, IntEnum


class Tags(Enum):
    """ Enum тегов для эндпоинтов. """

    users = "users"
    audio = "audio"


class Result(IntEnum):
    """ Enum результатов CRUD операций. """

    Success = 0
    NameExists = 1
    NameTooLong = 2
