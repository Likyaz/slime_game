from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from systems.actions.action_controller import ActionController
import settings


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



class ActionSystem(ABC):
    @classmethod
    @abstractmethod
    def apply_actions(self, dt: float, entities: list[Entity]) -> None:
        raise NotImplementedError


class AliveActionSystem(ActionSystem):
    @classmethod
    def apply_action(self, dt: float, entity: Entity) -> None:
        move_normalized = entity.entity_action.move.normalize()
        acc = move_normalized * settings.ENTITY_ACCELERATION
        if entity.entity_action.move.length > acc.length:
            entity.physics_entity.acc = entity.entity_action.move
        else:
            entity.physics_entity.acc = acc
