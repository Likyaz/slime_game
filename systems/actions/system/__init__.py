from abc import ABC, abstractmethod
from entities.entity import Entity


class ActionSystem(ABC):
    @classmethod
    @abstractmethod
    def apply_actions(self, dt: float, entities: list[Entity]) -> None:
        raise NotImplementedError

