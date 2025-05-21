"""
Wake-Word detection using Porcupine.
"""

import threading
import pyaudio
from porcupine import Porcupine, PorcupineActivationException

class WakeWordDetector(threading.Thread):
    def __init__(self, keyword_path: str, access_key: str):
        super().__init__(daemon=True)
        if not access_key:
            raise RuntimeError("Missing Picovoice access key")

        try:
            self.porcupine = Porcupine(
                access_key=access_key, keyword_paths=[keyword_path]
            )
        except PorcupineActivationException as e:
            raise RuntimeError("Invalid Picovoice access key") from e

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

    def run(self) -> None:
        while not self._stop.is_set():
            pcm = self.stream.read(
                self.porcupine.frame_length, exception_on_overflow=False
            )
            if self.porcupine.process(memoryview(pcm).cast("h")) >= 0:
                self._flag.set()

    def wait(self) -> None:
        self._flag.wait()
        self._flag.clear()

    def stop(self) -> None:
        self._stop.set()
        self.stream.close()
        self.pa.terminate()
