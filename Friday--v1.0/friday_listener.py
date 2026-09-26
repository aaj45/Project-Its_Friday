import os
import time
import uuid
import subprocess
import numpy as np
import sounddevice as sd
import soundfile as sf
import ollama
import threading

from openwakeword.model import Model
from openwakeword.utils import download_models
from faster_whisper import WhisperModel

import json

# ====================
# EMOTIONAL STATE
# ====================

emotion_state = {
    "mood": "neutral",      # neutral | friendly | concerned | enthusiastic | tired
    "confidence": 0.7,      # 0.0–1.0
    "last_interaction": time.time()
}

def detect_emotion(text: str):
    text = text.lower()

    if any(w in text for w in ["angry", "annoyed", "frustrated", "stupid"]):
        return "concerned"
    if any(w in text for w in ["sad", "down", "tired", "exhausted"]):
        return "gentle"
    if any(w in text for w in ["excited", "awesome", "great", "love"]):
        return "enthusiastic"
    if any(w in text for w in ["thanks", "thank you", "appreciate"]):
        return "friendly"

    return "neutral"

def update_emotion(user_text):
    global emotion_state

    new_mood = detect_emotion(user_text)

    if new_mood != "neutral":
        emotion_state["mood"] = new_mood
        emotion_state["last_interaction"] = time.time()

def decay_emotion():
    global emotion_state
    if time.time() - emotion_state["last_interaction"] > 120:
        emotion_state["mood"] = "neutral"


# ====================
# LONG-TERM MEMORY
# ====================

MEMORY_FILE = "fridays_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"facts": [], "dialogue": []}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Backward compatibility
        if isinstance(data, list):
            return {"facts": [], "dialogue": data}

        data.setdefault("facts", [])
        data.setdefault("dialogue", [])

        return data
        
    except Exception as e:
        print(f"⚠️ Memory load failed, starting fresh: {e}")
        return {"facts": [], "dialogue": []}  # add dialogue here



def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

long_term_memory = load_memory()

def extract_memory(text):
    text = text.lower()

    patterns = [
        "my name is",
        "i am called",
        "i like",
        "i love",
        "i hate",
        "i live in",
        "i work as",
        "remember that"
    ]

    for p in patterns:
        if p in text:
            return text

    return None




# ====================
# CONFIG
# ====================
SAMPLE_RATE = 16000
BLOCK_SIZE = 3200
THRESHOLD = 0.6
DEBOUNCE_TIME = 1.0
COMMAND_DURATION = 5  # seconds

PIPER_EXE = r"C:\piper\piper.exe"
PIPER_MODEL = r"C:\piper\voices\en_GB-alba-medium.onnx"
AUDIO_DIR = r"C:\Users\akifj\jarvis\audio"

os.makedirs(AUDIO_DIR, exist_ok=True)


# ====================
# INIT MODELS
# ====================
download_models()

wake_model = Model(
    wakeword_models=["hey_mycroft"],
    inference_framework="onnx"
)

print("🔊 Loading Whisper model...")
whisper = WhisperModel("base", device="cpu", compute_type="int8")

# ====================
# GLOBAL FLAGS
# ====================
TEXT_MODE = True   # Allows typing commands anytime
VOICE_MODE = True  # Keeps wake word detection active
is_thinking = False # Thinking animation flag
# ====================
# STATE
# ====================
last_trigger_time = 0
is_listening_for_command = False
is_speaking = False

# --------------------
# CONVERSATION MEMORY
# --------------------
conversation = [
    {
        "role": "system",
        "content": (
            "You are Friday, a calm, intelligent personal assistant. "
            "You remember past conversations and use them when relevant. "
            "Be concise, helpful, and conversational."
            "Known facts about the user:\n"
            + "\n".join(long_term_memory["facts"])
        )
    }
]

# Inject long-term memory
conversation.extend(long_term_memory.get("dialogue", []))

MAX_TURNS = 10  # prevents infinite memory growth

# =====================
# THINKING ANIMATION
# =====================

def thinking_indicator():
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while is_thinking:
        print(f"\r🤖 Friday is thinking {spinner[i % len(spinner)]}", end="", flush=True)
        time.sleep(0.15)
        i += 1
    print("\r" + " " * 40 + "\r", end="", flush=True)



