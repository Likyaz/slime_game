from dataclasses import dataclass

from systems.event_bus import Event, ChannelEvent
from systems.inputs.system.ui import UIInputEntity
from systems.inputs.system.game import GameInputEntity


@dataclass(frozen=True)
class UIInputEvent(Event):
    input_entity: UIInputEntity
    channel: ChannelEvent = ChannelEvent.INPUT_UI

@dataclass(frozen=True)
class GameInputEvent(Event):
    input_entity: GameInputEntity
    channel: ChannelEvent = ChannelEvent.INPUT_GAME