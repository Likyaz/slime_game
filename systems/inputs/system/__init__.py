from abc import ABC, abstractmethod

from systems.inputs.raw_input import RawInput


class InputEntity(ABC):
    pass

class InputSystem(ABC):
    @abstractmethod
    def handle(self, raw_input: RawInput) -> InputEntity:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self, input_entity: InputEntity) -> bool:
        raise NotImplementedError
