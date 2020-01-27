class Room(object):

    def __init__(self,user_session):
        self.terminal     = user_session.terminal
        self.user_session = user_session
        DOWNLOAD_CAPABLE = user_session.device_io.DOWNLOAD_CAPABLE
        self.run_room()
        return


class LogOut(Room):

    def run_room(self):
        username = self.user_session.username
        self.terminal.writeln("")
        self.terminal.writeln(f"Goodbye {username}")
        self.terminal.writeln("")
