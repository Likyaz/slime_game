from dataclasses import dataclass, field
from systems.audio.sound import Sound

@dataclass(slots=True)
class AudioEntity:
    sounds: dict[str, Sound] = field(default_factory=dict)

