import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.users as users

class Login(rooms.Room):

    def __init__(self, user_session, require_password):
        self.require_password = require_password
        rooms.Room.__init__(self, user_session)

    def run_room(self):
        self.terminal.writeln()
        self.terminal.writeln()
        username = self.terminal.string_prompt('Please enter your username')
        if self.require_password:
            password = self.terminal.string_prompt('Password:')
            if users.validate_user(username, password):
                #self.username = username
                user = users.User(username)
                self.user_session.authenticated = True
        else:
            user = users.User(username)
        self.user_session.user = user

