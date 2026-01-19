from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type, Callable

from systems.actions.controller import ActionController
from systems.actions.action_entity import ActionControllerID, ActionSystemID

if TYPE_CHECKING:
    from entities.entity import Entity
    from systems.actions.system import ActionSystem


class ActionSystemManager:
    def __init__(
        self,
        controller_registry: Dict[ActionControllerID, Callable[[], ActionController]],
        system_registry: Dict[ActionSystemID, Type[ActionSystem]],
    ):
        if not system_registry:
            raise ValueError("ActionSystemManager requires at least one system registered")
        self.controller_registry = controller_registry
        self.system_registry = system_registry
        self.entities: list[Entity] = []

    def add_entity(self, entity: Entity) -> None:
        action_entity = entity.action_entity
        if action_entity is None:
            raise ValueError("Entity registered to ActionSystemManager must have an action_entity")
        if action_entity.system_id not in self.system_registry:
            raise ValueError(f"Unknown action system id '{action_entity.system_id}'")
        if action_entity.controller_id and action_entity.controller_id not in self.controller_registry:
            raise ValueError(f"Unknown action controller id '{action_entity.controller_id}'")

        if action_entity.controller is None and action_entity.controller_id is not None:
            controller_factory = self.controller_registry[action_entity.controller_id]
            action_entity.controller = controller_factory()

        if action_entity.current_action is None and action_entity.controller is not None:
            action_entity.current_action = action_entity.controller.get_default_action()

        self.entities.append(entity)
    
    def add_entities(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.add_entity(entity)
    
    def remove_entity(self, entity: Entity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)

    def remove_entities(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.remove_entity(entity)

    def update_all(self, dt: float) -> None:
        for entity in self.entities:
            action_entity = entity.action_entity

            if action_entity.controller_id is not None:
                if action_entity.controller is None:
                    controller_factory = self.controller_registry[action_entity.controller_id]
                    action_entity.controller = controller_factory()
                action_entity.current_action = action_entity.controller.get_action()

            system = self.system_registry[action_entity.system_id]
            system.apply_action(dt, entity)
