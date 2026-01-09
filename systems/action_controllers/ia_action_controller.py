from dataclasses import dataclass

from systems.action_controllers.action_controller import ActionController, EntityAction
from systems.physics import Vector
from entities.entity_type import EntityType


@dataclass(frozen=True)
class EntityInfo:
    type: EntityType
    distance: Vector


@dataclass(frozen=True)
class EntityPerception:
    vel: Vector
    entities: list[EntityInfo]


class AIActionController(ActionController):
    def __init__(self, ia_component):
        self.ia_component = ia_component
        self.perception = None

    def update_perception(self, perception: EntityPerception):
        self.perception = perception

    def get_action(self) -> EntityAction:
        return self.ia_component.action(self.perception)
