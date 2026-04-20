import numpy as np
import sounddevice as sd
import threading

class Sound:
    def __init__(self, sample_rate=44100, freq_min=200, freq_max=2000, device=2):
        self._sample_rate = sample_rate
        self._freq_min = freq_min
        self._freq_max = freq_max
        self._device = device
        self._freq = freq_min
        self._recording = False
        self._recorded_frames = []
        self._phase = 0.0
        self._lock = threading.Lock()
        self._stream = sd.OutputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype='float32',
            device=self._device,
            callback=self._callback
        )
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        with self._lock:
            freq = self._freq
        t = (self._phase + np.arange(frames)) / self._sample_rate
        audio = 0.3 * np.sin(2 * np.pi * freq * t).astype(np.float32)
        outdata[:, 0] = audio
        self._phase += frames
        if self._recording:
            self._recorded_frames.append(audio.copy())

    # frequency
    def get_freq(self):
        return self._freq

    def set_freq(self, freq):
        if freq <= 0:
            raise ValueError("Frequency must be positive")
        with self._lock:
            self._freq = freq

    # frequency range
    def get_freq_min(self):
        return self._freq_min

    def set_freq_min(self, value):
        if value <= 0:
            raise ValueError("Minimum frequency must be positive")
        if value >= self._freq_max:
            raise ValueError("Minimum frequency must be less than maximum frequency")
        self._freq_min = value

    def get_freq_max(self):
        return self._freq_max

    def set_freq_max(self, value):
        if value <= 0:
            raise ValueError("Maximum frequency must be positive")
        if value <= self._freq_min:
            raise ValueError("Maximum frequency must be greater than minimum frequency")
        self._freq_max = value

    def get_sample_rate(self):
        return self._sample_rate

    def set_sample_rate(self, value):
        if value <= 0:
            raise ValueError("Sample rate must be positive")
        self._sample_rate = value

    # playback
    def play_freq(self, freq):
        self.set_freq(freq)

    def play_normalized(self, value):
        if not 0 <= value <= 1:
            raise ValueError("Normalized value must be between 0 and 1")
        freq = self._freq_min + value * (self._freq_max - self._freq_min)
        self.play_freq(freq)

    def stop(self):
        self._stream.stop()
        self._stream.close()

    def start_recording(self):
        with self._lock:
            self._recording = True
            self._recorded_frames = []

    def stop_recording(self):
        with self._lock:
            self._recording = False
            frames = self._recorded_frames.copy()
        return np.concatenate(frames) if frames else None