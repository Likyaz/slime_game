from entities.entity import Entity
from systems.graphics.entity import GraphicEntity
from systems.physics.manager import PhysicSystemManager
from systems.physics.entity import PhysicEntity
from systems.graphics.manager import GraphicSystemManager
from systems.actions.manager import ActionSystemManager
from systems.actions.system import ActionSystem
from systems.actions.controller.ia import AIActionController, EntityPerception, EntityInfo


class EntityManager:
    def __init__(self, physics_system_manager: PhysicSystemManager, graphic_system_manager: GraphicSystemManager, action_system_manager: ActionSystemManager):
        self.entities: list[Entity] = []
        self.physics_system_manager = physics_system_manager
        self.graphic_system_manager = graphic_system_manager
        self.action_system_manager = action_system_manager

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)
        if entity.physics_entity and isinstance(entity.physics_entity, PhysicEntity):
            self.physics_system_manager.add_entity(entity.physics_entity)
        if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
            self.graphic_system_manager.add_entity(entity.graphic_entity)
        if entity.action_system and issubclass(entity.action_system, ActionSystem):
            self.action_system_manager.add_entity(entity)

    def add_entities(self, entities: list[Entity]) -> None:
        self.entities.extend(entities)
        for entity in entities:
            if entity.physics_entity and isinstance(entity.physics_entity, PhysicEntity):
                self.physics_system_manager.add_entity(entity.physics_entity)
            if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
                self.graphic_system_manager.add_entity(entity.graphic_entity)
            if entity.action_system and issubclass(entity.action_system, ActionSystem):
                self.action_system_manager.add_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)
        if entity.physics_entity and isinstance(entity.physics_entity, PhysicEntity):
            self.physics_system_manager.remove_entity(entity.physics_entity)
        if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
            self.graphic_system_manager.remove_entity(entity.graphic_entity)
        if entity.action_system and issubclass(entity.action_system, ActionSystem):
            self.action_system_manager.remove_entity(entity)

    def update_all(self, dt: float) -> None:
        for entity in self.entities:
            if not (entity.physics_entity and isinstance(entity.physics_entity, PhysicEntity)):
                continue
            if entity.action_controller:
                if isinstance(entity.action_controller, AIActionController):
                    entity.action_controller.update_perception(EntityPerception(
                        vel=entity.physics_entity.vel,
                        entities=[
                            EntityInfo(type=e.entity_type, distance=e.physics_entity.position - entity.physics_entity.position)
                            for e in self.entities
                            if entity.physics_entity and isinstance(e.physics_entity, PhysicEntity)
                        ]
                    ))
            entity.graphic_entity.position = entity.physics_entity.position

    def cleanup(self) -> None:
        pass

