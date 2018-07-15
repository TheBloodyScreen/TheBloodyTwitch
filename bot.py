import json
import socket
import random
import logging
import requests
import datetime
from time import sleep
from config import config
from bloodyterminal import btext


# Variables & inits
s = socket.socket()
date = datetime.datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename="./logs/" + date + '.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


# Create an IRC connection
def connect():
    s.connect(("irc.twitch.tv", 6667))
    s.send(("PASS " + config['twitch']['authkey'] + "\r\n").encode())
    s.send(("NICK " + config['twitch']['username'] + "\r\n").encode())
    s.send(("JOIN #" + config['twitch']['channel'] + "\r\n").encode())
    return s


# Sending messages
def send(message, me=None):
    if me is None:
        construct = "PRIVMSG #" + config["twitch"]["channel"] + " :" + message + "\r\n"
        s.send(construct.encode())
        btext.info("BOT: " + message)
        sleep(.5)
    else:
        construct = "PRIVMSG #" + config["twitch"]["channel"] + " :/me " + message + "\r\n"
        s.send(construct.encode())
        btext.info("/me BOT: " + message)
        sleep(.5)


# PONG!
def pong():
    construct = "PONG :tmi.twitch.tv\r\n"
    s.send(construct.encode())
    btext.info("PONG!")


def chat(joinMessage="true"):
    con = connect()
    game = 'not set yet'

    if joinMessage is None:
        btext.info("> No join message specified.")
    else:
        btext.info("> Join message: " + joinMessage)
        send("is here and ready to work!", True)

    while True:
        message = con.recv(1024).decode().split(" ")
        username = "twitch"
        chatmsg = "twitch"

        if message[0] == "PING":
            pong()
            btext.info("Pong!")
        elif message[0] != ":tmi.twitch.tv":
            try:
                username = message[0][1:int(message[0].index("!"))]
                message[3] = message[3].replace(":", "")
                chatmsg = " ".join(message[3:])
                logging.info((username + ": " + chatmsg.rstrip()))
            except:
                exit()

        if chatmsg.startswith("!social"):
            send("You can find me on the following social media sites:")
            send("Player.me: https://thebloodyscreen.com/player.me")
            send("Twitter: https://thebloodyscreen.com/twitter")
            send("Discord: https://thebloodyscreen.com/discord")

        elif chatmsg.startswith("!link"):
            send("You should checkout this wonderful person:")
            send("http://twitch.tv/" + chatmsg[6:])

        elif chatmsg.startswith('!timeout'):
            if check_mod(username) is True:
                if chatmsg[1]:
                    send(".timeout " + chatmsg.split(" ")[1] + chatmsg.split(" ")[2])
                else:
                    send("There seems to be something wrong with your command. SYNTAX: !timeout username amount")
            elif check_mod(username) is False:
                send("You do not have access to this command!")

        elif chatmsg.lower().startswith("am i important?"):
            if check_mod(username) is True:
                send("Well you're a mod, I'll let you be the judge!")
            elif check_mod(username) is False:
                send("Every viewer is important!")

        elif chatmsg.startswith('!setgame'):
            game = chatmsg[8:]

        elif chatmsg.startswith('!game'):
            send(game)

        elif chatmsg.startswith('!humble'):
            send('I am lucky enough to call myself a Humble Partner.')
            send('If you want to support me please consider using my humble link for buying games:')
            send('https://www.thebloodyscreen.com/humble')

        elif chatmsg.startswith('!monthly'):
            send('You can always find the current Humble Monthly at:')
            send('https://www.thebloodyscreen.com/monthly')

        elif chatmsg.startswith('!bundle'):
            send('Here you can find the current humble bundle:')
            send(config['twitch']['currentBundle'])

        elif chatmsg.startswith('!test'):
            s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie",
                       "This cool guy my gardener met yesterday", "Superman"]
            p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys",
                       "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies",
                       "Like, these, like, all these people", "Supermen"]
            s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on",
                       "retards", "meows on", "flees from", "tries to automate", "explodes"]
            p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard",
                       "meow on", "flee from", "try to automate", "explode"]
            infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.",
                           "to be able to make toast explode.", "to know more about archeology."]
            while True:
                message = (random.choice(s_nouns) + ' ' + (random.choice(s_verbs) + ' ' + random.choice(s_nouns).lower()) or (random.choice(p_verbs) + ' ' +  random.choice(p_nouns).lower()) + ' ' + random.choice(infinitives))
                send(message)


def check_mod(username):
    if username in json.loads(requests.get("http://tmi.twitch.tv/group/user/thebloodyscreen/chatters").content.decode('utf-8'))['chatters']['moderators']:
        return True
    elif username == "thebloodyscreen":
        return True
    else:
        return False


chat()
