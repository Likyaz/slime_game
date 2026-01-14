from systems.actions.controller import InputActionController
from systems.actions.action.alive import AliveActionEntity
from systems.inputs.system import InputEntity
from systems.event_bus import EventBus
from systems.event_bus.event.logging import LoggingEvent
from systems.event_bus.event.logging import LogLevel
from systems.vector import Vector


class PlayerActionController(InputActionController):
    def feed_input(self, action_input: InputEntity) -> None:
        EventBus.emit(LoggingEvent(message=f"PlayerActionController.feed_input: {action_input}", level=LogLevel.DEBUG))
        move = Vector(0, 0)
        if action_input.left:
            move += Vector(-1, 0)
        if action_input.right:
            move += Vector(1, 0)
        if action_input.up:
            move += Vector(0, -1)
        if action_input.down:
            move += Vector(0, 1)
        self.last_action = AliveActionEntity(
            move=move,
            pick=action_input.pick
        )

    def get_default_action(self) -> AliveActionEntity:
        return AliveActionEntity()

    def get_action(self) -> AliveActionEntity:
        return self.last_action
