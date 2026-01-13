from __future__ import annotations

from typing import TYPE_CHECKING

from systems.actions.controller import ActionController

if TYPE_CHECKING:
    from entities.entity import Entity


class ActionSystemManager:
    def __init__(self):
        self.entities = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
    
    def add_entities(self, entities: list[Entity]):
        self.entities.extend(entities)
    
    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def remove_entities(self, entities: list[Entity]):
        for entity in entities:
            self.remove_entity(entity)

    def update_all(self, dt: float):
        for entity in self.entities:
            if entity.action_controller and isinstance(entity.action_controller, ActionController):
                entity_action = entity.action_controller.get_action()
                entity.entity_action = entity_action

            entity.action_system.apply_action(dt, entity)
