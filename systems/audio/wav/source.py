import numpy as np
from systems.audio.source import AudioSource, SoundReader
from systems.audio.wav.sound import WaveFileSound


class WaveFileAudioSource(AudioSource, SoundReader):
    def set_sound(self, sound: WaveFileSound) -> None:
        pass

    def play(self, frames: int, time, status):
        pass
