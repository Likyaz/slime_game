from dataclasses import dataclass
from systems.audio.sound import Sound
from systems.audio.synth.wave_type import WaveType
import numpy as np


@dataclass(frozen=True)
class SynthSound(Sound):
    freq: float
    amp: float
    wave_type: WaveType
    duration: float


@dataclass
class SynthSoundInterpreter:
    sound: SynthSound
    duration: float
    phase: float = 0

    @staticmethod
    def create(synth_sound: SynthSound, phase: float = 0) -> np.ndarray:
        return SynthSoundInterpreter(sound=synth_sound, duration=synth_sound.duration, phase=phase)

