from abc import ABC, abstractmethod

from systems.physics.entity import PhysicEntity



class PhysicSystem(ABC):
    class KeySortFunction(ABC):
        @abstractmethod
        def __call__(self, entity: PhysicEntity) -> tuple:
            raise NotImplementedError("Subclass must implement this method")

    key_sort_function: KeySortFunction = None

    @abstractmethod
    def update_all(self, entities: list[PhysicEntity], dt: float) -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def resolve_collisions(self, entities: list[PhysicEntity]) -> None:
        raise NotImplementedError("Subclass must implement this method")
