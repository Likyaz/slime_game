from abc import ABC, abstractmethod
from systems.actions.action import ActionEntity
from systems.inputs.system import InputEntity


class ActionController(ABC):
    @abstractmethod
    def get_default_action(self) -> ActionEntity:
        pass

    @abstractmethod
    def get_action(self) -> ActionEntity:
        pass

class InputActionController(ActionController):
    @abstractmethod
    def feed_input(self, action_input: InputEntity) -> None:
        pass
