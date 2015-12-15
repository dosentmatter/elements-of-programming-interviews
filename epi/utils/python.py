from enum import Enum

class Parameter(Enum):
    """
    Formal Parameter constants.

    OTHER_ARGUMENT is used when this parameter is to be replaced in terms of
    another argument.
    """

    OTHER_ARGUMENT = 1
