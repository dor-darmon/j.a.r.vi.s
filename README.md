# j.a.r.vi.s

Jarvis Personal Voice Assistant – Hebrew Edition
================================================

Features
--------
1. Wake-word detection (Porcupine, default keyword: "computer").
2. Hebrew speech recognition via Vosk (`vosk-model-small-he-0.4`).
3. Hebrew speech synthesis (`pyttsx3`, selects a Hebrew voice if available).
4. Music playback without Spotify – opens the first YouTube result.
5. Web search using DuckDuckGo.
6. ChatGPT integration – replies in Hebrew.

Install
-------
pip install vosk pyaudio porcupine-openai pyttsx3 duckduckgo-search python-dotenv openai

* Download a Vosk Hebrew model and extract to `vosk-model-small-he-0.4`.
* Get a free Picovoice access key and download a keyword file (computer.ppn).

Environment variables (in .env or OS):
OPENAI_API_KEY=sk-...
PORCUPINE_ACCESS_KEY=picovoice_access_key