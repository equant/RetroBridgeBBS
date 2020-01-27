import sys
import threading
import RetroBridgeBBS.device
import logging
import time
import pdb

class BaseManager(object):
    """
    Manages all the connections on device
    """
    sessions = []
    THREAD_ACCEPT_CONNECTIONS = False
    AssociatedDeviceIOClass = RetroBridgeBBS.device.BaseDeviceIOClass
    def __init__(self, bbs, dev_args):
        self.bbs = bbs
        self.dev_args = dev_args    # arguments unique to device class
        self.device_configuration(dev_args)

        if self.THREAD_ACCEPT_CONNECTIONS:
            self.thread = threading.Thread(target=self.accept_connections,
                                           #args=(inputQueue,),
                                           daemon=True)
            self.thread.start()
        else:
            self.accept_connections()

    def device_configuration(self, dev_args):
        return

    def accept_connections(self):
        while True:
            if len(self.sessions) == 0:
                logging.debug(f"Creating DeviceIOClass for manager: {self}")
                logging.debug(f"    Creating DeviceIOClass for manager: {self.AssociatedDeviceIOClass}")
                device_io = self.AssociatedDeviceIOClass(self.bbs, self.dev_args)
                user_session = RetroBridgeBBS.UserSession(self.bbs, device_io, self)
                thread = threading.Thread(target=user_session.accept_connections,
                                          #args=(self.bbs, self.device_io, self),
                                          daemon=True)
                thread.start()
                self.sessions.append(user_session)
                #breakpoint()
            time.sleep(0.1)

    def disconnect_user_session(self, user_session):
        self.sessions.remove(user_session)

    """
    def clear_receive_queue(self):
        garbage = self.queues['received'].get()
    def write(self, message):
        self.queues['to_send'].put(message)
    def console_io_thread(self):
        return
    """

class ConsoleManager(BaseManager):
    sessions = []
    THREAD_ACCEPT_CONNECTIONS = False
    AssociatedDeviceIOClass = RetroBridgeBBS.device.ConsoleDeviceIO


class TelnetManager(BaseManager):
    sessions = []
    THREAD_ACCEPT_CONNECTIONS = True
    AssociatedDeviceIOClass = RetroBridgeBBS.device.TelnetDeviceIO

    def device_configuration(self, dev_args):
        logging.debug(f"TelnetManager: device_configuration(): {dev_args}")
        import socket
        #self.host = self.dev_args[0]
        #self.port = self.dev_args[1]
        _host = dev_args[0]
        _port = dev_args[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((_host, _port))
        sock.listen(4)
        self.sock = sock

    def accept_connections(self):
        logging.debug(f"TelnetManager: accept_connections()")
        while (True):
            comm, address = self.sock.accept()
            comm.send(b'\377\375\042\377\373\001');     # put telnet client in character mode.
            garbage_from_telnet = comm.recv(1024)       # ignore telnet client's response.
            logging.info('%s:%s connected.' % address)

            device_io = self.AssociatedDeviceIOClass(self.bbs, self.dev_args, comm)
            user_session = RetroBridgeBBS.UserSession(self.bbs, device_io, self)
            thread = threading.Thread(target=user_session.accept_connections,
                                      #args=(self.bbs, self.device_io, self),
                                      daemon=True)
            thread.start()
            self.sessions.append(comm)
            time.sleep(0.5) 

    def disconnect_user_session(self, user_session):
        self.sessions.user_session.device_io.close()        # TODO: Doesn't work.
        self.sessions.remove(user_session.device_io)

