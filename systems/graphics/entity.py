from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from utils.math.vector import Vector
from systems.graphics.surface import GraphicSurface

if TYPE_CHECKING:
    from systems.graphics.system import RenderSystemID


@dataclass(slots=True)
class GraphicEntity:
    position: Vector
    active_surface: str
    surfaces: dict[str, GraphicSurface] = None
    z_index: int = 1
    visible: bool = True
    id: Optional[int] = None
    system_id: Optional["RenderSystemID"] = None
