from collections import defaultdict
from dataclasses import dataclass
import math
from abc import ABC

import settings
from systems.vector import Vector

class PhysicSurface(ABC):
    pass

@dataclass(frozen=True)
class RectPhysicSurface(PhysicSurface):
    width: float
    height: float


@dataclass(frozen=True)
class RotatedRectPhysicSurface(PhysicSurface):
    width: float
    height: float
    rotation: float

@dataclass(frozen=True)   
class CirclePhysicSurface(PhysicSurface):
    radius: float


@dataclass(slots=True)   
class PhysicEntity:
    position: Vector
    surface: PhysicSurface
    vel: Vector = Vector.zero()
    acc: Vector = Vector.zero()
    mass: float = 1.0
    fixed: bool = False

    def aabb(self) -> tuple[float, float, float, float]:
        if isinstance(self.surface, RectPhysicSurface):
            return (
                self.position.x - self.surface.width / 2,
                self.position.y - self.surface.height / 2,
                self.position.x + self.surface.width / 2,
                self.position.y + self.surface.height / 2
            )
        elif isinstance(self.surface, CirclePhysicSurface):
            return (
                self.position.x - self.surface.radius,
                self.position.y - self.surface.radius,
                self.position.x + self.surface.radius,
                self.position.y + self.surface.radius
            )   
        else:
            raise ValueError(f"Unsupported physic surface type: {type(self.surface)}")


