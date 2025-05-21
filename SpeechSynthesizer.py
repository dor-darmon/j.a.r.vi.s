from __future__ import annotations

import json
import os
import queue
import threading
import time
import webbrowser
from pathlib import Path
from typing import List

import openai
import pyaudio
import pyttsx3
import vosk
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from porcupine import Porcupine, PorcupineActivationException
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