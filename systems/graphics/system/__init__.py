from abc import ABC, abstractmethod

from systems.graphics.entity import GraphicEntity



class GraphicSystem(ABC):
    class KeySortFunction(ABC):
        @abstractmethod
        def __call__(self, entity: GraphicEntity) -> tuple:
            raise NotImplementedError("Subclass must implement this method")

    key_sort_function: KeySortFunction = None

    @abstractmethod
    def draw_all(self, entities: list[GraphicEntity], dt: float) -> None:
        raise NotImplementedError("Subclass must implement this method")
