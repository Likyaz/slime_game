from abc import ABC, abstractmethod
from systems.actions.action import ActionEntity
from systems.inputs.system import ActionInput


class ActionController(ABC):
    @abstractmethod
    def get_action(self) -> ActionEntity:
        pass

class InputActionController(ActionController):
    @abstractmethod
    def feed_input(self, action_input: ActionInput) -> None:
        pass
