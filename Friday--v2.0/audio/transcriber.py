from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def transcribe(self, path):
        segments, _ = self.model.transcribe(path)
        return " ".join(s.text for s in segments).strip()