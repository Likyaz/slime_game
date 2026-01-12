from systems.physics.system import PhysicSystem
from systems.physics.entity import PhysicEntity
from systems.physics.surface import CollisionEntity, select_collision_resolution
from systems.vector import Vector
import settings

from collections import defaultdict


class TopDownPhysicsSystem(PhysicSystem):
    class KeySortFunction(PhysicSystem.KeySortFunction):
        def __call__(self, entity: PhysicEntity) -> tuple[bool, float]:
            return entity.fixed, entity.mass * -1

    key_sort_function = KeySortFunction()

    def update_all(self, entities: list[PhysicEntity], dt: float) -> None:
        for entity in entities:
            if entity.fixed:
                continue
            entity.vel += entity.acc * dt
            entity.vel -= entity.vel * settings.ENTITY_FRICTION
            if entity.vel.length > settings.ENTITY_MAX_SPEED:
                entity.vel = entity.vel.normalize() * settings.ENTITY_MAX_SPEED
            entity.position += entity.vel * dt


    def resolve_collisions(self, entities: list[PhysicEntity]) -> None:
        potential_pairs = self._find_potential_pairs(entities)
        for _ in range(settings.COLLISION_RESOLUTION_ITERATIONS):

            corrections = defaultdict[int, Vector](Vector)
            for i, j in potential_pairs:
                entity1 = entities[i]
                entity2 = entities[j]
                penetration = select_collision_resolution(
                    CollisionEntity(position=entity1.position, surface=entity1.surface, mass=entity1.mass, fixed=entity1.fixed),
                    CollisionEntity(position=entity2.position, surface=entity2.surface, mass=entity2.mass, fixed=entity2.fixed)
                )
                if penetration.x != 0 or penetration.y != 0:
                    if not entity1.fixed and entity2.fixed:
                        corrections[i] += penetration
                    elif entity1.fixed and not entity2.fixed:
                        corrections[j] -= penetration
                    else:
                        ratio1 = entity1.mass / (entity1.mass + entity2.mass)
                        ratio2 = 1 - ratio1
                        corrections[i] += penetration * ratio2
                        corrections[j] -= penetration * ratio1
            
            for i, correction in corrections.items():
                if not entities[i].fixed:
                    entities[i].position += correction

    def _find_potential_pairs(self, entities: list[PhysicEntity]) -> list[tuple[int, int]]:
        spatial_index = self._build_spatial_index(entities)
        potential_pairs = set[tuple[int, int]]()
        for entity_keys in spatial_index.values():
            for i in entity_keys:
                for j in entity_keys:
                    if i < j and not (entities[i].fixed and entities[j].fixed):
                        potential_pairs.add((i, j))
        return potential_pairs

    def _build_spatial_index(self, entities: list[PhysicEntity]) -> defaultdict[tuple[int, int], list[int]]:
        index = defaultdict[tuple[int, int], list[int]](list)
        for i, entity in enumerate[PhysicEntity](entities):
            self._insert_entity_in_spatial_index(index, i, entities)
        return index

    def _insert_entity_in_spatial_index(self, index: defaultdict[tuple[int, int], list[int]], entity_id: int, entities: list[PhysicEntity]) -> None:
        min_x, min_y, max_x, max_y = entities[entity_id].aabb()

        cx0 = int(min_x // settings.SPATIAL_CELL_SIZE)
        cy0 = int(min_y // settings.SPATIAL_CELL_SIZE)
        cx1 = int(max_x // settings.SPATIAL_CELL_SIZE)
        cy1 = int(max_y // settings.SPATIAL_CELL_SIZE)

        for cx in range(cx0, cx1 + 1):
            for cy in range(cy0, cy1 + 1):
                index[(cx, cy)].append(entity_id)

