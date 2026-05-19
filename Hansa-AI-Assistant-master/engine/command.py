import time
import pyttsx3
import speech_recognition as sr
import eel
from textblob import TextBlob

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

def detect_language(text):
    """Detect language of the input text"""
    try:
        blob = TextBlob(text)
        lang = blob.detect_language()
        return lang
    except:
        return 'en'  # Default to English

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
        # Try English first
        try:
            query = r.recognize_google(audio, language='en')
        except:
            # Try Urdu if English fails
            query = r.recognize_google(audio, language='ur')
        
        print(f'User said: {query}')
        # Detect which language was spoken
        detected_lang = detect_language(query)
        print(f'Detected language: {detected_lang}')
        
        #speak(query)
        time.sleep(2)
        eel.DisplayMessage(query)
        
        

    except Exception as e:
        print(f'Error: {e}')
        return ""
    
    return query.lower()

# text = takeCommand()

# speak(text)
@eel.expose
def allCommands():
    query = takeCommand()
    print(query)

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)

    elif 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print('Not run')


    eel.ShowHood()
