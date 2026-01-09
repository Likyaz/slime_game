import math
from dataclasses import dataclass
import pygame

import settings
from systems.utils_surface import Vector, Surface, RectSurface, CircleSurface, RotatedRectSurface

@dataclass(slots=True)
class GraphicEntity:
    position: Vector
    surface: Surface
    z_index: int = 1
    color: tuple[int, int, int] = (255, 255, 255)

class GraphicSystem:
    def __init__(self):
        self.entities = []

    def add_entity(self, entity: GraphicEntity) -> None:
        self.entities.append(entity)
        self.entities.sort(key=lambda x: x.z_index)

    def add_entities(self, entities: list[GraphicEntity]) -> None:
        self.entities.extend(entities)
        self.entities.sort(key=lambda x: x.z_index)

    def remove_entity(self, entity: GraphicEntity) -> None:
        self.entities.remove(entity)

    def draw_all(self, screen: pygame.Surface) -> None:
        for entity in self.entities:
            if isinstance(entity.surface, CircleSurface):
                pygame.draw.circle(screen, entity.color, entity.position.to_tuple(), entity.surface.radius)
            elif isinstance(entity.surface, RectSurface):
                rect = pygame.Rect(
                    int(entity.position.x - entity.surface.width / 2),
                    int(entity.position.y - entity.surface.height / 2),
                    int(entity.surface.width),
                    int(entity.surface.height),
                )
                pygame.draw.rect(screen, entity.color, rect)
            elif isinstance(entity.surface, RotatedRectSurface):
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

