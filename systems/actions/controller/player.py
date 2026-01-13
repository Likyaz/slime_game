from systems.actions.controller import ActionController
from systems.actions.action import EntityAction
from systems.inputs.system import ActionInput
from systems.event_bus import EventBus
from systems.event_bus.event.logging import LoggingEvent
from systems.event_bus.event.logging import LogLevel


class PlayerActionController(ActionController):
    def feed_input(self, game_action: ActionInput) -> None:
        EventBus.emit(LoggingEvent(message=f"PlayerActionController.feed_input: {game_action}", level=LogLevel.DEBUG))
        self.last_action = EntityAction(
            move=game_action.move,
            pick=game_action.pick
        )

    def get_action(self) -> EntityAction:
        return self.last_action
