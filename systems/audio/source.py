from abc import ABC, abstractmethod
import numpy as np
from systems.audio.sound import Sound


class AudioSource(ABC):
    @abstractmethod
    def play(self, frames: int, time, status):
        raise NotImplementedError("Subclass must implement this method")

class SoundReader(ABC):
    @abstractmethod
    def set_sound(self, sound: Sound) -> None:
        raise NotImplementedError("Subclass must implement this method")

class MixAudioSource(AudioSource):
    def __init__(self, audio_sources: list[AudioSource] = []):
        self.audio_sources = audio_sources
    
    def add_audio_source(self, audio_source: AudioSource) -> None:
        self.audio_sources.append(audio_source)
    
    def remove_audio_source(self, audio_source: AudioSource) -> None:
        self.audio_sources.remove(audio_source)

    def play(self, frames: int, time, status):
        mix = np.zeros((frames, 2), dtype=np.float32)

        for audio_source in self.audio_sources:
            mix += audio_source.play(frames, time, status)

        return np.clip(mix, -1, 1)

