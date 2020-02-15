import types
import inspect
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu as menu
import logging

"""
RetroBridgeBBS/rooms/__init__.py
"""

class Room(object):

    def __init__(self,user_session):
        self.terminal     = user_session.terminal
        self.user_session = user_session
        self.bbs          = user_session.bbs
        DOWNLOAD_CAPABLE  = user_session.device_io.DOWNLOAD_CAPABLE
        self.run_room()
        return

    def do_menu(self, m=None, menu_list=None, title=None, menu_type=None):
        if title is None:
            title = self.bbs.name
        if menu_list is None:
            menu_list = self.menu_list
        if m is None:
            m = menu.Menu(self.user_session, menu_list, title=title, menu_type=menu_type)

        command = None
        while True:
            command_dict = m.handle_menu()
            logging.debug(f"Got command_dict from m.handle_menu()...")
            logging.debug(command_dict)
            if command_dict['valid']:
                command = command_dict['command']
                logging.debug("do_menu() COMMAND is valid")
                logging.debug(f"do_menu() COMMAND is: {command}")
                if command is None:
                    pass
                elif type(command) == str:
                    #logging.debug("do_menu() COMMAND is str()")
                    #if command in ('exit', 'Exit', 'back', 'Back', 'quit', 'Quit'):
                    should_break = self.do_string_command(command)
                    if should_break:
                        break
                #elif isinstance(command, types.FunctionType):
                elif inspect.ismethod(command):
                    logging.debug("do_menu() COMMAND is function")
                    logging.debug(f"About to use command: [{command}]")
                    if 'args' in command_dict.keys():
                        command(**command_dict['args'])
                    else:
                        command()
                elif issubclass(command, Room):
                    logging.debug("do_menu() COMMAND is subclass of Room")
                    if 'args' in command_dict.keys():
                        command(self.user_session, **command_dict['args'])
                    else:
                        command(self.user_session)
                else:
                    logging.debug("do_menu() COMMAND is unexpected type: {type(command)}")
                    logging.error_message(f"Command ({command}) appears valid, but I can't figure out what to do with it.")
            else:
                logging.debug("do_menu() COMMAND is NOT VALID")
                # invalid selection.  We just ignore it an reprint the
                # menu at the beginning of the while loop
                pass
            #self.terminal.writeln()
        return 

    def do_string_command(self, command_string):
        if command_string in ('exit', 'Exit', 'back', 'Back', 'quit', 'Quit'):
            logging.debug("do_string_command() thinks we should break")
            return True

class LogOut(Room):

    def run_room(self):

        # [HACK TODO]
        try:
            username = self.user_session.user.username
            self.terminal.writeln("")
            self.terminal.writeln(f"Goodbye {username}.")
            self.terminal.writeln("")
        except AttributeError:
            self.terminal.writeln("")
            self.terminal.writeln(f"Goodbye whoever you are.")
            self.terminal.writeln("")
