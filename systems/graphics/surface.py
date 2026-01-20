from abc import ABC
from dataclasses import dataclass
from utils.math.primitive_surface import CirclePrimitiveSurface, RectPrimitiveSurface, RotatedRectPrimitiveSurface


class GraphicSurface(ABC):
    pass


@dataclass(frozen=True)
class PrimitiveGraphicSurface(GraphicSurface):
    color: tuple[int, int, int]

@dataclass(frozen=True)
class CircleGraphicSurface(PrimitiveGraphicSurface, CirclePrimitiveSurface):
    pass

@dataclass(frozen=True)
class RectGraphicSurface(PrimitiveGraphicSurface, RectPrimitiveSurface):
    pass

@dataclass(frozen=True)
class RotatedRectGraphicSurface(PrimitiveGraphicSurface, RotatedRectPrimitiveSurface):
    pass
