from enum import Enum, auto


class PlayPolicy(Enum):
    OVERLAP = auto()
    RESTART = auto()
    IGNORE = auto()