# ====================
# LOCAL LLM (OLLAMA)
# ====================
def ask_llm(prompt):
    global conversation, long_term_memory, is_thinking

    update_emotion(prompt)

    personality_prompt = (
        f"You are Friday, a calm, intelligent personal assistant.\n"
        f"Current mood: {emotion_state['mood']}.\n"
        f"Confidence level: {emotion_state['confidence']}.\n"
        f"Adjust your tone naturally to match the mood.\n"
        f"Do not mention moods explicitly unless relevant."
    )

    conversation[0] = {
        "role": "system",
        "content": personality_prompt
    }

    # Add user message to short-term memory
    conversation.append({"role": "user", "content": prompt})

    # Start thinking indicator
    is_thinking = True
    thinker = threading.Thread(target=thinking_indicator, daemon=True)
    thinker.start()

    try:
        response = ollama.chat(
            model="llama3",
            messages=conversation
        )

        reply = response["message"]["content"]

        # Add user message to short-term memory
        conversation.append({"role": "assistant", "content": reply})

        # Save dialogue memory
        long_term_memory["dialogue"].append({"role": "user", "content": prompt})
        long_term_memory["dialogue"].append({"role": "assistant", "content": reply})

        # Limits entriess to last 100
        long_term_memory["dialogue"] = long_term_memory["dialogue"][-100:]

         # ---- LONG-TERM MEMORY (FACTS ONLY) ----
        fact = extract_memory(prompt)
        if fact:
            long_term_memory["facts"].append(fact)
            long_term_memory["facts"] = long_term_memory["facts"][-50:]  # cap
        save_memory(long_term_memory)

        # ---- TRIM SHORT-TERM MEMORY ----
        if len(conversation) > (MAX_TURNS * 2 + 1):
            conversation = [conversation[0]] + conversation[-(MAX_TURNS * 2):]

        return reply

    except Exception as e:
        print(f"⚠️ LLM error: {e}")
        return "Sorry, my brain froze for a moment."
    
    finally:
        is_thinking = False

    


# ====================
# SPEAK (PIPER)
# ====================
def speak(text: str):
    global is_speaking
    is_speaking = True

    print(f"🗣️ Friday: {text}")
    output_path = os.path.join(AUDIO_DIR, f"{uuid.uuid4().hex}.wav")

    try:
        process = subprocess.Popen(
            [
                PIPER_EXE,
                "--model", PIPER_MODEL,
                "--output_file", output_path
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )

        process.communicate(text)

        if not os.path.exists(output_path):
            raise RuntimeError("Piper did not produce audio output")

        data, sr = sf.read(output_path, dtype="float32")
        sd.play(data, sr)
        sd.wait()

    except Exception as e:
        print(f"⚠️ Piper TTS failed: {e}")

    is_speaking = False
    time.sleep(0.2)


# ====================
# RECORD COMMAND
# ====================
def record_command() -> str:
    print("🎧 Listening for command...")
    audio = sd.rec(
        int(COMMAND_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    path = os.path.join(AUDIO_DIR, "command.wav")
    sf.write(path, audio, SAMPLE_RATE)
    return path


# ====================
# TRANSCRIBE
# ====================
def transcribe(path: str) -> str:
    segments, _ = whisper.transcribe(path)
    return " ".join(segment.text for segment in segments).strip()


# ====================
# WAKE HANDLER
# ====================
def on_wake_word():
    global last_trigger_time, is_listening_for_command

    if is_listening_for_command or is_speaking:
        return

    now = time.time()
    if now - last_trigger_time < DEBOUNCE_TIME:
        return

    last_trigger_time = now

    is_listening_for_command = True
    speak("I'm listening.")

    audio_path = record_command()
    text = transcribe(audio_path)

    if text:
        print(f"🗣️ You said: {text}")
        reply = ask_llm(text)
        speak(reply)
    else:
        speak("Sorry, I didn't catch that.")

    is_listening_for_command = False

    if text.lower() in ["exit", "shutdown", "go to sleep"]:
        speak("Goodbye.")
        os._exit(0)



# ====================
# AUDIO CALLBACK
# ====================
def audio_callback(indata, frames, time_info, status):
    if is_listening_for_command or is_speaking:
        return

    audio = np.frombuffer(indata, dtype=np.int16)
    predictions = wake_model.predict(audio)

    for score in predictions.values():
        if score > THRESHOLD:
            on_wake_word()
            break


# ====================
# TEXT INPUT THREAD
# ====================
def text_input_loop():
    global TEXT_MODE
    while True:
        user_input = input("💬 You: ").strip()
        if not user_input:
            continue

        # Exit commands
        if user_input.lower() in ["exit", "shutdown", "go to sleep"]:
            speak("Goodbye.")
            os._exit(0)

        # Mode toggle commands
        if user_input.lower() in ["switch to voice mode", "voice mode"]:
            print("🔊 Voice mode remains active.")
            continue
        if user_input.lower() in ["switch to text mode", "text mode"]:
            print("💬 Text mode active.")
            continue

        # Ask LLM and speak
        reply = ask_llm(user_input)
        speak(reply)


# ====================
# START HYBRID SYSTEM
# ====================
if __name__ == "__main__":
    print("🎙️ Friday is ready. You can type commands or say the wake word.")

    decay_emotion()

    # Start text input in a separate thread
    text_thread = threading.Thread(target=text_input_loop, daemon=True)
    text_thread.start()

    # Start voice mode (audio stream)
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=1,
        dtype=np.int16,
        callback=audio_callback
    ):
        try:
            while True:
                # Main thread just sleeps; text + voice run concurrently
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Friday shutting down.")


