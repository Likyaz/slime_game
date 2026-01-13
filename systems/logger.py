from enum import Enum

from systems.event_bus.event.logging import LogLevel
from systems.event_bus import EventBus, ChannelEvent
import settings


class LoggerManager:
    def __init__(self):
        self.debug_enabled = settings.DEBUG
    
    def update(self):
        events = EventBus.poll(ChannelEvent.LOGGING)
        for event in events:
            if event.level == LogLevel.DEBUG and not self.debug_enabled:
                continue

            print(f"{event.level.name}: {event.message}")
        
