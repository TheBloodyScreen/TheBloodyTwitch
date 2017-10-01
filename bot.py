import json
import socket
from time import sleep
from debug import dbprint
from colorama import init, Fore, Back, Style


# Variables & inits
init(autoreset=True)
s = socket.socket()

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


def send(message, do=None):  # Sending messages
    if(do is None):
        construct = "PRIVMSG #" + config["channel"] + " :" + message + "\r\n"
        s.send((construct).encode())
        dbprint("INFO", "BOT: " + message)
        sleep(1.5)
    else:
        construct = "PRIVMSG #" + config["channel"] + " :/me " + message + "\r\n"
        s.send((construct).encode())
        dbprint("INFO", "/me BOT: " + message)
        sleep(1.5)


def afk():  # PONG!
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
            afk()
        elif message[0] != ":tmi.twitch.tv":
            username = message[0][1:int(message[0].index("!"))]
            channel = message[2]
            message[3] = message[3].replace(":", "")
            chatmsg = " ".join(message[3:])

        if chatmsg.startswith("!social"):
            send("You can find me on the following social media sites:")
            send("Player.me: https://player.me/thebloodyscreen")
            send("Twitter: https://twitter.com/thebloodyscreen")
            send("Discord: https://discord.gg/0aps0qFGCyAEe7mF")
        elif chatmsg.startswith("!link"):
            send("You should checkout this wonderful person:")
            send("http://twitch.tv/" + chatmsg[6:])


chat()
