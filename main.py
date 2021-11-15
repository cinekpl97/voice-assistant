import time
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
from gtts import gTTS
import os

from pvrecorder import PvRecorder
from pygame import mixer
from mutagen.mp3 import MP3
import urllib.request
import urllib.parse
import re
import webbrowser as wb
import subprocess
import pyautogui
import pvporcupine


def duration_detector(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds

    return hours, mins, seconds


def talk():
    input = sr.Recognizer()
    with sr.Microphone() as source:
        audio = input.listen(source)
        data = ""
        try:
            data = input.recognize_google(audio)
            print("You said: " + data)

        except sr.UnknownValueError:
            print("Sorry I did not hear your question, Please repeat again.")
    return data


count = 0


def respond(output):
    global count
    tts = gTTS(text=output, lang='en')
    tts.save(f'speech{count % 2}.mp3')
    mixer.init()
    mixer.music.load(f'speech{count % 2}.mp3')
    mixer.music.play()
    audio = MP3(f'speech{count % 2}.mp3')
    time.sleep(audio.info.length)
    count += 1


def get_next_audio_frame():
    pass


if __name__ == '__main__':
    respond("Hi, I am your very own personal desktop assistant, how can I help you sweetheart?")
    num = 0
    handler = pvporcupine.create(keywords=['porcupine', 'terminator', 'computer'], sensitivities=[0.6, 0.6, 0.6])
    # print(pvporcupine.KEYWORDS)
    recorder = PvRecorder(device_index=1, frame_length=handler.frame_length)

    while True:
        result = -1
        recorder.start()
        while result < 0:
            pcm = recorder.read()
            result = handler.process(pcm)
            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.time), result))
                recorder.stop()

        respond("Yes?")

        num += 1
        text = talk().lower()
        print(text)
        if text == 0:
            continue

        elif "goodbye" in str(text) or "exit" in str(text) or "bye" in str(text):
            respond("Ok bye and take care")
            break

        elif 'wikipedia' in text:
            respond('Searching Wikipedia')
            text = text.replace("wikipedia", "")
            results = wikipedia.summary(text, sentences=3)
            respond("According to Wikipedia")
            respond(results)

        elif 'time' in text:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            respond(f"the time is {strTime}")

        elif 'search' in text:
            text = text.replace("search", "")
            webbrowser.open_new_tab(text)
            time.sleep(5)

        # elif "calculate" or "what is" in text:
        #     question = talk()
        #     app_id = "Mention your API Key"
        #     client = wolframalpha.Client(app_id)
        #     res = client.query(question)
        #     answer = next(res.results).text
        #     respond("The answer is " + answer)

        elif 'open google' in text:
            webbrowser.open_new_tab("https://www.google.com")
            respond("Google is open")
            time.sleep(5)

        elif 'youtube' in text:
            indx = text.split().index('youtube')
            query = text.split()[indx + 1:]
            respond(f"Opening in YouTube and trying to search for {query}")
            query_string = urllib.parse.urlencode({"search_query": query})
            html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?" + query_string)
            search_results = re.findall(r'url\":\"/watch\?v=(.*?(?=\"))', html_content.read().decode())
            if search_results:
                print("http://www.youtube.com/watch?v=" + search_results[0])
                wb.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))

        elif 'open word' in text:
            respond("Opening Microsoft Word")
            os.startfile('Mention location of Word in your system')

        elif 'spotify' in text:
            respond("Opening Spotify")
            subprocess.call(['C:\\Users\\Cinek\\AppData\\Roaming\\Spotify\\Spotify.exe'])

        elif 'music' in text:
            if 'play' or 'pause' or 'stop' in text:
                pyautogui.press("playpause")

        elif 'next' in text:
            pyautogui.press("nexttrack")

        elif 'previous' in text:
            pyautogui.press("prevtrack")
            pyautogui.press("prevtrack")

        elif 'volume' in text:
            if 'up' in text:
                pyautogui.press("volumeup")

            if 'down' in text:
                pyautogui.press("volumedown")

            if 'mute' in text:
                pyautogui.press("volumemute")

        elif 'tab' in text:
            pyautogui.keyDown('ctrl')
            pyautogui.press('w')
            pyautogui.keyUp('ctrl')
        else:
            print("Application not available")
            # respond("Application not available")
