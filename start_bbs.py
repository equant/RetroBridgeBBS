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

    device_managers_to_start = [
            { 'name':'Node 0', 'class':RetroBridgeBBS.device.manager.ConsoleManager, 'args':[] },
            #{ 'name':'Node 1', 'class':RetroBridgeBBS.device.manager.SerialManager, 'args':['/dev/ttyUSB0', 57600]},
            { 'name':'Node 2', 'class':RetroBridgeBBS.device.manager.TelnetManager, 'args':['', 3030]},
    ]

    config = dict()
    config['name'] = 'RetroBridgeBBS'
    config['device_managers_to_start'] = device_managers_to_start
    config['require_username'] = False
    config['require_password'] = False
    config['default_transfer_protocol'] = 'zmodem'

    bbs = RetroBridgeBBS.BBS(device_managers_to_start, config)
    try:
        main()
    except KeyboardInterrupt:
        pass

    logging.info("Exiting main program.  All Done!")
