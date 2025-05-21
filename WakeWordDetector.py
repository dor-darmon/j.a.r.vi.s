from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import List
import pyaudio
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from porcupine import Porcupine, PorcupineActivationException


# ---------------------------------------------------------------------
# Wake-word detector
# ---------------------------------------------------------------------
class WakeWordDetector(threading.Thread):
    """Runs Porcupine in a background thread and fires when the keyword is spoken."""

    def __init__(self, keyword_path: str, library_path: str | None = None):
        super().__init__(daemon=True)
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if not access_key:
            raise RuntimeError("Missing PORCUPINE_ACCESS_KEY environment variable")

        try:
            self.porcupine = Porcupine(
                access_key=access_key,
                keyword_paths=[keyword_path],
                library_path=library_path,
            )
        except PorcupineActivationException as exc:
            raise RuntimeError("Invalid Picovoice access key") from exc

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )
        self._flag = threading.Event()
        self._stop = threading.Event()

    def run(self):
        while not self._stop.is_set():
            pcm = self.stream.read(
                self.porcupine.frame_length, exception_on_overflow=False
            )
            pcm_buffer = memoryview(pcm).cast("h")
            if self.porcupine.process(pcm_buffer) >= 0:
                self._flag.set()
        self.stream.close()
        self.pa.terminate()

    def wait(self):
        """Block until the wake-word is detected."""
        self._flag.wait()
        self._flag.clear()

    def stop(self):
        self._stop.set()

