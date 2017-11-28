import json
import socket
import pymysql
import logging
import requests
import datetime
from time import sleep
from debug import dbprint
from colorama import init, Fore, Back, Style


# Variables & inits
init(autoreset=True)
s = socket.socket()
date = datetime.datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename="./logs/" + date + '.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

# Open JSON settings file
with open("settings.json") as data:
    config = json.load(data)


# Create an IRC connection
def connect():
    init()
    s.connect(("irc.twitch.tv", 6667))
    s.send(("PASS " + config["authkey"] + "\r\n").encode())
    s.send(("NICK " + config["username"] + "\r\n").encode())
    s.send(("JOIN #" + config["channel"] + "\r\n").encode())
    return s


# Sending messages
def send(message, me=None):
    if(me is None):
        construct = "PRIVMSG #" + config["channel"] + " :" + message + "\r\n"
        s.send((construct).encode())
        dbprint("INFO", "BOT: " + message)
        sleep(.5)
    else:
        construct = "PRIVMSG #" + config["channel"] + " :/me " + message + "\r\n"
        s.send((construct).encode())
        dbprint("INFO", "/me BOT: " + message)
        sleep(.5)


# PONG!
def Pong():
    construct = "PONG :tmi.twitch.tv\r\n"
    s.send((construct).encode())
    dbprint("INFO", "PONG!")


def chat(joinMessage="True"):
    display = "".encode()
    con = connect()

    if(joinMessage is None):
        print(Fore.BLACK + Back.CYAN + " INFO " + Style.RESET_ALL + "> No join message specified.")
    else:
        print(Fore.BLACK + Back.CYAN + " INFO " + Style.RESET_ALL + "> Join message specified: " + joinMessage)
        send("is here and ready to work!", True)

    while True:
        display = con.recv(1024)
        display = display.decode()
        message = display.split(" ")
        username = "twitch"
        channel = "twitch"
        chatmsg = "twitch"

        if message[0] == "PING":
            Pong()
            dbprint("info", "Pong!")
        elif message[0] != ":tmi.twitch.tv":
            username = message[0][1:int(message[0].index("!"))]
            channel = message[2]
            message[3] = message[3].replace(":", "")
            chatmsg = " ".join(message[3:])
            logging.info((username + ": " + chatmsg.rstrip()))

        if chatmsg.startswith("!social"):
            send("You can find me on the following social media sites:")
            send("Player.me: https://thebloodyscreen.com/player.me")
            send("Twitter: https://thebloodyscreen.com/twitter")
            send("Discord: https://thebloodyscreen.com/discord")

        elif chatmsg.startswith("!link"):
            send("You should checkout this wonderful person:")
            send("http://twitch.tv/" + chatmsg[6:])

        elif chatmsg.startswith('!timeout'):
            chatmsg = chatmsg.split(" ")
            if checkMod(username) is True:
                if chatmsg[1]:
                    send(".timeout " + chatmsg[1] + chatmsg[2])
                else:
                    send("There seems to be something wrong with your command. !timeout username amount")
            elif checkMod(username) is False:
                send("You do not have access to this command!")

        elif chatmsg.lower().startswith("am i important?"):
            if checkMod(username) is True:
                send("Well you're a mod, I'll let you be the judge!")
            elif checkMod(username) is False:
                send("Every viewer is important!")


def checkMod(username):
    data = "http://tmi.twitch.tv/group/user/thebloodyscreen/chatters"
    userdata = json.loads(requests.get(data).content.decode('utf-8'))
    chatters = userdata['chatters']
    if username in chatters['moderators']:
        return True
    elif username == "thebloodyscreen":
        return True
    else:
        return False


chat()
