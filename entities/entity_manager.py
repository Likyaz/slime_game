from typing import Type

from entities.entity import Entity
from systems.physics import PhysicsEntity
from systems.graphic import GraphicEntity
from systems.actions.action_controller import AIActionController, EntityPerception, EntityInfo
from systems.physics import PhysicsSystem
from systems.graphic import GraphicSystem
from systems.actions.action_system import ActionSystemManager, ActionSystem

class EntityManager:
    def __init__(self, physics_system: PhysicsSystem, graphic_system: GraphicSystem, action_system_manager: ActionSystemManager):
        self.entities: list[Entity] = []
        self.physics_system = physics_system
        self.graphic_system = graphic_system
        self.action_system_manager = action_system_manager

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        if entity.physics_entity and isinstance(entity.physics_entity, PhysicsEntity):
            self.physics_system.add_entity(entity.physics_entity)
        if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
            self.graphic_system.add_entity(entity.graphic_entity)
        if entity.action_system and issubclass(entity.action_system, ActionSystem):
            self.action_system_manager.add_entity(entity)

    def add_entities(self, entities: list[Entity]):
        self.entities.extend(entities)
        for entity in entities:
            if entity.physics_entity and isinstance(entity.physics_entity, PhysicsEntity):
                self.physics_system.add_entity(entity.physics_entity)
            if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
                self.graphic_system.add_entity(entity.graphic_entity)
            if entity.action_system and issubclass(entity.action_system, ActionSystem):
                self.action_system_manager.add_entity(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)
        if entity.physics_entity and isinstance(entity.physics_entity, PhysicsEntity):
            self.physics_system.remove_entity(entity.physics_entity)
        if entity.graphic_entity and isinstance(entity.graphic_entity, GraphicEntity):
            self.graphic_system.remove_entity(entity.graphic_entity)
        if entity.action_system and issubclass(entity.action_system, ActionSystem):
            self.action_system_manager.remove_entity(entity)

    def update_all(self, dt: float):
        for entity in self.entities:
            if not (entity.physics_entity and isinstance(entity.physics_entity, PhysicsEntity)):
                continue
            if entity.action_controller:
                if isinstance(entity.action_controller, AIActionController):
                    entity.action_controller.update_perception(EntityPerception(
                        vel=entity.physics_entity.vel,
                        entities=[
                            EntityInfo(type=e.entity_type, distance=e.physics_entity.position - entity.physics_entity.position)
                            for e in self.entities
                            if entity.physics_entity and isinstance(e.physics_entity, PhysicsEntity)
                        ]
                    )) 
            entity.graphic_entity.position = entity.physics_entity.position

    def cleanup(self):
        pass

