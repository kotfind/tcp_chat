import curses
import socket
import threading
import requests
from time import sleep
import os

# init curses
stdscr = curses.initscr()
stdscr.clear()
#stdscr.addstr(str(stdscr.getmaxyx()[1]).encode("utf-8"));
#stdscr.refresh()
#sleep(1);
#inputscr = stdscr.subwin(stdscr.getmaxyx()[1] - 8, 1)
inputscr = stdscr.subwin(24, 1)

# init socket
sock = socket.socket()
host, port = requests.get("http://kotfind.oquendo.ru").text.split(":")
port = int(port)
sock.connect((host, port))

# listen for messages
def listen_messages():
    while 1:
        stdscr.addstr(sock.recv(1024).decode("utf-8") + '\n')
        stdscr.refresh()
listen_messages_thread = threading.Thread(target=listen_messages)
listen_messages_thread.start()

# main loop
while 1:
    sock.send(inputscr.getstr())
    inputscr.clear()
    inputscr.refresh()

# exit
def quit():
    sock.close()
    curses.endwin()
    exit();
    os.abort()

quit()
