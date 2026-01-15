from systems.actions.controller import ActionController
from systems.actions.action.alive import AliveActionEntity
from systems.inputs.system.game import GameInputEntity
from systems.event_bus import EventBus
from systems.event_bus.channel_event import ChannelEvent
from systems.vector import Vector


class PlayerActionController(ActionController):
    def _create_alive_action(self, action_input: GameInputEntity) -> AliveActionEntity:
        move = Vector(0, 0)
        if action_input.left:
            move += Vector(-1, 0)
        if action_input.right:
            move += Vector(1, 0)
        if action_input.up:
            move += Vector(0, -1)
        if action_input.down:
            move += Vector(0, 1)
        return AliveActionEntity(
            move=move,
            pick=action_input.pick
        )

    def get_default_action(self) -> AliveActionEntity:
        return AliveActionEntity()

    def get_action(self) -> AliveActionEntity:
        for event in EventBus.poll(ChannelEvent.INPUT_GAME):
            return self._create_alive_action(event.input_entity)
        
        return self.get_default_action()