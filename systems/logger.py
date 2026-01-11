from dataclasses import dataclass
from enum import Enum

from systems.event_bus import Event
from systems.event_bus import EventBus, ChannelEvent
import settings

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


class LoggerManager:
    def __init__(self):
        self.debug_enabled = settings.DEBUG
    
    def update(self):
        events = EventBus.poll(ChannelEvent.LOGGING)
        for event in events:
            if event.level == LogLevel.DEBUG and not self.debug_enabled:
                continue

            print(f"{event.level.name}: {event.message}")
        
