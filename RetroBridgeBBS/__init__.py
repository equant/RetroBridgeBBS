import threading
import queue
import RetroBridgeBBS.devices   # telnet, serial, console device interfaces

#['Node 0', RetroBridgeBBS.devices.console,  []],
#['Node 1', RetroBridgeBBS.comms.tty,    ['/dev/ttyUSB0']],
#['Node 2', RetroBridgeBBS.comms.telnet, ['', 51235]],

node_list = [
        { 'name':'Node 0', 'class':RetroBridgeBBS.devices.console, 'args':[] },
        { 'name':'Node 2', 'class':RetroBridgeBBS.devices.telnet, 'args':['', 3030]},
]

class UserSession(object):
    def __init__(self, device_object, device_argument_list):
        self.device_object = device_object
        self.do_login

    def do_login(self):
        username = self.device_object.prompt('Username:')
        print(f"User logged in: {username}")
        self.username = username

class BBS(object):
    """
    This is the main code that dispatches nodes on devices for callers to connect to.
    """

    exit    = False
    devices = []
    queues  = {}

    def __init__(self):
        print("In init")
        self.initialize_nodes(node_list)
        self.queues['console_queue'] = queue.Queue()
        return

    def initialize_nodes(self, node_list):
        print("begin initialize_nodes")
        self.devices = []
        for _idx, _n in enumerate(node_list):
            name = _n['name']
            dev_class = _n['class']
            dev_class_args = _n['args']
            device = dev_class(self, dev_class_args)
            self.devices.append(device)
        print("exit initialize_nodes")
        return

    def log(self, message):
        print(message)
        return

    def initialize_user_session(self, device, arg_list):
        user = UserSession(device, arg_list)
        

