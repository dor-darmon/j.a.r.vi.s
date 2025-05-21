"""
Entry point – starts wake-word loop and dispatches Hebrew commands.
"""

import os
from dotenv import load_dotenv
from assistants.wake_word import WakeWordDetector
from assistants.recognizer import SpeechRecognizer
from assistants.tts import SpeechSynthesizer
from assistants.brain import AssistantBrain
from assistants.dispatcher import ActionDispatcher

def main() -> None:
    load_dotenv()

    wake = WakeWordDetector(
        keyword_path="resources/keywords/computer.ppn",
        access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
    )
    recognizer = SpeechRecognizer("resources/vosk-model-small-he-0.4")
    tts = SpeechSynthesizer()
    brain = AssistantBrain(os.getenv("OPENAI_API_KEY", ""))
    dispatcher = ActionDispatcher(brain, tts)

    wake.start()
    tts.speak("המערכת פועלת. אמור 'computer' כדי להתחיל.")

    try:
        while True:
            wake.wait()              # blocks until key-word
            tts.speak("כן?")
            command = recognizer.listen_once()
            if command:
                print(f"You said: {command}")
                dispatcher.handle(command)
            else:
                tts.speak("לא שמעתי כלום.")
    except KeyboardInterrupt:
        pass
    finally:
        wake.stop()
        recognizer.close()
        tts.speak("להתראות")

if __name__ == "__main__":
    main()
