from dataclasses import dataclass
from enum import Enum
from systems.event_bus import Event, ChannelEvent
from systems.event_bus.channel_event import ChannelEvent


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

@dataclass(frozen=True)
class LoggingEvent(Event):
    message: str
    channel: ChannelEvent = ChannelEvent.LOGGING
    level: LogLevel = LogLevel.DEBUG
