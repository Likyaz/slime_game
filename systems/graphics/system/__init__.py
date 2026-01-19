from abc import ABC, abstractmethod
from enum import Enum, auto
import pygame

from systems.graphics.entity import GraphicEntity


class RenderSystemID(Enum):
    WORLD = auto()
    UI = auto()
    DEBUG = auto()


class GraphicSystem(ABC):
    class KeySortFunction(ABC):
        @abstractmethod
        def __call__(self, entity: GraphicEntity) -> tuple:
            raise NotImplementedError("Subclass must implement this method")

    priority: int = 0

    key_sort_function: KeySortFunction = None

    @abstractmethod
    def draw_all(self, screen: pygame.Surface, entities: list[GraphicEntity]) -> None:
        raise NotImplementedError("Subclass must implement this method")
