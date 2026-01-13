from dataclasses import dataclass

from systems.event_bus import Event, ChannelEvent
from entities.entity import Entity


@dataclass(frozen=True)
class PlaySoundEvent(Event):
    key_sound: str
    entity: Entity
    channel: ChannelEvent = ChannelEvent.AUDIO
