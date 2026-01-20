import pygame

from systems.graphics.system import GraphicSystem
from systems.graphics.entity import GraphicEntity
from utils.math.primitive_surface import RectPrimitiveSurface, RotatedRectPrimitiveSurface, CirclePrimitiveSurface
from utils.math.vector import Vector
import math


class Primitive2DGraphicSystem(GraphicSystem):
    class KeySortFunction(GraphicSystem.KeySortFunction):
        def __call__(self, entity: GraphicEntity) -> tuple:
            return entity.z_index

    key_sort_function = KeySortFunction()

    def draw_all(self, screen: pygame.Surface, entities: list[GraphicEntity]) -> None:
        for entity in entities:
            surface = entity.surfaces[entity.active_surface]
            if surface is None:
                raise ValueError(f"No surface found for entity {entity.id}")

            if isinstance(surface, CirclePrimitiveSurface):
                pygame.draw.circle(screen, surface.color, entity.position.to_tuple(), surface.radius)
            elif isinstance(surface, RectPrimitiveSurface):
                rect = pygame.Rect(
                    int(entity.position.x - surface.width / 2),
                    int(entity.position.y - surface.height / 2),
                    int(surface.width),
                    int(surface.height),
                )
                pygame.draw.rect(screen, surface.color, rect)
            elif isinstance(surface, RotatedRectPrimitiveSurface):
                hw = surface.width / 2
                hh = surface.height / 2
                angle = surface.rotation
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
