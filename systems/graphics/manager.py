from typing import Dict, Optional

import pygame

from systems.graphics.entity import GraphicEntity
from systems.graphics.system import GraphicSystem, RenderSystemID


class GraphicSystemManager:
    def __init__(self, graphic_systems: Dict[RenderSystemID, GraphicSystem], default_system: Optional[RenderSystemID] = None):
        if not graphic_systems:
            raise ValueError("GraphicSystemManager requires at least one graphic system")
        self.graphic_systems = graphic_systems
        self.default_system = default_system or next(iter(graphic_systems))
        if self.default_system not in self.graphic_systems:
            raise ValueError(f"Default graphic system '{self.default_system}' is not registered")
        self.entities_by_system: Dict[RenderSystemID, list[GraphicEntity]] = {name: [] for name in graphic_systems}
        self.entity_system_map: Dict[int, RenderSystemID] = {}
        self._id_counter: int = 0

    def add_entity(self, entity: GraphicEntity) -> None:
        system_id = entity.system_id or self.default_system
        system = self.graphic_systems.get(system_id)
        if system is None:
            raise ValueError(f"No graphic system registered for id '{system_id}'")

        if entity.id is None:
            self._id_counter += 1
            entity.id = self._id_counter

        bucket = self.entities_by_system[system_id]
        key_sort_function = system.key_sort_function
        if key_sort_function is not None:
            key = key_sort_function(entity)
            for i, e in enumerate(bucket):
                if key < key_sort_function(e):
                    bucket.insert(i, entity)
                    break
            else:
                bucket.append(entity)
        else:
            bucket.append(entity)
        self.entity_system_map[entity.id] = system_id

    def add_entities(self, entities: list[GraphicEntity]) -> None:
        for entity in entities:
            self.add_entity(entity)

    def remove_entity(self, entity: GraphicEntity) -> None:
        if entity.id is None:
            return
        system_id = self.entity_system_map.pop(entity.id, None)
        if system_id is None:
            return
        bucket = self.entities_by_system.get(system_id)
        if bucket is not None and entity in bucket:
            bucket.remove(entity)

    def draw_all(self, screen: pygame.Surface) -> None:
        for system_id, system in sorted(self.graphic_systems.items(), key=lambda kv: kv[1].priority):
            entities = self.entities_by_system.get(system_id, [])
            system.draw_all(screen, entities)
