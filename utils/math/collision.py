import math
from typing import Tuple

from utils.math.vector import Vector
from utils.math.primitive_surface import (
    PrimitiveSurface,
    CirclePrimitiveSurface,
    RectPrimitiveSurface,
    RotatedRectPrimitiveSurface,
)


CollisionResult = Tuple[bool, Vector, Vector]


def compute_aabb(pos: Vector, surface: PrimitiveSurface) -> tuple[float, float, float, float]:
    """Axis-aligned bounding box for a primitive surface at a given position."""
    if isinstance(surface, RectPrimitiveSurface):
        hw = surface.width / 2
        hh = surface.height / 2
        return (
            pos.x - hw,
            pos.y - hh,
            pos.x + hw,
            pos.y + hh,
        )
    if isinstance(surface, CirclePrimitiveSurface):
        r = surface.radius
        return (
            pos.x - r,
            pos.y - r,
            pos.x + r,
            pos.y + r,
        )
    if isinstance(surface, RotatedRectPrimitiveSurface):
        hw = surface.width / 2
        hh = surface.height / 2
        cos_a = abs(math.cos(surface.rotation))
        sin_a = abs(math.sin(surface.rotation))
        ext_x = hw * cos_a + hh * sin_a
        ext_y = hw * sin_a + hh * cos_a
        return (
            pos.x - ext_x,
            pos.y - ext_y,
            pos.x + ext_x,
            pos.y + ext_y,
        )
    raise ValueError(f"Unsupported surface type for AABB: {type(surface)}")


