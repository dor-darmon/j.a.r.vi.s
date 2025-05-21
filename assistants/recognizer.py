"""
Single-utterance Hebrew speech recognizer using Vosk.
"""

import json
import time
import pyaudio
import vosk

class SpeechRecognizer:
    def __init__(self, model_path: str):
        self.model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.pa = pyaudio.PyAudio()

    def listen_once(self, timeout: float = 8.0) -> str | None:
        stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000,
        )
        start = time.time()
        text = ""
        while time.time() - start < timeout:
            data = stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                res = json.loads(self.rec.Result())
                text = res.get("text", "").strip()
                if text:
                    break
        stream.close()
        return text or None

    def close(self) -> None:
        self.pa.terminate()
