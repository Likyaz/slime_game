from dataclasses import dataclass
from systems.vector import Vector
from systems.physics.surface import PhysicSurface, RectPhysicSurface, CirclePhysicSurface


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
