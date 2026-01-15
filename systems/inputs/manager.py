from systems.inputs.system import InputSystem
from systems.inputs.raw_input import RawInput
from systems.inputs.system.ui import UIInputSystem
from systems.event_bus import EventBus
from systems.event_bus.event.input import UIInputEvent, GameInputEvent

class InputSystemManager:
    def __init__(self, input_system: InputSystem, has_ui: bool = False):
        self.input_system = input_system
        self.ui_input_system = UIInputSystem() if has_ui else None

    def handle(self, raw_input: RawInput) -> None:
        if self.ui_input_system is not None:
            ui_input_entity = self.ui_input_system.handle(raw_input)
            if not self.ui_input_system.is_empty(ui_input_entity):
                EventBus.emit(UIInputEvent(input_entity=ui_input_entity))
                return 

        input_entity = self.input_system.handle(raw_input)
        if not self.input_system.is_empty(input_entity):
            EventBus.emit(GameInputEvent(input_entity=input_entity))
