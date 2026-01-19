from dataclasses import dataclass
from utils.math.vector import Vector
from utils.math.primitive_surface import PrimitiveSurface


@dataclass(slots=True)
class PhysicEntity:
    position: Vector
    surface: PrimitiveSurface
    vel: Vector = Vector.zero()
    acc: Vector = Vector.zero()
    mass: float = 1.0
    fixed: bool = False
