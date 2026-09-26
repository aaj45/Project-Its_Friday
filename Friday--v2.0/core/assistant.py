import threading
import time

from audio.wake_word import WakeWordListener
from audio.recorder import Recorder
from audio.transcriber import Transcriber
from audio.tts import Speaker
from ai.llm import LLM
from core.memory import MemoryManager
from core.emotion import EmotionEngine


class FridayAssistant:
    def __init__(self):
        self.memory = MemoryManager()
        self.emotion = EmotionEngine()
        self.llm = LLM(self.memory, self.emotion)

        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.speaker = Speaker()

        self.wake_listener = WakeWordListener(self.on_wake)

        self.running = True

    def start(self):
        print("🎙️ Friday is ready.")

        threading.Thread(
            target=self.text_loop,
            daemon=True
        ).start()

        self.wake_listener.start()

        while self.running:
            time.sleep(0.1)

        print("🛑 Friday has shut down.")

    # -------------------
    # TEXT MODE
    # -------------------
    def text_loop(self):
        while self.running:
            try:
                user_input = input("💬 You: ").strip()

                if not user_input:
                    continue

                if self._handle_exit(user_input):
                    return

                self.handle_query(user_input)

            except KeyboardInterrupt:
                self.running = False
                return

    # -------------------
    # VOICE FLOW
    # -------------------
    def on_wake(self):
        if not self.running:
            return

        self.speaker.speak("I'm listening.")

        audio_path = self.recorder.record()
        text = self.transcriber.transcribe(audio_path)

        if not text:
            self.speaker.speak("Sorry, I didn't catch that.")
            return

        print(f"🗣️ You said: {text}")

        if self._handle_exit(text):
            return

        self.handle_query(text)

    # -------------------
    # CORE LOGIC
    # -------------------
    def handle_query(self, text):
        reply = self.llm.ask(text)
        self.speaker.speak(reply)

    # -------------------
    # SHUTDOWN COMMANDS
    # -------------------
    def _handle_exit(self, text):
        text = text.lower().strip()

        exit_commands = [
            "exit",
            "shutdown",
            "go to sleep",
            "good bye",
            "goodbye"
        ]

        if any(command in text for command in exit_commands):
            self.speaker.speak("Goodbye.")

            self.running = False

            try:
                if hasattr(self.wake_listener, "stop"):
                    self.wake_listener.stop()
            except Exception:
                pass

            return True

        return False