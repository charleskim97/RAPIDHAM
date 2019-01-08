### The only import you need!
import socket
import requests
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import random


### Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667  # port
### Options (Edit this)
PASS = "oauth:yp1x4xinnywvf3qbz2g2b7pul2j8pq"  # bot password can be found on https://twitchapps.com/tmi/, no need to touch
BOT = "rapidham"  # Bot's name [NO CAPITALS]
CHANNEL = "rapidham"  # Which channel the bot will enter
OWNER = "rapidham"  # Owner's name [NO CAPITALS] <- used for owner only commands




### Functions

def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

def getMessage(line):
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message

def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
    sendMessage(s, "Chat room joined!")
    print("Bot has joined " + CHANNEL + " Channel!")

def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True


### Code runs
s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())
s = s_prep
joinchat()
readbuffer = ""

def Console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True


while True:
        try:
            readbuffer = s.recv(1024)
            readbuffer = readbuffer.decode()
            temp = readbuffer.split("\n")
            readbuffer = readbuffer.encode()
            readbuffer = temp.pop()
        except:
            temp = ""
        for line in temp:
            if line == "":
                break
            # So twitch doesn't timeout the bot.
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                print(msgg)
                break
            # get user
            user = getUser(line)
            # get message send by user
            message = getMessage(line)
            # for you to see the chat from CMD
            print(user + " > " + message)
            # sends private msg to the user (start line)
            PMSG = "/w " + user + " "

################################# Command ##################################
############ Here you can add as many commands as you wish of ! ############
############################################################################

            if user == OWNER and "!command" in message:
                sendMessage(s, "This can only be used by the owner")
                break

            if "!private" in message:
                sendMessage(s, PMSG + "This is a private message send to the user")
                break

            if "!global" in message:
                sendMessage(s, "This is a global message send to the chat")
                break

            
            ## OSMS ranking command
            #!rank Player_Char -> "Player_Char is rank ####!"   
            if "!rank" in message:

                x = "placeholder"
                url = 'https://oldschoolmaple.com/rankings?filter=name&order=level&sort=desc&name='
                messages = message.split()
                failed_search = False

                ##Check valid input
                if len(messages) == 2:
                    url = url + messages[1]
                    print(url) #for visibility in shell


                    #Driver browser does not open a window
                    option = Options()
                    option.headless = True

                    #Navigate to page
                    driver = webdriver.Firefox(options=option) 
                    driver.get(url) 
                    
                    ##Iterate until successful query or 5 loops
                    for i in range(0,5):
                        print("iterate")
                        try:
                            x = driver.find_element_by_class_name('position')
                            rank = str(x.text)
                            
                            driver.quit()
                            nice = True

                            check = ''.join(i for i in rank if i.isdigit())
                            check = int(check)

                            name = messages[1].capitalize()
                            name = str(name)

                            if check >= 1000:
                                sendMessage(s, name + " is rank " + rank + "! AYAYA")
                            elif check > 500:
                                sendMessage(s, name + " is rank " + rank + "! EZ Clap")
                            elif check > 100:
                                sendMessage(s, name + " is rank " + rank + "! POGGERS")
                            else:
                                sendMessage(s, name + " is rank " + rank + "! PartyParrot")
                            rip = False
                            break

                        except NoSuchElementException as exception:
                            time.sleep(1)
                            rip = True  

                else:
                    sendMessage(s, "Invalid number of parameters")

                #If unable to find position tag in HTML
                if rip:
                    driver.quit()
                    sendMessage(s, "Rank search failed. Please try again.")
                else:
                    pass
                break	
                              
            ## Kill the program    
            if "!die" in message:
                sendMessage(s,"See you, space cowboy.")
                sys.exit(0)

############################################################################