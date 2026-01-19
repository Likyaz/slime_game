from dataclasses import dataclass

import pygame


from systems.inputs.system import InputEntity, InputSystem
from systems.inputs.raw_input import RawInput
from utils.math.vector import Vector


class UIKey:
    ESCAPE = pygame.K_ESCAPE
    ENTER = pygame.K_RETURN
    SPACE = pygame.K_SPACE
    TAB = pygame.K_TAB
    BACKSPACE = pygame.K_BACKSPACE
    DELETE = pygame.K_DELETE
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    MOUSE_LEFT = 0
    MOUSE_MIDDLE = 1
    MOUSE_RIGHT = 2


@dataclass(frozen=True)
class UIInputEntity(InputEntity):
    pointer_pos: Vector
    pointer_down: bool
    pointer_up: bool
    confirm: bool
    cancel: bool


class UIInputSystem(InputSystem):
    @staticmethod
    def handle(raw_input: RawInput) -> None:
        return UIInputEntity(
            pointer_pos=Vector(raw_input.mouse_position[0], raw_input.mouse_position[1]),
            pointer_down=raw_input.pressed_keys[UIKey.MOUSE_LEFT],
            pointer_up=raw_input.pressed_keys[UIKey.MOUSE_RIGHT],
            confirm=raw_input.keys[UIKey.ENTER],
            cancel=raw_input.keys[UIKey.ESCAPE]
        )

    @staticmethod
    def is_empty(input_entity: UIInputEntity) -> bool:
        return not any([
            input_entity.pointer_down,
            input_entity.pointer_up,
            input_entity.confirm,
            input_entity.cancel
        ])

