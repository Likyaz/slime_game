from dataclasses import dataclass
import pygame


@dataclass(frozen=True)
class RawInput:
    keys: pygame.key.ScancodeWrapper
    events: list[pygame.event.Event]
    mouse_position: tuple[int, int]

class RawInputSystem:
    @staticmethod
    def poll():
        return RawInput(
            keys=pygame.key.get_pressed(),
            events=pygame.event.get(),
            mouse_position=pygame.mouse.get_pos(),
        )
