from enum import Enum


class EntityType(Enum):
    NONE = "none"
    PLAYER = "player"
    SOLID = "solid"
    SLIME = "slime"
    VISUAL = "visual"
    ITEM = "item"