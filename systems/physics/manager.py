from systems.physics.system import PhysicSystem
from systems.physics.entity import PhysicEntity


class PhysicSystemManager:
    def __init__(self, physic_system: PhysicSystem):
        self.physic_system = physic_system
        self.entities = []

    def add_entity(self, entity: PhysicEntity) -> None:
        if self.physic_system.key_sort_function is not None:
            key_sort_function = self.physic_system.key_sort_function
            key = key_sort_function(entity)
            for i, e in enumerate[PhysicEntity](self.entities):
                if key < key_sort_function(e):
                    self.entities.insert(i, entity)
                    return

            self.entities.append(entity)
        else:
            self.entities.append(entity)

    def add_entities(self, entities: list[PhysicEntity]) -> None:
        for entity in entities:
            self.add_entity(entity)

    def remove_entity(self, entity: PhysicEntity) -> None:
        self.entities.remove(entity)

    def update_all(self, dt: float) -> None:
        self.physic_system.update_all(self.entities, dt)
        self.physic_system.resolve_collisions(self.entities)
