import numpy as np
from systems.audio.source import AudioSource, SoundReader
from systems.audio.synth.sound import SynthSound, SynthSoundInterpreter
from systems.audio.play_policy import PlayPolicy
from systems.audio.synth.wave_type import WaveType

class SynthAudioSource(AudioSource, SoundReader):
    def __init__(self, freq_ech: float):
        self.sounds = []

        self.freq_ech = freq_ech
        self.prev_time = 0


    def set_sound(self, sound: SynthSound) -> None:
        if sound.play_policy == PlayPolicy.IGNORE and not sound.id in [s.sound.id for s in self.sounds]:
            self.sounds.append(SynthSoundInterpreter.create(sound))
        elif sound.play_policy == PlayPolicy.RESTART:
            if sound.id in [s.sound.id for s in self.sounds]:
                sound_to_remove = [s for s in self.sounds if s.sound.id == sound.id][0]
                self.sounds.append(SynthSoundInterpreter.create(sound, phase=sound_to_remove.phase))
                self.sounds.remove(sound_to_remove)
            else:
                self.sounds.append(SynthSoundInterpreter.create(sound))
        elif sound.play_policy == PlayPolicy.OVERLAP:
            self.sounds.append(SynthSoundInterpreter.create(sound))

    def play(self, frames: int, time, status):
        mix = np.zeros((frames, 2), dtype=np.float32)
        note_to_remove = []
        dt = frames / self.freq_ech

        for sound in self.sounds:
            freq = np.array([sound.sound.freq] * frames)
            phase_d = (2 * np.pi) / (self.freq_ech / freq)
            phase_d[0] += sound.phase
            phase = phase_d.cumsum() % (2 * np.pi)
            sound.phase = phase[-1]
            wave = self._get_sig(phase, sound.sound.wave_type) * sound.sound.amp
            wave = np.column_stack((wave, wave))
            mix += wave
            sound.duration -= dt
            if sound.duration <= 0:
                note_to_remove.append(sound)

        for sound in note_to_remove:
            self.sounds.remove(sound)

        self.prev_time = time.currentTime
        return mix

    def _get_sig(self, phase: np.ndarray, wave_type: WaveType):
        return {
            WaveType.SIN: np.sin(phase),
            WaveType.SQUARD: np.sign(np.sin(phase)),
            WaveType.TRIANGULAR: (2 * (phase % np.pi) / np.pi) - 1,
            WaveType.RAMP: phase / (np.pi) - 1,
        }[wave_type]

