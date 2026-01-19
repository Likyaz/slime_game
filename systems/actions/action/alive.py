from dataclasses import dataclass, field
from utils.math.vector import Vector
from systems.actions.action import Action


@dataclass(frozen=True, slots=True)
class AliveActionEntity(Action):
    move: Vector = field(default_factory=lambda: Vector(0, 0))
    pick: bool = False
