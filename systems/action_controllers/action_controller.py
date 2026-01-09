from abc import ABC, abstractmethod
from dataclasses import dataclass

from systems.physics import Vector

@dataclass(frozen=True)
class EntityAction:
    move: Vector = Vector(0, 0)
    pick: bool = False

class ActionController(ABC):
    @abstractmethod
    def get_action(self, dt: float):
        pass

