from gtts import gTTS
import os
import datetime
import smtplib
import sys

computer_name = "Galaxy"


# convert text to audio
def speak(text):
    try:
        tts = gTTS(text=text, lang="en-in")
        tts.save("audio.wav")
        clear_previous_line()
        print(computer_name + ": " + text + "\n")
        os.system("mpg321 -q audio.wav")

    except KeyboardInterrupt:
        exit(0)


def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning, Sir! how may I help you?")
    elif 12 <= hour < 17:
        speak("Good afternoon, Sir! how may I help you?")
    else:
        speak("Good evening, Sir! how may I help you?")
    print()


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('abhijeets.150598@gmail.com', 'dummypassword;')
    server.sendmail('abhijeets.150598@gmail.com', to, content)
    server.close()
    speak("Email sent!")


def clear_previous_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
