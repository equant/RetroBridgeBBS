"""
This script is still in the testing phases, and is not intended for prime time.

Useful:
    python -m serial.tools.list_ports -v
"""
import sys
import socket
#import threading
#import queue
import time
import pdb
import logging
logging.basicConfig(filename='RetroBridgeBBS.log',level=logging.DEBUG)


import RetroBridgeBBS

def main():
    while True:
        time.sleep(0.2)

if __name__ == "__main__":

    bbs = RetroBridgeBBS.BBS()
    try:
        main()
    except KeyboardInterrupt:
        pass

    logging.info("Exiting main program.  All Done!")
