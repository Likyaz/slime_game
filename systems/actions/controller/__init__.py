from abc import ABC, abstractmethod
from systems.actions.action import Action
from systems.inputs.system import InputEntity


class ActionController(ABC):
    @abstractmethod
    def get_default_action(self) -> Action:
        pass

    @abstractmethod
    def get_action(self) -> Action:
        pass
