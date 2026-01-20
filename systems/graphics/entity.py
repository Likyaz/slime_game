from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from utils.math.vector import Vector
from utils.math.primitive_surface import PrimitiveSurface

if TYPE_CHECKING:
    from systems.graphics.system import RenderSystemID


@dataclass(slots=True)
class GraphicEntity:
    position: Vector
    surface: PrimitiveSurface
    z_index: int = 1
    color: tuple[int, int, int] = (255, 255, 255)
    visible: bool = True
    id: Optional[int] = None
    system_id: Optional["RenderSystemID"] = None
