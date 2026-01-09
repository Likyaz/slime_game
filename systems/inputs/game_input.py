from dataclasses import dataclass

import pygame

from systems.inputs.input import InputContext, RawInput, Action
from systems.physics import Vector


class GameKey:
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    PICK = pygame.K_e
    OPEN_INVENTORY = pygame.K_i

@dataclass(frozen=True)
class GameAction(Action):
    move: Vector
    pick: bool
    open_inventory: bool

class GameInput(InputContext):
    @staticmethod
    def handle(raw_input: RawInput) -> GameAction:
        keys = raw_input.keys   
        move = Vector(0, 0)
        if keys[GameKey.LEFT]:
            move.x = -1
        if keys[GameKey.RIGHT]:
            move.x = 1
        if keys[GameKey.UP]:
            move.y = -1
        if keys[GameKey.DOWN]:
            move.y = 1
        return GameAction(
            move=move,
            pick=keys[GameKey.PICK],
            open_inventory=keys[GameKey.OPEN_INVENTORY]
        )

