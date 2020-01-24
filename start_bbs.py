import sys
import socket
import threading
import queue
import time
import pdb


#sys.path.append('Rooms/')
#import Room
#import MainMenu
#import Login

import RetroBridgeBBS

"""
This script is still in the testing phases, and is not intended for prime time.

Useful:
    python -m serial.tools.list_ports -v
"""
def main():
    """

    HOST = ''
    PORT = 51235 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(4)
    nodes = Nodes()
    telnetThread = threading.Thread(target=telnet_handshake,
                                   args=(s, nodes),
                                   daemon=True)
    telnetThread.start()

    while (True):
        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get()
            print("input_str = {}".format(input_str))

            if (input_str == EXIT_COMMAND):
                print("Exiting serial terminal.")
                break

            # Insert your code here to do whatever you want with the input_str.
        # The rest of your program goes here.

        time.sleep(0.001) 
    """

if __name__ == "__main__":

    EXIT_COMMAND = 'Q'
    bbs = RetroBridgeBBS.BBS()
    try:
        while bbs.exit == False:
            if (bbs.queues['console_queue'].qsize() > 0):
                console_string = bbs.queues['console_queue'].get()
                print("console_string = {}".format(console_string))

                if (console_string.find(EXIT_COMMAND) >= 0):
                    print("Exiting serial terminal.")
                    break
            time.sleep(0.001) 
    except KeyboardInterrupt:
        pass
    print("The end.")

# DEVICE = '/dev/ttyUSB0'
# #DEVICE = '/dev/ttyS0'
# BAUD = 57600 
# 
# ser = serial.Serial(DEVICE, baudrate=BAUD, timeout=900)
# print(ser.name) # check which port was really used
# 
# import terminal
# term = terminal.BaseTerminal(ser)
# term.text_normal()
# 
# class Session(object):
#     def __init__(self):
#         pass
# session = Session()
# session.username = 'Guest'
# session.term = term
# 
# # LOGIN
# #Login.Login(session)
# 
# # MAIN MENU
# main_menu = MainMenu.MainMenu(session)
# 
# # LOGOUT
# term.newline()
# term.writeln(f"Goodbye {session.username}!")
# term.newline()
# ser.close()