class PhysicSystem:
    def __init__(self, entities: list[PhysicEntity]=None):
        self.entities = entities or []

    def sort_entities(self) -> None:
        self.entities.sort(key=lambda x: (x.fixed, x.mass * -1))

    def add_entity(self, entity: PhysicEntity) -> None:
        self.entities.append(entity)
        self.sort_entities()

    def add_entities(self, entities: list[PhysicEntity]) -> None:
        self.entities.extend(entities)
        self.sort_entities()

    def remove_entity(self, entity: PhysicEntity) -> None:
        self.entities.remove(entity)

    def update_all(self, dt: float) -> None:
        for entity in self.entities:
            if entity.fixed:
                continue
            entity.vel += entity.acc * dt
            entity.position += entity.vel * dt
            entity.vel -= entity.vel * settings.ENTITY_FRICTION

        self.resolve_collisions()

    def find_potential_pairs(self) -> list[tuple[int, int]]:
        spatial_index = self.build_spatial_index()
        potential_pairs = set()
        for entity_keys in spatial_index.values():
            for i in entity_keys:
                for j in entity_keys:
                    if i < j and not (self.entities[i].fixed and self.entities[j].fixed):
                        potential_pairs.add((i, j))
        return potential_pairs

    def build_spatial_index(self) -> defaultdict[tuple[int, int], list[int]]:
        index = defaultdict(list)
        for i, entity in enumerate(self.entities):
            self._insert_entity_in_spatial_index(index, i)
        return index

    def _insert_entity_in_spatial_index(self, index: defaultdict[tuple[int, int], list[int]], entity_id: int) -> None:
        min_x, min_y, max_x, max_y = self.entities[entity_id].aabb()

        cx0 = int(min_x // settings.SPATIAL_CELL_SIZE)
        cy0 = int(min_y // settings.SPATIAL_CELL_SIZE)
        cx1 = int(max_x // settings.SPATIAL_CELL_SIZE)
        cy1 = int(max_y // settings.SPATIAL_CELL_SIZE)

        for cx in range(cx0, cx1 + 1):
            for cy in range(cy0, cy1 + 1):
                index[(cx, cy)].append(entity_id)


    def resolve_collisions(self) -> None:
        potential_pairs = self.find_potential_pairs()
        for _ in range(settings.COLLISION_RESOLUTION_ITERATIONS):

            corrections = defaultdict(Vector)
            for i, j in potential_pairs:
                entity1 = self.entities[i]
                entity2 = self.entities[j]
                penetration = self._select_collision_resolution(entity1, entity2)
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
            
            sorted_corrections = sorted(corrections.items(), key=lambda x: x[1].length)
            for i, correction in sorted_corrections:
                if not self.entities[i].fixed:
                    self.entities[i].position += correction

    def _select_collision_resolution(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
                surface_set = {type(entity1.surface), type(entity2.surface)}
                if len(surface_set) == 1:
                    if CirclePhysicSurface in surface_set:
                        return self._resolve_circle_vs_circle(entity1, entity2)
                    elif RectPhysicSurface in surface_set:
                        return self._resolve_rect_vs_rect(entity1, entity2)
                    elif RotatedRectPhysicSurface in surface_set:
                        return self._resolve_rotated_rect_vs_rotated_rect(entity1, entity2)
                    else:
                        raise ValueError(f"Unsupported surface type: {entity1.surface} and {entity2.surface}")
                else:
                    if CirclePhysicSurface in surface_set and RectPhysicSurface in surface_set:
                        if isinstance(entity1.surface, CirclePhysicSurface):
                            return self._resolve_circle_vs_rect(entity1, entity2)
                        else:
                            return self._resolve_circle_vs_rect(entity2, entity1) * -1
                    elif CirclePhysicSurface in surface_set and RotatedRectPhysicSurface in surface_set:
                        if isinstance(entity1.surface, CirclePhysicSurface):
                            return self._resolve_circle_vs_rotated_rect(entity1, entity2)
                        else:
                            return self._resolve_circle_vs_rotated_rect(entity2, entity1) * -1
                    elif RectPhysicSurface in surface_set and RotatedRectPhysicSurface in surface_set:
                        if isinstance(entity1.surface, RectPhysicSurface):
                            return self._resolve_rect_vs_rotated_rect(entity1, entity2)
                        else:
                            return self._resolve_rect_vs_rotated_rect(entity2, entity1) * -1
                    else:
                        raise ValueError(f"Unsupported surface type: {entity1.surface} and {entity2.surface}")

    def _resolve_rect_vs_rotated_rect(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
        def dot(a: Vector, b: Vector) -> float:
            return a.x * b.x + a.y * b.y

        def get_axes(entity: PhysicEntity) -> tuple[Vector, Vector]:
            angle = entity.surface.rotation if isinstance(entity.surface, RotatedRectPhysicSurface) else 0
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            return (Vector(cos_a, sin_a), Vector(-sin_a, cos_a))

        def get_extent(axis: Vector, entity: PhysicEntity) -> float:
            hw = entity.surface.width / 2
            hh = entity.surface.height / 2
            ax1, ax2 = get_axes(entity)
            return hw * abs(dot(axis, ax1)) + hh * abs(dot(axis, ax2))

        axes1 = get_axes(entity1)
        axes2 = get_axes(entity2)
        axes = axes1 + axes2
        delta = entity2.position - entity1.position

        min_overlap = float("inf")
        min_axis = None

        for axis in axes:
            distance = abs(dot(delta, axis))
            overlap = get_extent(axis, entity1) + get_extent(axis, entity2) - distance
            if overlap <= 0:
                return
            if overlap < min_overlap:
                min_overlap = overlap
                direction = 1 if dot(delta, axis) > 0 else -1
                min_axis = Vector(axis.x * direction, axis.y * direction)

        if min_axis is not None:
            penetration = min_axis * min_overlap
            return penetration
        return Vector.zero()

    def _resolve_circle_vs_rotated_rect(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
        circle, rect = entity1, entity2
        angle = rect.surface.rotation
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Transform circle center into rect local space
        rel_x = circle.position.x - rect.position.x
        rel_y = circle.position.y - rect.position.y
        local_x = rel_x * cos_a + rel_y * sin_a
        local_y = -rel_x * sin_a + rel_y * cos_a

        hw, hh = rect.surface.width / 2, rect.surface.height / 2
        clamped_x = max(-hw, min(local_x, hw))
        clamped_y = max(-hh, min(local_y, hh))

        dx = local_x - clamped_x
        dy = local_y - clamped_y
        dist_sq = dx * dx + dy * dy
        r = circle.surface.radius

        if dist_sq <= (r * r):
            distance = math.sqrt(dist_sq)
            if distance == 0:
                normal_local = Vector(1, 0)
            else:
                normal_local = Vector(dx / distance, dy / distance)

            # Rotate normal back to world space
            normal_world = Vector(
                normal_local.x * cos_a - normal_local.y * sin_a,
                normal_local.x * sin_a + normal_local.y * cos_a,
            )
            penetration = normal_world * (r - distance)
            return penetration
        return Vector.zero()

    def _resolve_rotated_rect_vs_rotated_rect(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
        def dot(a: Vector, b: Vector) -> float:
            return a.x * b.x + a.y * b.y

        def get_axes(entity: PhysicEntity) -> tuple[Vector, Vector]:
            angle = entity.surface.rotation if isinstance(entity.surface, RotatedRectPhysicSurface) else 0
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            return (Vector(cos_a, sin_a), Vector(-sin_a, cos_a))

        def get_extent(axis: Vector, entity: PhysicEntity) -> float:
            hw = entity.surface.width / 2
            hh = entity.surface.height / 2
            ax1, ax2 = get_axes(entity)
            return hw * abs(dot(axis, ax1)) + hh * abs(dot(axis, ax2))

        axes1 = get_axes(entity1)
        axes2 = get_axes(entity2)
        axes = axes1 + axes2
        delta = entity2.position - entity1.position

        min_overlap = float("inf")
        min_axis = None

        for axis in axes:
            distance = abs(dot(delta, axis))
            overlap = get_extent(axis, entity1) + get_extent(axis, entity2) - distance
            if overlap <= 0:
                return
            if overlap < min_overlap:
                min_overlap = overlap
                direction = 1 if dot(delta, axis) > 0 else -1
                min_axis = Vector(axis.x * direction, axis.y * direction)

        if min_axis is not None:
            penetration = min_axis * min_overlap
            return penetration
        return Vector.zero()

    def _resolve_circle_vs_circle(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
        r = entity1.surface.radius + entity2.surface.radius
        dx = entity1.position.x - entity2.position.x
        dy = entity1.position.y - entity2.position.y
        dist_sq = dx * dx + dy * dy

        if dist_sq <= (r * r):
            distance = math.sqrt(dist_sq)
            if dist_sq == 0:
                normal = Vector.random_unit_vector()
            else:
                normal = Vector(dx / distance, dy / distance) 
            penetration = r - distance
            return normal * penetration
        return Vector.zero()
    
    def _resolve_rect_vs_rect(self, entity1: PhysicEntity, entity2: PhysicEntity) -> Vector:
        dx = entity2.position.x - entity1.position.x
        px = (entity1.surface.width / 2 + entity2.surface.width / 2) - abs(dx)
        dy = entity2.position.y - entity1.position.y
        py = (entity1.surface.height / 2 + entity2.surface.height / 2) - abs(dy)

        if px > 0 and py > 0:
            if px < py:
                penetration = Vector(px if dx > 0 else -px, 0)
            else:
                penetration = Vector(0, py if dy > 0 else -py)
            return penetration
        return Vector.zero()

    def _resolve_circle_vs_rect(self, circle: PhysicEntity, rect: PhysicEntity) -> Vector:
        cx, cy = circle.position.x, circle.position.y

        half_w = rect.surface.width / 2
        half_h = rect.surface.height / 2

        left   = rect.position.x - half_w
        right  = rect.position.x + half_w
        top    = rect.position.y - half_h
        bottom = rect.position.y + half_h

        closest_x = max(left, min(cx, right))
        closest_y = max(top, min(cy, bottom))

        dx = cx - closest_x
        dy = cy - closest_y
        dist_sq = dx*dx + dy*dy
        r = circle.surface.radius
    
        if dist_sq != 0:
            distance = math.sqrt(dist_sq)
            penetration = circle.surface.radius - distance

            if penetration <= 0:
                return Vector.zero()
            normal = Vector(dx/distance, dy/distance)
            correction = normal * penetration
            return correction
        
        else:
            pen_x = min(right - cx, cx - left)
            pen_y = min(bottom - cy, cy - top)

            if pen_x < pen_y:
                normal = Vector(-1 if cx < rect.position.x else 1, 0)
                penetration = pen_x + circle.surface.radius
            else:
                normal = Vector(0, -1 if cy < rect.position.y else 1)
                penetration = pen_y + circle.surface.radius

            correction = normal * penetration
            return correction

