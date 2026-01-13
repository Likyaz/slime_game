from abc import ABC
from enum import Enum
from systems.event_bus.channel_event import ChannelEvent

class Event(ABC):
    channel: ChannelEvent = ChannelEvent.GLOBAL
