from dataclasses import dataclass

import pygame

from systems.inputs.input import InputContext, RawInput, ActionInput
from systems.vector import Vector


class GameKey:
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    PICK = pygame.K_e
    OPEN_INVENTORY = pygame.K_i

@dataclass(frozen=True)
class GameActionInput(ActionInput):
    move: Vector
    pick: bool
    open_inventory: bool

class GameInput(InputContext):
    @staticmethod
    def handle(raw_input: RawInput) -> GameActionInput:
        keys = raw_input.keys
        move = Vector.zero()
        if keys[GameKey.LEFT]:
            move = Vector(-1, 0)
        if keys[GameKey.RIGHT]:
            move = Vector(1, 0)
        if keys[GameKey.UP]:
            move = Vector(0, -1)
        if keys[GameKey.DOWN]:
            move = Vector(0, 1)
        return GameActionInput(
            move=move,
            pick=keys[GameKey.PICK],
            open_inventory=keys[GameKey.OPEN_INVENTORY]
        )

