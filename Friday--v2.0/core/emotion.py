import time

class EmotionEngine:
    def __init__(self):
        self.mood = "neutral"
        self.confidence = 0.7
        self.last_interaction = time.time()

    def detect(self, text: str):
        text = text.lower()

        if any(w in text for w in ["angry", "frustrated"]):
            return "concerned"
        if any(w in text for w in ["sad", "tired"]):
            return "gentle"
        if any(w in text for w in ["great", "awesome"]):
            return "enthusiastic"
        if "thank" in text:
            return "friendly"

        return "neutral"

    def update(self, text):
        mood = self.detect(text)
        if mood != "neutral":
            self.mood = mood
            self.last_interaction = time.time()

    def decay(self):
        if time.time() - self.last_interaction > 120:
            self.mood = "neutral"