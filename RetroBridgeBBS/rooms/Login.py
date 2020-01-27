import Room

class Login(Room.Room):

    def __init__(self, session):
        Room.Room.__init__(self, session)
        self.term.clearscreen()
        self.term.newline()
        self.term.newline()
        self.term.writeln(f'connected to {self.term.comm.name}')
        self.term.write('Macintosh login: ')
        username = self.term.get_line()
        self.term.newline()
        self.term.writeln(f'Welcome {username}!')
        self.session.username = username
        self.term.newline()
