from dataclasses import dataclass

import pygame

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

    @staticmethod
    def is_empty(input_entity: GameInputEntity) -> bool:
        return not any([
            input_entity.left,
            input_entity.right,
            input_entity.up,
            input_entity.down,
            input_entity.pick
        ])
