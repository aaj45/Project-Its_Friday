import numpy as np
import sounddevice as sd
import time

from openwakeword.model import Model
from openwakeword.utils import download_models


class WakeWordListener:
    def __init__(
        self,
        on_wake_callback,
        model_name="hey_mycroft",
        threshold=0.6,
        sample_rate=16000,
        block_size=3200,
        debounce_time=1.0
    ):
        self.on_wake_callback = on_wake_callback
        self.threshold = threshold
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.debounce_time = debounce_time

        self.last_trigger_time = 0
        self.is_running = False

        # Load model
        print("🔊 Loading wake word model...")
        download_models()

        self.model = Model(
            wakeword_models=[model_name],
            inference_framework="onnx"
        )

    # -----------------------
    # AUDIO CALLBACK
    # -----------------------
    def _audio_callback(self, indata, frames, time_info, status):
        if not self.is_running:
            return

        audio = np.frombuffer(indata, dtype=np.int16)
        predictions = self.model.predict(audio)

        for score in predictions.values():
            if score > self.threshold:
                self._handle_wake()
                break

    # -----------------------
    # WAKE HANDLER
    # -----------------------
    def _handle_wake(self):
        now = time.time()

        # Debounce (prevent spam triggers)
        if now - self.last_trigger_time < self.debounce_time:
            return

        self.last_trigger_time = now

        print("👂 Wake word detected!")
        self.on_wake_callback()

    # -----------------------
    # START LISTENING
    # -----------------------
    def start(self):
        self.is_running = True

        print("🎧 Wake word listener started...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=1,
            dtype=np.int16,
            callback=self._audio_callback
        ):
            try:
                while self.is_running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop()

    # -----------------------
    # STOP
    # -----------------------
    def stop(self):
        print("🛑 Wake word listener stopped.")
        self.is_running = False