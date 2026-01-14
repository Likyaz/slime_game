from systems.inputs.system import InputSystem, InputEntity
from systems.inputs.raw_input import RawInput


class InputSystemManager:
    def __init__(self, input_system: InputSystem):
        self.input_system = input_system

    def handle(self, raw_input: RawInput) -> InputEntity:
        return self.input_system.handle(raw_input)
