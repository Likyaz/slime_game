from abc import ABC, abstractmethod
from systems.actions.action import Action


class ActionController(ABC):
    @abstractmethod
    def get_action(self) -> Action:
        pass
