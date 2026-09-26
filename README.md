# 🎙️ It's Friday

A local AI voice assistant inspired by JARVIS and Friday from the Marvel universe.

Friday combines:

- 🧠 Local LLM powered by Ollama
- 🎤 Speech-to-Text transcription
- 🔊 Text-to-Speech responses
- 🎧 Wake-word detection
- 💾 Persistent memory
- 😊 Emotion tracking
- ⌨️ Text and Voice interaction modes

Everything runs locally on your machine for privacy and customization.

---

# Features

### 🎧 Wake Word Activation
Activate Friday using a custom wake word and interact naturally through your microphone.

### 💬 Chat Mode
Type directly into the console and receive responses instantly.

### 🧠 Local AI
Powered by Ollama and Llama 3.

No cloud API keys required.

### 💾 Persistent Memory
Friday remembers:

- Previous conversations
- User facts
- Preferences

Memory is stored in:

```text
fridays_memory.json
```

### 😊 Emotion Engine
Tracks conversational sentiment and user interactions.

### 🔊 Voice Responses
Friday speaks responses using Text-to-Speech.

---

# Project Structure

```text
Project-Its_Friday/
│
├── Its-Friday.py
│
├── ai/
│   └── llm.py
│
├── audio/
│   ├── recorder.py
│   ├── transcriber.py
│   ├── tts.py
│   └── wake_word.py
│
├── core/
│   ├── assistant.py
│   ├── emotion.py
│   └── memory.py
│
├── utils/
│   └── thinking.py
│
├── fridays_memory.json
├── requirements.txt
└── README.md
```

---

# Requirements

- Python 3.10+
- Ollama
- Llama 3

Install Ollama:

https://ollama.com

Pull the model:

```bash
ollama pull llama3
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/aaj45/Project-Its_Friday.git
```

Navigate to the project:

```bash
cd Project-Its_Friday
```

Create a virtual environment:

```bash
python -m venv jarvis-env
```

Activate it:

### Windows

```bash
jarvis-env\Scripts\activate
```

### Linux / macOS

```bash
source jarvis-env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running Friday

Start Ollama:

```bash
ollama serve
```

Run the assistant:

```bash
python Its-Friday.py
```

Expected output:

```text
🎙️ Friday is ready.
🎧 Wake word listener started...
💬 You:
```

---

# Memory System

Friday stores:

```json
{
  "facts": [],
  "dialogue": []
}
```

Examples of remembered facts:

```text
My name is Akif.
My favourite colour is blue.
I live in Sandbach.
```

These facts are automatically loaded on startup.

---

# Shutdown Commands

Friday can be stopped using:

```text
exit
shutdown
goodbye
good bye
go to sleep
```

These commands work in both Voice Mode and Text Mode.

---

# Future Improvements

- Web search integration
- Calendar management
- Email integration
- Home automation
- Vision support
- Face recognition
- Long-term vector memory
- Multi-agent architecture

---

# Contributing

Contributions, suggestions, and pull requests are welcome.

If you find a bug or have an idea for a new feature, please open an issue.

---

# Author

**Akif Jawad**

Built as a personal AI assistant project inspired by JARVIS and Friday.

---

# License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute it.
