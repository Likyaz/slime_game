from dataclasses import dataclass, field
from systems.vector import Vector
from systems.actions.action import ActionEntity


@dataclass(frozen=True, slots=True)
class AliveActionEntity(ActionEntity):
    move: Vector = field(default_factory=lambda: Vector(0, 0))
    pick: bool = False
