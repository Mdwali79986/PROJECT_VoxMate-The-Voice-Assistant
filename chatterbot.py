import pyttsx3
import datetime
import speech_recognition as sr
import os
import ctypes
import pywhatkit  # for advanced YouTube control
import wikipedia
import webbrowser
import pywhatkit as kit
import requests
from bs4 import BeautifulSoup

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 190)  # Speed of speech

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greeting based on time of day
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning")
        speak("Good Morning")
    elif 12 <= hour < 17:
        print("Good Afternoon")
        speak("Good Afternoon")
    else:
        print("Good Evening")
        speak("Good Evening")
    print("Hello! I am VoxMate, your AI assistant.")
    speak("Hello! I am VoxMate, your AI assistant.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            return r.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. Try again.")
            speak("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        return "None"

def get_current_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"The current time is {now}")
    speak(f"The current time is {now}")

def get_weather():
    # Placeholder for weather function
    print("Currently, I can't fetch the weather, but this will be added soon.")
    speak("Currently, I can't fetch the weather, but this will be added soon.")

def youtube_search(query):
    speak("Searching YouTube for your request.")
    pywhatkit.playonyt(query)

def wikipedia_search(query):
    """Search Wikipedia and read out the summary."""
    speak(f"Searching Wikipedia for {query}")
    print(f"Searching Wikipedia for {query}")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        print(results)
    except wikipedia.exceptions.PageError:
        speak("No matching page found on Wikipedia.")

def google_search(query):
    """Search Google and open the results in a browser."""
    speak(f"Searching Google for {query}")
    print(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the Google search results.")
    print("Here are the Google search results.")


def youtube_search(query):
    """Search YouTube and open the results in a browser."""
    speak(f"Searching YouTube for {query}")
    print(f"Searching YouTube for {query}")
    kit.playonyt(query)
    speak("Playing the top YouTube result.")
    print("Playing the top YouTube result.")

def web_search(query, platform="wikipedia"):
    """Perform a web search on the specified platform."""
    if platform == "wikipedia":
        wikipedia_search(query)
    elif platform == "google":
        google_search(query)
    elif platform == "youtube":
        youtube_search(query)
    else:
        speak("Sorry, I can only search on Wikipedia, Google,or YouTube.")

def adjust_volume(level):
    # level: 0 to 100 for the volume level
    volume = int(level)
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0x40000, volume)

def shutdown():
    print("Shutting down the system.")
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

def restart():
    print("Restarting the system.")
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

def check_temperature():
    url = "https://www.timeanddate.com/weather/india/bhubaneswar"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the temperature
        temp_element = soup.find("div", class_="h2")
        temp = temp_element.text.strip() if temp_element else "N/A"

        speak(f"The current temperature in Bhubaneswar is {temp}")
        print(f"The current temperature in Bhubaneswar is {temp}")
    except Exception as e:
        speak("Sorry, I couldn't retrieve the temperature.")
        print("Error:",e)

def menu():
    commands = '''
    Here are the things I can assist you with:
    - Search Wikipedia for information
    - Open web applications: YouTube, Instagram, Google, Twitter, Facebook
    - Tell you the current time
    - Tell you the temperature 
    - Adjust system volume
    - Control YouTube: search and play
    - Control the system: Shutdown, Restart, Logout
    '''
    print(commands)
    speak(commands)

if __name__ == "__main__":
    wishme()
    menu()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        if "google" in query:

            q = query.replace("search google", "").strip()

            google_search(q)

        elif "youtube" in query:

            q = query.replace("search youtube", "").strip()

            youtube_search(q)

        elif "wikipedia" in query:

            q = query.replace("search", "").strip()
            web_search(q)
        elif 'open instagram' in query:
            print("Opening Instagram...")
            speak("Opening Instagram")
            webbrowser.open("instagram.com")
        elif 'open twitter' in query:
            print("Opening Twitter...")
            speak("Opening Twitter")
            webbrowser.open("twitter.com")
        elif 'open facebook' in query:
            print("Opening Facebook...")
            speak("Opening Facebook")
            webbrowser.open("facebook.com")

        elif 'time' in query:
            get_current_time()
        elif "temperature" in query:
            check_temperature()

        elif 'youtube search' in query:
            speak("What would you like to search on YouTube?")
            yt_query = takeCommand()
            youtube_search(yt_query)

        elif 'volume' in query:
            if 'up' in query:
                adjust_volume(80)
                speak("Volume turned up")
            elif 'down' in query:
                adjust_volume(30)
                speak("Volume turned down")

        elif 'shutdown' in query:
            shutdown()
            break
        elif 'restart' in query:
            restart()
            break

        elif 'goodbye' in query or 'quit' in query:
            print("Goodbye! Have a nice day!")
            speak("Goodbye! Have a nice day!")
            break

        else:
            print("I'm sorry, I couldn't understand that or it may not be available yet.")
            speak("I'm sorry, I couldn't understand that or it may not be available yet.")
