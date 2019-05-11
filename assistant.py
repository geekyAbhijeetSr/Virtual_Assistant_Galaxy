import speech_recognition as sr
import webbrowser
import wikipedia
import Snowboy.snowboydecoder as snowboydecoder
import time
from other_funtions import *
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from ctypes import *
from contextlib import contextmanager
import pyaudio

# ======================= for handling alsa errors =============================

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


with noalsaerr():
    p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

#================================================================================

chatbot = ChatBot("Galaxy")

chk = 1
chrome_path = "/usr/bin/google-chrome"
computer_name = "Galaxy"
open_list = ["youtube", "you tube", "google", "stackoverflow", "stack overflow", "github", "git hub", "chrome",
             "browser"]
count = 0


# callback function after detecting the hot word or trigger word
def detected_callback():
    global chk
    chk = 1
    if chk:
        while chk:
            q = my_command(check=0)
            if q:
                assistant(str(q))
            else:
                pass


def my_command(check=0):
    query = ""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            clear_previous_line()
            print("Microphone calibrating...")
            r.energy_threshold = 4000
            clear_previous_line()
            print("Listening...")
            audio = r.listen(source)
    except KeyboardInterrupt:
        exit(0)

    try:
        clear_previous_line()
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        clear_previous_line()
        print("You: " + query)
    except sr.UnknownValueError:
        global count, chk
        count += 1
        if count == 4:
            os.system("rm audio.wav")
            chk = 0
            count = 0
        elif check:
            query = my_command(check=1)
        else:
            return 0
    except sr.RequestError:
        pass
    except KeyboardInterrupt:
        exit(0)

    return query.lower()


def open_(query):
    if "youtube" in query or "you tube" in query:
        url = "https://www.youtube.com/"
        speak("Opening YouTube...")
        webbrowser.get(chrome_path).open(url)

    elif "google" in query:
        url = "https://www.google.com/"
        speak("Opening Google...")
        webbrowser.get(chrome_path).open(url)

    elif "stackoverflow" in query or "stack overflow" in query:
        url = "https://stackoverflow.com/"
        speak("Opening Stackoverflow...")
        webbrowser.get(chrome_path).open(url)

    elif "github" in query or "git hub" in query:
        url = "https://github.com/"
        speak("Opening Github...")
        webbrowser.get(chrome_path).open(url)

    elif "chrome" in query or "browser" in query:
        speak("Opening Chrome...")
        os.system("google-chrome &> /dev/null &")


def assistant(query):
    print("Thinking...")

    if "open" in query:
        open_(query)

    elif query in open_list:
        open_(query)

    elif "train yourself" in query:
        speak("Training start")
        trainer = ListTrainer(chatbot)
        trainer.train(open("data.txt", "r").readlines())

        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train('chatterbot.corpus.english')
        speak("Training completed")

    elif "send email" in query:
        speak("Who is the recipient?")
        recipient = my_command()

        if "abhijeet" in recipient:
            speak("What should i say?")
            content = my_command()
            send_email("blacktorpedo121@gmail.com", content)

    elif "drop storage" in query:
        speak("Storage dropping")
        chatbot.storage.drop()

    elif "stop listening" in query or "take rest" in query:
        global chk
        chk = 0
        speak("Ok Sir!")

    elif "google search" in query:
        speak("Google search activated, what do you want to search?")
        ans = my_command()
        url = "https://www.google.com/search?q=" + str(ans)
        speak("Searching on google...")
        webbrowser.get(chrome_path).open(url)

    elif "update" in query:
        speak("Starting system update...")
        os.system("update")
        speak("System update completed.")

    elif "time" in query:
        hr = time.localtime()[3]
        min = time.localtime()[4]
        if hr > 12:
            hr = hr - 12
            ampm = "PM"
        else:
            ampm = "AM"
        speak("The current time is " + str("{:02d}".format(hr)) + ":" + str("{:02d}".format(min)) + " " + ampm)

    elif "power off" in query or "shut down" in query or "shutdown" in query or "poweroff" in query:
        speak("Shutting down...")
        time.sleep(3)
        os.system("poweroff")

    elif "play music" in query or "song" in query or "music" in query:
        speak("Playing music...")
        os.system("vlc --random ~/Music/*.mp3 &> /dev/null &")

    elif query:
        response = chatbot.get_response(query)
        if response.confidence > 0.5:
            speak(str(response))
        else:
            try:
                results = str(wikipedia.summary(query, sentences=2))
                speak(results)
                print()
                speak("Are you satisfied with my answer?")
                ans = my_command(check=True)
                if "no" in ans or "not satisfied" in ans:
                    url = "https://www.google.com/search?q=" + str(query)
                    speak("Searching on google '" + query + "'")
                    webbrowser.get(chrome_path).open(url)
                elif "yes" in ans or "yeah" in ans or "ya" in ans or "satisfied" in ans:
                    pass
                else:
                    pass

            except KeyboardInterrupt:
                pass
            except Exception:
                url = "https://www.google.com/search?q=" + str(query)
                speak("Searching on google '" + query + "'")
                webbrowser.get(chrome_path).open(url)


if __name__ == "__main__":
    print("Initializing assistant...")
    greet()
    detected_callback()
    try:
        detector = snowboydecoder.HotwordDetector("Hey_Galaxy.pmdl", sensitivity=0.5, audio_gain=1)
        detector.start(detected_callback)
    except KeyboardInterrupt:
        exit(0)
