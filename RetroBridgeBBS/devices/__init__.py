import sys, time
import threading
import queue

class base_device(object):
    import serial
    queues = {}
    def __init__(self, bbs, dev_args):
        self.bbs = bbs
        self.dev_args = dev_args    # arguments unique to device class
        self.queues['received'] = queue.Queue()
        self.queues['to_send'] = queue.Queue()
    def debug(self):
        print("self.bbs:")
        print(self.bbs)
    def prompt(self, prompt_string):
        self.clear_receive_queue()
        self.write(prompt_string)
        while (True):
            if (inputQueue.qsize() > 0):
                input_str = inputQueue.get()
                print("input_str = {}".format(input_str))
                time.sleep(0.01) 
    def clear_receive_queue(self):
        garbage = self.queues['received'].get()
    def write(self, message):
        self.queues['to_send'].put(message)
        pass
        


class tty(base_device):
    def __init__(self, bbs, dev_args):
        base_device.__init__(self, bbs, dev_args)


class telnet(base_device):
    def __init__(self, bbs, dev_args):
        base_device.__init__(self, bbs, dev_args)
        import socket

        self.host = self.dev_args[0]
        self.port = self.dev_args[1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(4)
        self.s = s

        connectionThread = threading.Thread(target=self.accept_connections,
                                        #args=(s, nodes),
                                        daemon=True)
        connectionThread.start()


    def accept_connections(self):
        while (True):
            sock, address = self.s.accept()
            sock.send(b'\377\375\042\377\373\001');     # put telnet client in character mode.
            garbage_from_telnet = sock.recv(1024)       # ignore telnet client's response.
            print('%s:%s connected.' % address)
#            telnetThread = threading.Thread(target=self.handle_connection,
#                                            args=(sock, address),
#                                            daemon=True)
#            telnetThread.start()
            receiveThread = threading.Thread(target=self.handle_receive,
                                            args=(sock, address),
                                            daemon=True)
            receiveThread.start()
            sendThread = threading.Thread(target=self.handle_send,
                                            args=(sock, address),
                                            daemon=True)
            sendThread.start()
            user_session = self.bbs.initialize_user_session(self, [sock, address])
            time.sleep(0.1) 


    def handle_receive(self, sock, address):
        while True:
            data = sock.recv(1024)
            if not data:
                break
            #sock.send(data)
            #print(data)
            self.queues['received'].put(data)
            time.sleep(0.1) 
        sock.close()
        print('%s:%s disconnected.' % address)


    def handle_send(self, sock, address):
        while True:
            if (self.queues['to_send'].qsize() > 0):
                message = self.queues['to_send'].get()
                print("message = {}".format(message))
                sock.send(message)
                time.sleep(0.1) 
            sock.close()


class console(base_device):
    """
    This device is not used for use login at the moment.
    """

    def __init__(self, bbs, dev_args):
        base_device.__init__(self, bbs, dev_args)

        self.thread = threading.Thread(target=self.read_console_input,
                                       #args=(inputQueue,),
                                       daemon=True)
        self.thread.start()

    def read_console_input(self):
        print()
        self.debug()
        print()
        print('Ready for keyboard input:')
        while (True):
            input_str = input()
            self.bbs.queues['console_queue'].put(input_str)
            time.sleep(0.01) 


"""
class stdio(base_device):
    def __init__(self):
        pass
"""

