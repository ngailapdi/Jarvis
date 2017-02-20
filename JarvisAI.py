import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound
import webbrowser
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import subprocess
import random
#from google import search

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

tellMeSomethingArray = ["You're the smartest person in the world", "You're doing a great job", "The time is {0}".format(str(ctime())),
                        "You look nice today", "You should be happier because your life is awesome", "I love you"]
greetingArray = ["I am fine, thank you. How about you", "I am doing well. How about you", "Thank you so much for asking, I'm doing well. How about you",
                "I am feeling awesome. How about you"]
helloArray = ["Hi baby, what can I do for you", "What's up", "How can I help you baby", "Hi baby, I'm listening"]
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    playsound('audio.mp3')
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
    try:
        audio = r.listen(source)
    except Error:
        os.system("say 'hi'")
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    if "what's your name" in data:
        speak("My name is Jarvis. Nice to meet you")
    if "how are you" in data:
        num = random.randint(0, len(greetingArray) - 1)
        speak(greetingArray[num])
        data = recordAudio()
        if "good" in data or "fine" in data:
            speak("Nice to hear")
        else:
            speak("Let's chill")
 
    if "tell me something" in data:
        num = random.randint(0, len(tellMeSomethingArray)-1)
        speak(tellMeSomethingArray[num])
    if "thank you" in data:
        speak("You're welcome")

    if "what time is it" in data:
        speak("The time is {0}".format(str(ctime())))

    if "who made you" in data:
        speak("Anh Thai")
 
    if "where is" in data:
        data = data.split(" ")
        location = ""
        say = ""
        for i in range(2, len(data)):
            say += " " + data[i]
            location += "+" + data[i]
        speak("Hold on baby, I will show you where " + say + " is.")
        webbrowser.open_new('https://www.google.com/maps/place/{0}'.format(location))
    if "open" in data:
        data = data.split(" ")
        url = data[1]
        speak("Opening " + url)
        webbrowser.open_new('https://www.{0}.com'.format(url))
        #data = ""
    if "YouTube" in data:
        data = data.split(" ")
        name = data[1]
        for i in range(2, len(data)):
            name += " " + data[i]
        argparser.add_argument("--q", help="Search term", default="{0}".format(name))
        argparser.add_argument("--max-results", help="Max results", default=25)
        args = argparser.parse_args()
        try:
            videos = youtube_search(args)
            videos = videos[0].replace('(',' ').replace(')', ' ').split(" ")
            videos = videos[-2]
            print videos
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
        webbrowser.open_new('https://www.youtube.com/watch?v={0}'.format(videos))
    if "application" in data:
        data = data.split(" ")
        app = data[1]
        subprocess.call(
            ["/usr/bin/open", "-n", "-a", "/Applications/{0}.app".format(app)]
        )
    if "Google" in data:
        data = data.split(" ")
        name = data[1]
        for i in range(2, len(data)):
            name += "+" + data[i]
        speak("Here is what I found")
        webbrowser.open_new('https://www.google.com/search?q={0}'.format(name))


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    print "options: " + str(options)
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

    #print "Videos: " + str(videos), "\n"
    #print "Channels: " + str(channels), "\n"
    #print "Playlists:\n", "\n".join(playlists), "\n"
    return videos
def greeting():
    number = random.randint(0,1)
    if number == 0:
        num = random.randint(0, len(helloArray) - 1)
        speak(helloArray[num])
    else:
        t = ctime().split(" ")[3].split(":")[0]
        if 0 <= t <= 11:
            speak("Good morning baby, what can I do for you")
        elif 12 <= t <= 18:
            speak("Good afternoon baby, what can I do for you")
        else:
            speak("Good evening baby, what can I do for you")
# initialization
time.sleep(2)
greeting()
while 1:
    data = recordAudio()
    if "bye" in data:
        speak("Goodbye")
        break
    jarvis(data)
    data = ""