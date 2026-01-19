import math
import random
from typing import Union
from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    @staticmethod
    def zero() -> "Vector":
        return Vector(0.0, 0.0)

    @staticmethod
    def random_unit_vector(min_angle: float = 0, max_angle: float = 2 * math.pi) -> "Vector":
        angle = random.uniform(min_angle, max_angle)
        return Vector(math.cos(angle), math.sin(angle))

    @staticmethod
    def random_vector(min_length: float, max_length: float) -> "Vector":
        angle = random.uniform(0, 2 * math.pi)
        length = random.uniform(min_length, max_length)
        return Vector(math.cos(angle) * length, math.sin(angle) * length)

    @staticmethod
    def dot(a: "Vector", b: "Vector") -> float:
        return a.x * b.x + a.y * b.y

    x: float = 0
    y: float = 0

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y
    
    def normalize(self) -> "Vector":
        length = math.sqrt(self.x**2 + self.y**2)
        if length == 0:
            return Vector.zero()
        return Vector(self.x / length, self.y / length)

    def add_angle(self, angle: float) -> "Vector":
        angle = self.arg + angle
        return Vector(math.cos(angle), math.sin(angle))
    
    def add_angle_random(self, min_angle: float = 0, max_angle: float = 2 * math.pi) -> "Vector":
        angle = random.uniform(min_angle, max_angle)
        return self.add_angle(angle)
    
    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    @property
    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def arg(self) -> float:
        return math.atan2(self.y, self.x)

    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        raise TypeError(f"Unsupported operand type for +: {type(other)}")

    def __radd__(self, other: Union[int, float]) -> "Vector":
        return self.__add__(other)

    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        raise TypeError(f"Unsupported operand type for -: {type(other)}")

    def __rsub__(self, other: Union[int, float]) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(other - self.x, other - self.y)
        raise TypeError(f"Unsupported operand type for -: {type(other)}")

    def __mul__(self, other: Union[int, float, "Vector"]) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            raise TypeError(f"Unsupported operand type for *: {type(other)}")

    def __truediv__(self, other: Union[int, float, "Vector"]) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        elif isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        else:
            raise TypeError(f"Unsupported operand type for /: {type(other)}")

    def __rtruediv__(self, other: Union[int, float]) -> "Vector":
        return Vector(other / self.x, other / self.y)

    __rmul__ = __mul__
    __imul__ = __mul__
    __iadd__ = __add__
    __isub__ = __sub__

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"