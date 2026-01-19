from abc import ABC, abstractmethod
from entities.entity import Entity


class ActionSystem(ABC):
    @classmethod
    @abstractmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
        raise NotImplementedError

