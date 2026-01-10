from dataclasses import dataclass, field
from abc import ABC
from systems.physics import Vector


class Action(ABC):
    pass


@dataclass(frozen=True, slots=True)
class EntityAction(Action):
    move: Vector = field(default_factory=lambda: Vector(0, 0))
    pick: bool = False
