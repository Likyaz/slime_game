import pytest

from dataclasses import dataclass

from systems.event_bus import EventBus, Event


@pytest.fixture
def event_bus() -> EventBus:
    return EventBus()

@dataclass(frozen=True)
class EventTest(Event):
    data_test: str

class TestEventBus:
    def test_emit(self, event_bus: EventBus):
        event_bus.emit(EventTest(data_test="test"))
        event = event_bus.events[0]
        assert len(event_bus.events) == 1
        assert isinstance(event, EventTest)
        assert event.data_test == "test"
    
    def test_poll(self, event_bus: EventBus):
        event_bus.events.append(EventTest(data_test="test"))
        events = event_bus.poll()[0]
        assert isinstance(events, EventTest)
        assert events.data_test == "test"
