from dataclasses import dataclass
from systems.audio.sound import Sound


@dataclass(frozen=True)
class WaveFileSound(Sound):
    pass
