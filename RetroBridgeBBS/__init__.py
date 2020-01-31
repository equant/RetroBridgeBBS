import os, pathlib
import pdb
import threading
import queue
import RetroBridgeBBS.device           # telnet, serial, console device interfaces
import RetroBridgeBBS.device.manager   # telnet, serial, console device interfaces
import RetroBridgeBBS.terminal  # ascii, ansi, etc
import RetroBridgeBBS.rooms  # ascii, ansi, etc
import RetroBridgeBBS.rooms.main_menu  # ascii, ansi, etc
import logging
import pdb
#logging.basicConfig(filename='RetroBridgeBBS.log',level=logging.DEBUG)

#['Node 0', RetroBridgeBBS.devices.console,  []],
#['Node 1', RetroBridgeBBS.comms.tty,    ['/dev/ttyUSB0']],
#['Node 2', RetroBridgeBBS.comms.telnet, ['', 51235]],

device_managers_to_start = [
        { 'name':'Node 0', 'class':RetroBridgeBBS.device.manager.ConsoleManager, 'args':[] },
        { 'name':'Node 1', 'class':RetroBridgeBBS.device.manager.SerialManager, 'args':['/dev/ttyUSB0', 57600]},
        { 'name':'Node 2', 'class':RetroBridgeBBS.device.manager.TelnetManager, 'args':['', 3030]},
]

class UserSession(object):

    STATES = {
            'ACCEPTING_CONNECTION' : 0,
            'USER_LOGGED_IN'       : 1,
    }

    def __init__(self, bbs, device_io, device_manager):
        self.state = UserSession.STATES['ACCEPTING_CONNECTION']
        self.bbs = bbs
        self.device_io = device_io
        self.device_manager = device_manager
        self.bbs.register_session(self)

    def accept_connections(self):
        logging.debug(f"Creating Terminal Class: {self.device_io.DEFAULT_TERM_CLASS}")
        self.terminal = self.device_io.DEFAULT_TERM_CLASS(self.bbs, self.device_io, self)
        logging.debug(f"UserSession.do_login()")
        logging.info(f"Waiting for login on {self.device_io}")
        self.terminal.writeln()
        self.terminal.writeln()
        username = self.terminal.string_prompt('Please enter your username')
        logging.info(f"User logged in: {username}")
        self.username = username
        RetroBridgeBBS.rooms.main_menu.MainMenu(self)
        RetroBridgeBBS.rooms.LogOut(self)
        self.device_manager.disconnect_user_session(self)

class BBS(object):
    """
    This is the main code that dispatches ___ on devices for callers to connect to.
    """

    exit    = False
    devices = []
    queues  = {}
    sessions = []

    DOWNLOAD_ARCHIVE_PATH = None
    CONFIG_FILES_PATH     = None

    def __init__(self):
        logging.debug("RetroBridgeBBS.BBS.__init__()")
        self.name = 'RetroBridgeBBS'
        self.config_path = os.path.join(os.path.expanduser("~"), ".RetroBridgeBBS")
        self.archive_downloads_path = os.path.join(self.config_path, 'downloads')
        pathlib.Path(self.config_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.archive_downloads_path).mkdir(parents=True, exist_ok=True)
        self.initialize_device_managers(device_managers_to_start)
        return

    def register_session(self, user_session):
        self.sessions.append(user_session)

    def initialize_device_managers(self, managers_to_start):
        logging.info(f"Launching [{len(managers_to_start)}]device managers...")
        self.device_managers = []
        for _idx, _n in enumerate(managers_to_start):
            _name = _n['name']
            _class = _n['class']
            _args = _n['args']
            logging.info(f"    {_idx}: {_class}")
            thread = threading.Thread(target=_class,
                                           args=(self, _args,),
                                           daemon=True)
            thread.start()
            self.device_managers.append(thread)
        return

    def initialize_user_session(self, device, arg_list):
        user = UserSession(device, arg_list)
