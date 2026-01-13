from abc import ABC, abstractmethod
from dataclasses import dataclass

from systems.actions.action import EntityAction, Action
from systems.inputs.system import ActionInput
from systems.vector import Vector
from entities.entity_type import EntityType
from systems.event_bus import EventBus
from systems.event_bus.event.logging import LoggingEvent, LogLevel

class ActionController(ABC):
    @abstractmethod
    def get_action(self) -> Action:
        pass


class PlayerActionController(ActionController):
    def feed_input(self, game_action: ActionInput) -> None:
        EventBus.emit(LoggingEvent(message=f"PlayerActionController.feed_input: {game_action}", level=LogLevel.DEBUG))
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

    def update_perception(self, perception: EntityPerception) -> None:
        self.perception = perception

    def get_action(self) -> EntityAction:
        return self.ia_component.action(self.perception)
