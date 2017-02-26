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
import urllib2
from HTMLParser import HTMLParser
import sys
from twilio.rest import TwilioRestClient
import HTMLReader
import mainFunction
#from google import search

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

greetingArray = ["I am fine, thank you. How about you", "I am doing well. How about you", "Thank you so much for asking, I'm doing well. How about you",
                "I am feeling awesome. How about you"]
helloArray = ["Hi baby, what can I do for you", "What's up", "How can I help you baby", "Hi baby, I'm listening"]
dataTrain = ["zero", "one", "two", "three", "four"]
 

#TO DO: find a way not to hard code \xe2\x80\x9c, maybe using UNICODE




# Main functions: speak, recordAudio and jarvis

 
def jarvis(data):
    if "what's your name" in data or "what is your name" in data:
        mainFunction.speak("My name is Jarvis. Nice to meet you")
    if "how are you" in data:
        num = random.randint(0, len(greetingArray) - 1)
        mainFunction.speak(greetingArray[num])
        data = recordAudio()
        if "good" in data or "fine" in data:
            mainFunction.speak("Nice to hear")
        else:
            mainFunction.speak("Let's chill")
 
    if "tell me something" in data:
        if HTMLReader.arr != []:
           num = random.randint(0, len(HTMLReader.arr)-1)
           mainFunction.speak(HTMLReader.arr[num])
        else:
            parser = HTMLReader.MyHTMLParser()
            response = urllib2.urlopen("http://www.positivityblog.com/index.php/2014/03/19/self-esteem-quotes/") 
            page_source = response.read()
            parser.feed(page_source)
            print "First"
            num = random.randint(0, len(HTMLReader.arr)-1)
            mainFunction.speak(HTMLReader.arr[num])

    if "thank you" in data:
        mainFunction.speak("You're welcome")

    if "what time is it" in data:
        mainFunction.speak("The time is {0}".format(str(ctime())))

    if "who made you" in data:
        mainFunction.speak("Anh Thai")
 
    if "where is" in data:
        data = data.split(" ")
        location = ""
        say = ""
        for i in range(2, len(data)):
            say += " " + data[i]
            location += "+" + data[i]
        mainFunction.speak("Hold on baby, I will show you where " + say + " is.")
        webbrowser.open_new('https://www.google.com/maps/place/{0}'.format(location))
    if "open" in data:
        data = data.split(" ")
        url = data[1]
        mainFunction.speak("Opening " + url)
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
        mainFunction.speak("Here is what I found")
        webbrowser.open_new('https://www.google.com/search?q={0}'.format(name))

    if "friend" in data:
        greetingFriend()
    if "stupid" in data:
        speak("Come on, it's not very nice")
    if "ABC" in data or "hey" in data or "see" in data:
        train()
    if "send message" in data:
        sendMessage()
    #else:
    #    speak("I don't quite understand what you said")


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
        mainFunction.speak(helloArray[num])
    else:
        t = int(ctime().split(" ")[3].split(":")[0])
        if t >= 0  and t <= 11:
            mainFunction.speak("Good morning baby, what can I do for you")
        elif t >= 12 and t <= 18:
            mainFunction.speak("Good afternoon baby, what can I do for you")
        else:
            mainFunction.speak("Good evening baby, what can I do for you")
def greetingFriend():
    speak("Hi, my name is Jarvis. What's your name")
    data = recordAudio()
    data = data.split(" ")
    data = data[-1]
    mainFunction.speak("Hi, {0}, nice to meet you".format(data))

dataTrain = ["zero", "one", "two", "three", "four"]
data = ""
def train():
    file = open('train.txt','r')
    list = []
    for line in file:
        list.append(float(line[0:len(line)-1]))
    #print "List " + str(list)
    index = dummySetUpTrain(list)
    mainFunction.speak(dataTrain[index])
    data = recordAudio()
    if "like" in data:
        list[index] += 1
    elif "don't" in data:
        list[index] -= 1
    file1 = open('train.txt', 'w')
    for i in range(0, len(list)):
        file1.write(str(list[i])+"\n")

def dummySetUpTrain(list):
    myList = [list[i] for i in range(0, len(list))]
    print myList
    for i in range(1, len(myList)):
        myList[i] += myList[i-1]
    print "MyList " + str(myList)
    number = random.randint(0, myList[len(myList)-1])
    print "Number " + str(number)
    if number <= myList[0]:
        return 0
    if number > myList[-1]:
        return -1
    for i in range(1, len(myList)):
        if number <= myList[i] and number > myList[i-1]:
            return i

ACCOUNT_SID = "" 
AUTH_TOKEN = "" 
 
def sendMessage():
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
    client.messages.create(
        to="", 
        from_="", 
        body="Good morning", 
    )
# initialization
time.sleep(2)
greeting()
while 1:
    data = mainFunction.recordAudio()
    #print "First " + str(HTMLReader.arr)
    #data = "tell me something"
    if "bye" in data or "leaving" in data:
        mainFunction.speak("Goodbye")
        break
    jarvis(data)
    #print HTMLReader.arr
    data = ""


