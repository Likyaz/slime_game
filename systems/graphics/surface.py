from abc import ABC
from dataclasses import dataclass


class GraphicSurface(ABC):
    pass

@dataclass(frozen=True)
class RectGraphicSurface(GraphicSurface):
    width: float
    height: float

@dataclass(frozen=True)
class RotatedRectGraphicSurface(GraphicSurface):
    width: float
    height: float
    rotation: float

@dataclass(frozen=True)   
class CircleGraphicSurface(GraphicSurface):
    radius: float

