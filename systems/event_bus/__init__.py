from systems.event_bus.event import Event
from systems.event_bus.channel_event import ChannelEvent


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
