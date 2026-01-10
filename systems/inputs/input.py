from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame


@dataclass(frozen=True)
class RawInput:
    keys: pygame.key.ScancodeWrapper
    events: list[pygame.event.Event]
    mouse_position: tuple[int, int]

class InputSystem:
    @staticmethod
    def poll():
        return RawInput(
            keys=pygame.key.get_pressed(),
            events=pygame.event.get(),
            mouse_position=pygame.mouse.get_pos(),
        )

class ActionInput(ABC):
    pass

class InputContext(ABC):
    @abstractmethod
    def handle(self, raw_input: RawInput) -> ActionInput:
        raise NotImplementedError