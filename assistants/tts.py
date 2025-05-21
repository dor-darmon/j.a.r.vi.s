"""
Hebrew text-to-speech via pyttsx3.
"""

import pyttsx3

class SpeechSynthesizer:
    def __init__(self, rate: int = 165):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        for v in self.engine.getProperty("voices"):
            if "he" in v.languages or "he_IL" in v.id:
                self.engine.setProperty("voice", v.id)
                break

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
