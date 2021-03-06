import sys, time, pdb
import threading
import queue
import serial
import logging
import RetroBridgeBBS.terminal
        

class BaseDeviceIOClass(object):
    transfer_data_as_bytes = True
    queues = {}
    DEFAULT_TERM_CLASS = RetroBridgeBBS.terminal.BaseTerminal
    DOWNLOAD_CAPABLE = True
    def __init__(self, bbs, dev_args, comm=None):
        self.bbs = bbs
        self.dev_args = dev_args    # arguments unique to device class
        if comm is None:
            self.comm = None
        else:
            self.comm = comm

    def write(self, data):
        if self.transfer_data_as_bytes:
            print(data.encode(), end='', flush=True)
        else:
            print(data, end='', flush=True)

    def read(self):
        input_character = input()
        if type(input_character) == bytes:
            logging.debug(f"DeviceIO(): input_character is bytes")
            return input_character.decode()
        else:
            logging.debug(f"DeviceIO(): input_character is not bytes")
            return input_character


class SerialDeviceIO(BaseDeviceIOClass):
    transfer_data_as_bytes = False

    DOWNLOAD_CAPABLE = True
    DEFAULT_TERM_CLASS = RetroBridgeBBS.terminal.BaseTerminal
    #def __init__(self, bbs, dev_args, comm):
        #BaseDeviceIOClass.__init__(self, bbs, dev_args)
        #self.comm = comm
        #self.dev_args = dev_args
        #return

    def write(self, data):
        self.comm.write(data.encode())
        return

    def read(self):
        data = self.comm.read()
        return data.decode()


class TelnetDeviceIO(BaseDeviceIOClass):
    transfer_data_as_bytes = False

    DEFAULT_TERM_CLASS = RetroBridgeBBS.terminal.BaseTerminal
    #def __init__(self, bbs, dev_args, sock):
        #BaseDeviceIOClass.__init__(self, bbs, dev_args)
        ##DEFAULT_TERM_CLASS = RetroBridgeBBS.terminal.BaseTerminal
        #self.sock = sock
        #self.dev_args = dev_args
        #return

    def write(self, data):
        self.comm.send(data.encode())
        return

    def read(self):
        data = self.comm.recv(1024)
        return data.decode()


class ConsoleDeviceIO(BaseDeviceIOClass):
    transfer_data_as_bytes = False

    DEFAULT_TERM_CLASS = RetroBridgeBBS.terminal.ConsoleTerminal
    #def __init__(self, bbs, dev_args):
        #BaseDeviceIOClass.__init__(self, bbs, dev_args)
        #return
