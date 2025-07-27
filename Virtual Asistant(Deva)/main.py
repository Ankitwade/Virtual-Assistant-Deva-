
# Meet your personal Virtual Assistant!
# Features:
# 1. Plays specific songs: faded, soul survivor, mockingbird, old town road, lonely, smack that
# 2. Opens any app on macOS (say: "open app [name]")
# 3. Opens top 10 most visited Indian websites
# 4. Fetches latest news
# 5. Talks to Gemini AI (specify word limit in prompt)

# Usage Tips:
# - Wait 1–2 seconds before giving commands
# - Use natural language, but follow format for app/AI commands



import speech_recognition as sr #importing library to convert audio to text
import webbrowser #library for acess the web 
import sounddevice as sd # library for recods the sound input
import numpy as np #library to handel sound array 
from gtts import gTTS # library for Text to Speech
import os # library helps to Interact with system file
import scipy.io.wavfile as wav # library for converting an sound array into .wav file supported by speech recognition
import musicLibrary # External library 
import sites
import requests # library to request to perform a specific method
import google.generativeai as genai # library to use gemini ai
import re # library to handel the texts  
import subprocess # library for excessing external element
import platform # library for excessing external element


#setup of API key, confugring and starting the chat of gemini
GOOGLE_API_KEY="<your API key>"
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = gemini_model.start_chat(history=[])
except KeyError as e:
    print(f"Error: Environment variable for API key not set: {e}")
    print("Please set your GOOGLE_API_KEY  environment variables.")
    print("You can get a free Gemini API key from https://aistudio.google.com/app/apikey")
    exit() 


#functin for speaking
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("afplay output.mp3")



#function for recoding the audio
def record_audio(duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio, fs



#function for converting the audio to text
def save_wav(filename, data, fs):
    wav.write(filename, fs, data)




newsapi="<your API here>"
#function for the various inputs we will give it to perform
def processcommand(c):
    if "open" in c.lower():
        if("app" in c.lower()):
            app_name=c.lower().split(" ")[2]
            print(app_name)
            os_name=platform.system()
            if os_name == "Darwin":  
                subprocess.run(["open", f"/Applications/{app_name}.app"])
            else:
                speak("not available")
            
        else:
            site=c.lower().split(" ")[1]
        link=sites.web.get(site)
        webbrowser.open(link)
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1:]
        songs=" ".join(song)
        link=musicLibrary.music.get(songs)
        webbrowser.open(link)
    elif "news" in c.lower():
        r= requests.get("https://newsapi.org/v2/everything?q=bitcoin&apiKey=b507843205444fb0ad27f99143c1f684")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            # Create list of news summaries
            news_list = []

            for article in articles[:5]:  # Get first 5 articles
                title = article.get("title", "No Title")
                description = article.get("description", "No Description")
                summary = f"Title: {title}. Description: {description}"
                news_list.append(summary)
            # Speak each article
            for i, news in enumerate(news_list, start=1):
                speak(f"News {i}: {news}")
    else:
        speak("Let me think...")
        try:
            gemini_response = chat_session.send_message(c)
            speak(re.sub(r'[^\w\s]', '', gemini_response.text).lower())
        except Exception as e:
            speak(f"I encountered an issue while processing your request with Gemini: {e}")
            speak("Please try again.")




#main function where the action is done
if __name__ == "__main__":
    #Starting statement which help us know about working
    speak("Initializing Deva...")
    while True:
        try:
            #definign the duration and recoging audio
            duration = 5 
            audio_data, sample_rate = record_audio(duration)

            # Save temporary WAV file
            filename = "temp.wav"
            save_wav(filename, audio_data, sample_rate)

            # Recognize using speech_recognition from WAV
            r = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio = r.record(source)
            text = r.recognize_google(audio)
            

            #code for interacting with user 
            if(text.lower()=="hey deva"):
                speak("Yess Boss")
                print("Deva is active")
                duration = 5  
                audio_data, sample_rate = record_audio(duration)
                filename = "temp.wav"
                save_wav(filename, audio_data, sample_rate)

                with sr.AudioFile(filename) as source:
                    command_audio = r.record(source)
                    command_text = r.recognize_google(command_audio)
                processcommand(command_text)
                print(command_text)
            elif "stop" in text.lower():
                speak("Okayy, Turning off")
                break
            else:
                os.remove("output.mp3")
                os.remove("temp.wav")
                speak("Can't recognize you")
        except Exception as e:
            speak("Waiting..")

