import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel

from engine.command import speak, get_language
from engine.config import ASSISTANT_NAME
import pywhatkit as kit


conn = sqlite3.connect("hansa.db")
cursor = conn.cursor()
#sound function for playing sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

#click sound for mic button

@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)


# Urdu keyword mappings
URDU_OPEN_KEYWORDS = ['کھولو', 'کھول', 'چلاؤ', 'شروع']
URDU_YOUTUBE_KEYWORDS = ['یوٹیوب', 'یوٹیوب پر']

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    # Strip both English and Urdu "open" keywords
    for kw in URDU_OPEN_KEYWORDS:
        query = query.replace(kw, "")
    query = query.replace("open", "").strip().lower()

    if query != "":
        try:
            # Try to find the application in sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()

            if len(results) != 0:
                if get_language() == 'ur':
                    speak(query + " کھول رہی ہوں", lang='ur')
                else:
                    speak("Opening " + query)
                os.startfile(results[0][0])
                return

            # If not found, try to find the URL in web_command table
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()

            if len(results) != 0:
                if get_language() == 'ur':
                    speak(query + " کھول رہی ہوں", lang='ur')
                else:
                    speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            # If still not found, try to open using os.system
            if get_language() == 'ur':
                speak(query + " کھول رہی ہوں", lang='ur')
            else:
                speak("Opening " + query)
            try:
                os.system('start ' + query)
            except Exception as e:
                if get_language() == 'ur':
                    speak(f"{query} کھولنے میں مسئلہ ہوا", lang='ur')
                else:
                    speak(f"Unable to open {query}. Error: {str(e)}")

        except Exception as e:
            if get_language() == 'ur':
                speak("کچھ غلط ہو گیا", lang='ur')
            else:
                speak(f"Something went wrong: {str(e)}")



def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        if get_language() == 'ur':
            speak("یوٹیوب پر " + search_term + " چلا رہی ہوں", lang='ur')
        else:
            speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        if get_language() == 'ur':
            speak("معذرت، یوٹیوب پر کچھ نہیں ملا", lang='ur')
        else:
            speak("Sorry, I couldn't find what to play on YouTube.")


def extract_yt_term(command):
    # English pattern: "play X on youtube"
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return match.group(1)

    # Urdu pattern: "یوٹیوب پر X چلاؤ" or "یوٹیوب پر X"
    urdu_pattern = r'یوٹیوب\s*پر\s+(.*?)(?:\s+چلاؤ|\s+چلائیں|$)'
    match = re.search(urdu_pattern, command)
    if match:
        return match.group(1).strip()

    return None