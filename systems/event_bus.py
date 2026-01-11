from abc import ABC
from dataclasses import dataclass
from enum import Enum

import settings
from entities.entity import Entity

class ChannelEvent(Enum):
    # ==== GLOBAL EVENTS ====
    GLOBAL = 'global'

    # ==== ENGINE EVENTS ====
    AUDIO = 'audio'

    # ==== LOGGING EVENTS ====
    DEBUG = 'debug'

class Event(ABC):
    channel: ChannelEvent = ChannelEvent.GLOBAL

@dataclass(frozen=True)
class PlaySoundEvent(Event):
    key_sound: str
    entity: Entity
    channel: ChannelEvent = ChannelEvent.AUDIO

@dataclass(frozen=True)
class DebugEvent(Event):
    message: str
    channel: ChannelEvent = ChannelEvent.DEBUG


class EventBus:
    events: list[Event] = []

    @classmethod
    def emit(self, event: Event):
        if not settings.DEBUG and event.channel == ChannelEvent.DEBUG:
            return
        self.events.append(event)

    @classmethod
    def poll(self, channel: ChannelEvent = ChannelEvent.GLOBAL):
        if channel != ChannelEvent.GLOBAL:
            events = []
            for event in self.events:
                if event.channel == channel:
                    events.append(event)
                    self.events.remove(event)
            return events
        else:
            events = self.events
            self.events = []
            return events
