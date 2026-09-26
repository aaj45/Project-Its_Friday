import sounddevice as sd
import soundfile as sf

data, sr = sf.read(r"C:\Users\akifj\jarvis\audio\test.wav", dtype="float32")
sd.play(data, sr)
sd.wait()
