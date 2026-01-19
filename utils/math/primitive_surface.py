from dataclasses import dataclass


class PrimitiveSurface:
    pass


@dataclass(frozen=True, slots=True)
class RectPrimitiveSurface(PrimitiveSurface):
    width: float
    height: float


@dataclass(frozen=True, slots=True)
class CirclePrimitiveSurface(PrimitiveSurface):
    radius: float


@dataclass(frozen=True, slots=True)
class RotatedRectPrimitiveSurface(PrimitiveSurface):
    width: float
    height: float
    rotation: float
