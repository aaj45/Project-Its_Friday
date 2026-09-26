import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import uuid


class Recorder:
    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        dtype="float32",
        duration=5,
        output_dir="audio_files"
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.duration = duration
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------
    # RECORD AUDIO
    # -----------------------
    def record(self) -> str:
        print("🎧 Listening for command...")

        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype
        )

        sd.wait()

        file_path = os.path.join(
            self.output_dir,
            f"{uuid.uuid4().hex}.wav"
        )

        sf.write(file_path, audio, self.sample_rate)

        return file_path