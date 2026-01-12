import pygame

from systems.graphics.entity import GraphicEntity
from systems.graphics.system import GraphicSystem

class GraphicSystemManager:
    def __init__(self, graphic_system: GraphicSystem):
        self.graphic_system = graphic_system
        self.entities = []

    def add_entity(self, entity: GraphicEntity) -> None:
        if self.graphic_system.key_sort_function is not None:
            key_sort_function = self.graphic_system.key_sort_function
            key = key_sort_function(entity)
            for i, e in enumerate[GraphicEntity](self.entities):
                if key < key_sort_function(e):
                    self.entities.insert(i, entity)
                    return

            self.entities.append(entity)
        else:
            self.entities.append(entity)

    def add_entities(self, entities: list[GraphicEntity]) -> None:
        for entity in entities:
            self.add_entity(entity)

    def remove_entity(self, entity: GraphicEntity) -> None:
        self.entities.remove(entity)

    def draw_all(self, screen: pygame.Surface) -> None:
        self.graphic_system.draw_all(screen, self.entities)