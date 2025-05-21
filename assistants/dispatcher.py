"""
Simple Hebrew intent router.
"""

from utils.search import WebSearcher
from utils.music import MusicPlayer
from assistants.brain import AssistantBrain
from assistants.tts import SpeechSynthesizer

class ActionDispatcher:
    def __init__(self, brain: AssistantBrain, tts: SpeechSynthesizer):
        self.brain = brain
        self.tts = tts
        self.searcher = WebSearcher()
        self.player = MusicPlayer()

    def handle(self, text: str) -> None:
        low = text.lower()
        if low.startswith("חפש"):
            query = text.split(" ", 1)[1]
            results = self.searcher.search(query)
            self.tts.speak("הנה התוצאות שמצאתי:")
            print("\n".join(results))
        elif low.startswith("נגן"):
            track = text.split(" ", 1)[1]
            if self.player.play(track):
                self.tts.speak("מנגן כעת")
            else:
                self.tts.speak("לא מצאתי שיר מתאים.")
        else:
            answer = self.brain.chat(text)
            self.tts.speak(answer)
            print(answer)
