import numpy as np


import settings
import sounddevice as sd
from systems.event_bus import EventBus, ChannelEvent
from systems.event_bus import PlaySoundEvent
from systems.audio.source import AudioSource, MixAudioSource
from systems.audio.synth.source import SynthAudioSource
from systems.audio.wav.source import WaveFileAudioSource
from systems.audio.synth.sound import SynthSound
from systems.audio.wav.sound import WaveFileSound
from entities.entity import Entity
from systems.audio.sound import Sound



class AudioSystemManager:
    def __init__(self):
        self.mix = MixAudioSource()
        self.audio_sources = []
        self._audio_stream = sd.OutputStream(
            samplerate=settings.AUDIO_FREQ_ECH,
            blocksize=settings.AUDIO_SAMPLE_SIZE,
            channels=2,
            callback=self._audio_callback
        )

    def start_audio(self) -> None:
        self._audio_stream.start()

    def stop_audio(self) -> None:
        self._audio_stream.stop()

    def play_sounds(self) -> None:
        events = EventBus.poll(ChannelEvent.AUDIO)
        for event in events:
            if isinstance(event, PlaySoundEvent):
                self._play_sound(event.key_sound, event.entity)

    def register_audio_source(self, audio_source_class: type[AudioSource]) -> None:
        if any(isinstance(obj, audio_source_class) for obj in self.audio_sources):
            return
        audio_source = audio_source_class(freq_ech=settings.AUDIO_FREQ_ECH)
        self.mix.add_audio_source(audio_source)
        self.audio_sources.append(audio_source)

    def _audio_callback(self, outdata: np.ndarray, frames: int, time, status) -> None:
        outdata[:] = self.mix.play(frames, time, status)

    def _play_sound(self, key: str, entity: Entity) -> None:
        if entity.audio_entity is None:
            return

        sound = entity.audio_entity.sounds[key]
        if isinstance(sound, SynthSound):
            synth = self._get_audio_source(sound)
            synth.set_sound(sound)
        elif isinstance(sound, WaveFileSound):
            raise NotImplementedError("WaveFileSound not implemented")
        else:
            raise ValueError(f"Unknown sound type: {type(sound)}")

    def _get_audio_source(self, sound: Sound) -> AudioSource:
        if isinstance(sound, SynthSound):
            if not any(isinstance(obj, SynthAudioSource) for obj in self.audio_sources):
                raise RuntimeError("SynthAudioSource not registered")
            return [obj for obj in self.audio_sources if isinstance(obj, SynthAudioSource)][0]
        elif isinstance(sound, WaveFileSound):
            if not any(isinstance(obj, WaveFileAudioSource) for obj in self.audio_sources):
                raise RuntimeError("WaveFileAudioSource not registered")
            return [obj for obj in self.audio_sources if isinstance(obj, WaveFileAudioSource)][0] 
        else:
            raise ValueError(f"Unknown sound type: {type(sound)}")
