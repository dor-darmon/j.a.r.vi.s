def main():
    load_dotenv()

    vosk_model_path = "vosk-model-small-he-0.4"      # adjust if needed
    keyword_path = str(Path("keywords/computer.ppn"))  # or Hebrew keyword ppn

    wake_detector = WakeWordDetector(keyword_path)
    recognizer = SpeechRecognizer(vosk_model_path)
    tts = SpeechSynthesizer()
    brain = AssistantBrain(os.getenv("OPENAI_API_KEY", ""))
    dispatcher = ActionDispatcher(brain, tts)

    wake_detector.start()
    tts.speak("המערכת פועלת. אמור 'computer' כדי להתחיל.")

    try:
        while True:
            wake_detector.wait()
            tts.speak("כן?")
            sentence = recognizer.listen_once()
            if sentence:
                print(f"You said: {sentence}")
                dispatcher.handle(sentence)
            else:
                tts.speak("לא שמעתי כלום.")
    except KeyboardInterrupt:
        pass
    finally:
        wake_detector.stop()
        recognizer.close()
        tts.speak("להתראות")


if __name__ == "__main__":
    main()