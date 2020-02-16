import os, pathlib
import pdb
import logging
import threading
import queue
import RetroBridgeBBS.device           # telnet, serial, console device interfaces
import RetroBridgeBBS.device.manager   # telnet, serial, console device interfaces
import RetroBridgeBBS.terminal  # ascii, ansi, etc
import RetroBridgeBBS.rooms
import RetroBridgeBBS.rooms.main_menu
import RetroBridgeBBS.rooms.file_area_main_menu
import RetroBridgeBBS.rooms.login
#logging.basicConfig(filename='RetroBridgeBBS.log',level=logging.DEBUG)

"""
RetroBridgeBBS/__init__.py
"""

class UserSession(object):

    # I don't think I ever ended up using these STATES.  Probably should check and decide
    # how to clean this up.
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

        # Everything below here should probably by in the BBS class...
        # but I think because of the way I've choosen to do threads it works
        # better here.  Meh.

        if self.bbs.require_username:
            if self.bbs.require_password:
                self.authenticated = False
                while self.authenticated == False:
                    RetroBridgeBBS.rooms.login.Login(self, require_password=True)
                    logging.debug(f'Exited login.  self.authenticated is: {self.authenticated}')
            else:
                RetroBridgeBBS.rooms.login.Login(self, require_password=False)

        #breakpoint()
        #RetroBridgeBBS.rooms.main_menu.MainMenu(self)
        RetroBridgeBBS.rooms.file_area_main_menu.FileAreaMainMenu(self)
        RetroBridgeBBS.rooms.LogOut(self)
        self.device_manager.disconnect_user_session(self)

class BBS(object):
    """
    This is the main code that dispatches ___ on devices for callers to connect to.
    """

    exit     = False
    devices  = []
    queues   = {}
    sessions = []

    DOWNLOAD_ARCHIVE_PATH = None
    CONFIG_FILES_PATH     = None

    def __init__(self, device_managers_to_start, config_dict):
        logging.debug("RetroBridgeBBS.BBS.__init__()")

        self.name = config_dict['name']
        self.device_managers_to_start = config_dict['device_managers_to_start']
        self.require_username = config_dict['require_username']
        self.require_password = config_dict['require_password']
        self.default_transfer_protocol = config_dict['default_transfer_protocol']

        self.config_path = os.path.join(os.path.expanduser("~"), ".RetroBridgeBBS")
        self.archive_downloads_path = os.path.join(self.config_path, 'downloads')
        self.archive_uploads_path = os.path.join(self.config_path, 'uploads')
        pathlib.Path(self.config_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.archive_downloads_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.archive_uploads_path).mkdir(parents=True, exist_ok=True)

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

    #def initialize_user_session(self, device, arg_list):
        #user = UserSession(device, arg_list)
