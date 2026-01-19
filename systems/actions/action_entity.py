from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from systems.actions.controller import ActionController
    from systems.actions.action import Action


class ActionControllerID(Enum):
    PLAYER = auto()
    AI_SLIME = auto()


class ActionSystemID(Enum):
    ALIVE = auto()


@dataclass(slots=True)
class ActionEntity:
    system_id: ActionSystemID
    controller_id: Optional[ActionControllerID] = None
    controller: Optional[ActionController] = None
    current_action: Optional[Action] = None
