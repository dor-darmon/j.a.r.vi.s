
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List
import pyaudio
import pyttsx3
import vosk
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from porcupine import Porcupine, PorcupineActivationException

# ---------------------------------------------------------------------
# Speech recognizer (single utterance)
# ---------------------------------------------------------------------
class SpeechRecognizer:
    """Records a sentence in Hebrew and returns its text."""

    def __init__(self, model_path: str):
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.pa = pyaudio.PyAudio()

    def listen_once(self, timeout: float = 8.0) -> str | None:
        """Capture up to *timeout* seconds and transcribe."""
        stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000,
        )
        stream.start_stream()
        start = time.time()
        text = ""
        while time.time() - start < timeout:
            data = stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                res = json.loads(self.recognizer.Result())
                text = res.get("text", "").strip()
                if text:
                    break
        stream.stop_stream()
        stream.close()
        return text or None

    def close(self):
        self.pa.terminate()


# ---------------------------------------------------------------------
# Speech synthesis
# ---------------------------------------------------------------------
class SpeechSynthesizer:
    """Hebrew TTS with pyttsx3."""

    def __init__(self, rate: int = 165):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        # Auto-select Hebrew voice
        for voice in self.engine.getProperty("voices"):
            if "he" in voice.languages or "he_IL" in voice.id:
                self.engine.setProperty("voice", voice.id)
                break

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()