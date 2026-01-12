from dataclasses import dataclass
from systems.vector import Vector
from systems.graphics.surface import GraphicSurface

@dataclass(slots=True)
class GraphicEntity:
    position: Vector
    surface: GraphicSurface
    z_index: int = 1
    color: tuple[int, int, int] = (255, 255, 255)