def detect_collision(
    pos_a: Vector, surface_a: PrimitiveSurface, pos_b: Vector, surface_b: PrimitiveSurface
) -> bool:
    """Dispatch collision detection based on primitive surface types."""
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return detect_circle_vs_circle(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return detect_circle_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return detect_rect_vs_circle(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return detect_rect_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return detect_rect_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return detect_rotated_rect_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return detect_rotated_rect_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return detect_circle_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return detect_rotated_rect_vs_circle(pos_a, surface_a, pos_b, surface_b)
    raise ValueError(f"Unsupported primitive surfaces: {type(surface_a)} and {type(surface_b)}")


def resolve_collision(
    pos_a: Vector, surface_a: PrimitiveSurface, pos_b: Vector, surface_b: PrimitiveSurface
) -> CollisionResult:
    """Dispatch collision resolution based on primitive surface types.

    Returns:
        (detected, correction_pos_a, correction_pos_b)
        correction vectors separate A from B; if no collision both vectors are zero.
    """
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return resolve_circle_vs_circle(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return resolve_circle_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return resolve_rect_vs_circle(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return resolve_rect_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RectPrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return resolve_rect_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, RectPrimitiveSurface):
        return resolve_rotated_rect_vs_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return resolve_rotated_rect_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, CirclePrimitiveSurface) and isinstance(surface_b, RotatedRectPrimitiveSurface):
        return resolve_circle_vs_rotated_rect(pos_a, surface_a, pos_b, surface_b)
    if isinstance(surface_a, RotatedRectPrimitiveSurface) and isinstance(surface_b, CirclePrimitiveSurface):
        return resolve_rotated_rect_vs_circle(pos_a, surface_a, pos_b, surface_b)
    raise ValueError(f"Unsupported primitive surfaces: {type(surface_a)} and {type(surface_b)}")


def detect_circle_vs_circle(pos_a: Vector, circle_a: CirclePrimitiveSurface, pos_b: Vector, circle_b: CirclePrimitiveSurface) -> bool:
    detected, _, _ = resolve_circle_vs_circle(pos_a, circle_a, pos_b, circle_b)
    return detected


def resolve_circle_vs_circle(
    pos_a: Vector, circle_a: CirclePrimitiveSurface, pos_b: Vector, circle_b: CirclePrimitiveSurface
) -> CollisionResult:
    combined_radius = circle_a.radius + circle_b.radius
    dx = pos_a.x - pos_b.x
    dy = pos_a.y - pos_b.y
    dist_sq = dx * dx + dy * dy

    if dist_sq > combined_radius * combined_radius:
        return _no_collision()

    distance = math.sqrt(dist_sq) if dist_sq != 0 else 0
    if distance == 0:
        normal = Vector.random_unit_vector()
    else:
        normal = Vector(dx / distance, dy / distance)

    penetration_depth = combined_radius - distance
    mtv = normal * penetration_depth
    return True, mtv, -mtv


def detect_rect_vs_rect(pos_a: Vector, rect_a: RectPrimitiveSurface, pos_b: Vector, rect_b: RectPrimitiveSurface) -> bool:
    detected, _, _ = resolve_rect_vs_rect(pos_a, rect_a, pos_b, rect_b)
    return detected


def resolve_rect_vs_rect(
    pos_a: Vector, rect_a: RectPrimitiveSurface, pos_b: Vector, rect_b: RectPrimitiveSurface
) -> CollisionResult:
    dx = pos_b.x - pos_a.x
    dy = pos_b.y - pos_a.y
    px = (rect_a.width / 2 + rect_b.width / 2) - abs(dx)
    py = (rect_a.height / 2 + rect_b.height / 2) - abs(dy)

    if px <= 0 or py <= 0:
        return _no_collision()

    if px < py:
        normal = Vector(-1 if dx > 0 else 1, 0)
        penetration = px
    else:
        normal = Vector(0, -1 if dy > 0 else 1)
        penetration = py

    mtv = normal * penetration
    return True, mtv, -mtv


def detect_circle_vs_rect(
    pos_circle: Vector, circle: CirclePrimitiveSurface, pos_rect: Vector, rect: RectPrimitiveSurface
) -> bool:
    detected, _, _ = resolve_circle_vs_rect(pos_circle, circle, pos_rect, rect)
    return detected


def resolve_circle_vs_rect(
    pos_circle: Vector, circle: CirclePrimitiveSurface, pos_rect: Vector, rect: RectPrimitiveSurface
) -> CollisionResult:
    cx, cy = pos_circle.x, pos_circle.y

    half_w = rect.width / 2
    half_h = rect.height / 2

    left = pos_rect.x - half_w
    right = pos_rect.x + half_w
    top = pos_rect.y - half_h
    bottom = pos_rect.y + half_h

    closest_x = max(left, min(cx, right))
    closest_y = max(top, min(cy, bottom))

    dx = cx - closest_x
    dy = cy - closest_y
    dist_sq = dx * dx + dy * dy
    radius = circle.radius

    if dist_sq > radius * radius:
        return _no_collision()

    if dist_sq != 0:
        distance = math.sqrt(dist_sq)
        penetration = radius - distance
        normal = Vector(dx / distance, dy / distance)
    else:
        pen_x = min(right - cx, cx - left)
        pen_y = min(bottom - cy, cy - top)
        if pen_x < pen_y:
            normal = Vector(-1 if cx < pos_rect.x else 1, 0)
            penetration = pen_x + radius
        else:
            normal = Vector(0, -1 if cy < pos_rect.y else 1)
            penetration = pen_y + radius

    mtv = normal * penetration
    return True, mtv, -mtv


def detect_rect_vs_circle(
    pos_rect: Vector, rect: RectPrimitiveSurface, pos_circle: Vector, circle: CirclePrimitiveSurface
) -> bool:
    detected, _, _ = resolve_rect_vs_circle(pos_rect, rect, pos_circle, circle)
    return detected


def resolve_rect_vs_circle(
    pos_rect: Vector, rect: RectPrimitiveSurface, pos_circle: Vector, circle: CirclePrimitiveSurface
) -> CollisionResult:
    detected, mtv_circle, mtv_rect = resolve_circle_vs_rect(pos_circle, circle, pos_rect, rect)
    if not detected:
        return _no_collision()
    return True, mtv_rect, mtv_circle


def detect_rect_vs_rotated_rect(
    pos_rect: Vector, rect: RectPrimitiveSurface, pos_rot: Vector, rot_rect: RotatedRectPrimitiveSurface
) -> bool:
    detected, _, _ = resolve_rect_vs_rotated_rect(pos_rect, rect, pos_rot, rot_rect)
    return detected


def resolve_rect_vs_rotated_rect(
    pos_rect: Vector, rect: RectPrimitiveSurface, pos_rot: Vector, rot_rect: RotatedRectPrimitiveSurface
) -> CollisionResult:
    detected, mtv = _sat_penetration_rotated_rects(
        pos_rect, rect.width, rect.height, 0.0,
        pos_rot, rot_rect.width, rot_rect.height, rot_rect.rotation
    )
    if not detected:
        return _no_collision()
    return True, mtv, -mtv


def detect_rotated_rect_vs_rect(
    pos_rot: Vector, rot_rect: RotatedRectPrimitiveSurface, pos_rect: Vector, rect: RectPrimitiveSurface
) -> bool:
    detected, _, _ = resolve_rotated_rect_vs_rect(pos_rot, rot_rect, pos_rect, rect)
    return detected


def resolve_rotated_rect_vs_rect(
    pos_rot: Vector, rot_rect: RotatedRectPrimitiveSurface, pos_rect: Vector, rect: RectPrimitiveSurface
) -> CollisionResult:
    detected, mtv = _sat_penetration_rotated_rects(
        pos_rot, rot_rect.width, rot_rect.height, rot_rect.rotation,
        pos_rect, rect.width, rect.height, 0.0
    )
    if not detected:
        return _no_collision()
    return True, mtv, -mtv


def detect_rotated_rect_vs_rotated_rect(
    pos_a: Vector, rect_a: RotatedRectPrimitiveSurface, pos_b: Vector, rect_b: RotatedRectPrimitiveSurface
) -> bool:
    detected, _, _ = resolve_rotated_rect_vs_rotated_rect(pos_a, rect_a, pos_b, rect_b)
    return detected


def resolve_rotated_rect_vs_rotated_rect(
    pos_a: Vector, rect_a: RotatedRectPrimitiveSurface, pos_b: Vector, rect_b: RotatedRectPrimitiveSurface
) -> CollisionResult:
    detected, mtv = _sat_penetration_rotated_rects(
        pos_a, rect_a.width, rect_a.height, rect_a.rotation,
        pos_b, rect_b.width, rect_b.height, rect_b.rotation
    )
    if not detected:
        return _no_collision()
    return True, mtv, -mtv


def detect_circle_vs_rotated_rect(
    pos_circle: Vector, circle: CirclePrimitiveSurface, pos_rect: Vector, rect: RotatedRectPrimitiveSurface
) -> bool:
    detected, _, _ = resolve_circle_vs_rotated_rect(pos_circle, circle, pos_rect, rect)
    return detected


def resolve_circle_vs_rotated_rect(
    pos_circle: Vector, circle: CirclePrimitiveSurface, pos_rect: Vector, rect: RotatedRectPrimitiveSurface
) -> CollisionResult:
    angle = rect.rotation
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    rel_x = pos_circle.x - pos_rect.x
    rel_y = pos_circle.y - pos_rect.y
    local_x = rel_x * cos_a + rel_y * sin_a
    local_y = -rel_x * sin_a + rel_y * cos_a

    hw, hh = rect.width / 2, rect.height / 2
    clamped_x = max(-hw, min(local_x, hw))
    clamped_y = max(-hh, min(local_y, hh))

    dx = local_x - clamped_x
    dy = local_y - clamped_y
    dist_sq = dx * dx + dy * dy
    radius = circle.radius

    if dist_sq > radius * radius:
        return _no_collision()

    if dist_sq == 0:
        pen_x = min(hw - local_x, local_x + hw)
        pen_y = min(hh - local_y, local_y + hh)
        if pen_x < pen_y:
            normal_local = Vector(1 if local_x > 0 else -1, 0)
            penetration = pen_x + radius
        else:
            normal_local = Vector(0, 1 if local_y > 0 else -1)
            penetration = pen_y + radius
    else:
        distance = math.sqrt(dist_sq)
        penetration = radius - distance
        normal_local = Vector(dx / distance, dy / distance)

    normal_world = Vector(
        normal_local.x * cos_a - normal_local.y * sin_a,
        normal_local.x * sin_a + normal_local.y * cos_a,
    )
    mtv = normal_world * penetration
    return True, mtv, -mtv


def detect_rotated_rect_vs_circle(
    pos_rect: Vector, rect: RotatedRectPrimitiveSurface, pos_circle: Vector, circle: CirclePrimitiveSurface
) -> bool:
    detected, _, _ = resolve_rotated_rect_vs_circle(pos_rect, rect, pos_circle, circle)
    return detected


def resolve_rotated_rect_vs_circle(
    pos_rect: Vector, rect: RotatedRectPrimitiveSurface, pos_circle: Vector, circle: CirclePrimitiveSurface
) -> CollisionResult:
    detected, mtv_circle, mtv_rect = resolve_circle_vs_rotated_rect(pos_circle, circle, pos_rect, rect)
    if not detected:
        return _no_collision()
    return True, mtv_rect, mtv_circle


def _sat_penetration_rotated_rects(
    pos_a: Vector, width_a: float, height_a: float, rotation_a: float,
    pos_b: Vector, width_b: float, height_b: float, rotation_b: float
) -> tuple[bool, Vector]:
    """Separating Axis Test between two oriented rectangles."""
    axes_a = _get_axes(rotation_a)
    axes_b = _get_axes(rotation_b)
    axes = axes_a + axes_b
    delta = pos_b - pos_a

    min_overlap = float("inf")
    min_axis: Vector | None = None

    for axis in axes:
        distance = abs(delta.dot(axis))
        overlap = _get_extent(axis, width_a, height_a, rotation_a) + _get_extent(axis, width_b, height_b, rotation_b) - distance
        if overlap <= 0:
            return False, Vector.zero()
        if overlap < min_overlap:
            min_overlap = overlap
            direction = 1 if delta.dot(axis) < 0 else -1
            min_axis = Vector(axis.x * direction, axis.y * direction)

    if min_axis is None:
        return False, Vector.zero()

    penetration = min_axis * min_overlap
    return True, penetration


def _get_axes(rotation: float) -> tuple[Vector, Vector]:
    cos_a = math.cos(rotation)
    sin_a = math.sin(rotation)
    return Vector(cos_a, sin_a), Vector(-sin_a, cos_a)


def _get_extent(axis: Vector, width: float, height: float, rotation: float) -> float:
    hw = width / 2
    hh = height / 2
    ax1, ax2 = _get_axes(rotation)
    return hw * abs(axis.dot(ax1)) + hh * abs(axis.dot(ax2))


def _no_collision() -> CollisionResult:
    zero = Vector.zero()
    return False, zero, zero
