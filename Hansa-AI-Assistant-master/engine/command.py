import time
import pyttsx3
import speech_recognition as sr
import eel
from engine.config import ASSISTANT_NAME, DEFAULT_LANGUAGE

_current_language = DEFAULT_LANGUAGE

def set_language(lang):
    global _current_language
    if lang in ('en', 'ur'):
        _current_language = lang

def get_language():
    return _current_language

def speak(text, lang=None):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    speak_lang = lang or _current_language

    urdu_voice = None
    for voice in voices:
        if 'ur' in voice.id.lower() or 'urdu' in voice.name.lower():
            urdu_voice = voice
            break

    if speak_lang == 'ur' and urdu_voice:
        engine.setProperty('voice', urdu_voice.id)
    else:
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')

        # Try Urdu first, fall back to English
        try:
            query = r.recognize_google(audio, language='ur-PK')
            if query.strip():
                set_language('ur')
                print(f'User said (Urdu): {query}')
                time.sleep(2)
                eel.DisplayMessage(query)
                return query.lower()
        except sr.UnknownValueError:
            pass

        # Fall back to English
        query = r.recognize_google(audio, language='en-US')
        set_language('en')
        print(f'User said (English): {query}')
        time.sleep(2)
        eel.DisplayMessage(query)

    except Exception as e:
        return ""

    return query.lower()

# text = takeCommand()

# speak(text)
@eel.expose
def allCommands():
    query = takeCommand()
    print(query)

    if 'open' in query or 'کھولو' in query:
        from engine.features import openCommand
        openCommand(query)

    elif 'on youtube' in query or 'یوٹیوب' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print('Not run')


    eel.ShowHood()