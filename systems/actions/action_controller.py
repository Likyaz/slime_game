from abc import ABC, abstractmethod
from dataclasses import dataclass

from systems.actions.action import EntityAction, Action
from systems.inputs.input import ActionInput
from systems.physics import Vector
from entities.entity_type import EntityType

class ActionController(ABC):
    @abstractmethod
    def get_action(self) -> Action:
        pass


class PlayerActionController(ActionController):
    def feed_input(self, game_action: ActionInput) -> None:
        self.last_action = EntityAction(
            move=game_action.move,
            pick=game_action.pick
        )

    def get_action(self) -> EntityAction:
        return self.last_action


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
