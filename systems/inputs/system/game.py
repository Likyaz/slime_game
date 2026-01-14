from dataclasses import dataclass

import pygame

from systems.vector import Vector
from systems.inputs.system import InputEntity, InputSystem
from systems.inputs.raw_input import RawInput


class GameKey:
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    PICK = pygame.K_e

@dataclass(frozen=True)
class GameInputEntity(InputEntity):
    left: bool
    right: bool
    up: bool
    down: bool
    pick: bool

class GameInputSystem(InputSystem):
    @staticmethod
    def handle(raw_input: RawInput) -> GameInputEntity:
        return GameInputEntity(
            left=raw_input.keys[GameKey.LEFT],
            right=raw_input.keys[GameKey.RIGHT],
            up=raw_input.keys[GameKey.UP],
            down=raw_input.keys[GameKey.DOWN],
            pick=raw_input.keys[GameKey.PICK]
        )
