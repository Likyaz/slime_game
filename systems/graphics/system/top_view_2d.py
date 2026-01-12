import pygame

from systems.graphics.system import GraphicSystem
from systems.graphics.entity import GraphicEntity
from systems.graphics.surface import RectGraphicSurface, RotatedRectGraphicSurface, CircleGraphicSurface
from systems.vector import Vector
import math


class TopView2DGraphicSystem(GraphicSystem):
    class KeySortFunction(GraphicSystem.KeySortFunction):
        def __call__(self, entity: GraphicEntity) -> tuple:
            return entity.z_index

    key_sort_function = KeySortFunction()

    def draw_all(self, screen: pygame.Surface, entities: list[GraphicEntity]) -> None:
        for entity in entities:
            if isinstance(entity.surface, CircleGraphicSurface):
                pygame.draw.circle(screen, entity.color, entity.position.to_tuple(), entity.surface.radius)
            elif isinstance(entity.surface, RectGraphicSurface):
                rect = pygame.Rect(
                    int(entity.position.x - entity.surface.width / 2),
                    int(entity.position.y - entity.surface.height / 2),
                    int(entity.surface.width),
                    int(entity.surface.height),
                )
                pygame.draw.rect(screen, entity.color, rect)
            elif isinstance(entity.surface, RotatedRectGraphicSurface):
                hw = entity.surface.width / 2
                hh = entity.surface.height / 2
                angle = entity.surface.rotation
                cos_a = math.cos(angle)
                sin_a = math.sin(angle)
                corners = [
                    Vector(-hw, -hh),
                    Vector(hw, -hh),
                    Vector(hw, hh),
                    Vector(-hw, hh),
                ]
                points = []
                for c in corners:
                    x = c.x * cos_a - c.y * sin_a + entity.position.x
                    y = c.x * sin_a + c.y * cos_a + entity.position.y
                    points.append((x, y))
                pygame.draw.polygon(screen, entity.color, points)
            else:
                raise ValueError(f"Unsupported surface type: {type(entity.surface)}")
