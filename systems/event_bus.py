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
    LOGGING = 'logging'

class Event(ABC):
    channel: ChannelEvent = ChannelEvent.GLOBAL


class EventBus:
    events: list[Event] = []

    @classmethod
    def emit(self, event: Event):
        self.events.append(event)

    @classmethod
    def poll(self, channel: ChannelEvent = ChannelEvent.GLOBAL):
        if channel != ChannelEvent.GLOBAL:
            events = []
            for event in self.events:
                if event.channel == channel:
                    events.append(event)

            for event in events:
                self.events.remove(event)

            return events
        else:
            events = self.events
            self.events = []
            return events
