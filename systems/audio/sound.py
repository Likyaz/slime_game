from dataclasses import dataclass, field
from abc import ABC
import uuid
from systems.audio.play_policy import PlayPolicy


@dataclass(frozen=True, kw_only=True)
class Sound(ABC):
    id: int = field(default_factory=lambda: id(uuid.uuid4()), init=False)
    play_policy: PlayPolicy = PlayPolicy.OVERLAP
