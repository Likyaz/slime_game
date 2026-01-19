from dataclasses import dataclass
from utils.math.vector import Vector
from utils.math.primitive_surface import PrimitiveSurface

@dataclass(slots=True)
class GraphicEntity:
    position: Vector
    surface: PrimitiveSurface
    z_index: int = 1
    color: tuple[int, int, int] = (255, 255, 255)
