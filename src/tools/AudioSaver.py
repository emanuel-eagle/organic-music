import numpy as np
import soundfile as sf
import os
from datetime import datetime

class AudioSaver:
    def __init__(self, sample_rate=44100, output_dir="./samples"):
        self._sample_rate = sample_rate
        self._output_dir = output_dir
        self._frames = []
        os.makedirs(output_dir, exist_ok=True)

    def record(self, freq, duration=0.5):
        t = np.linspace(0, duration, int(self._sample_rate * duration), endpoint=False)
        frame = 0.3 * np.sin(2 * np.pi * freq * t).astype(np.float32)
        self._frames.append(frame)

    def save_from_stream(self, audio, sample_rate):
        if audio is None:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._output_dir, f"plant_{timestamp}.wav")
        sf.write(path, audio, sample_rate)
        print(f"Saved to {path}")

    def clear(self):
        self._frames = []