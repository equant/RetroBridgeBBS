#from serial.tools import list_ports
import textwrap
from textwrap import wrap, dedent
import logging

"""
(no attributes) 	SGR 	ESC [ m
(no attributes) 	SGR 	ESC [ 0 m
(select attribute bold) 	SGR 	ESC [ 1 m
(select attribute underline) 	SGR 	ESC [ 4 m
(select attribute blink) 	SGR 	ESC [ 5 m
(select attribute, reverse video) 	SGR 	ESC [ 7 m
Cursor up 	CUU 	ESC [ Pn A
Cursor down 	CUD 	ESC [ Pn B
Cursor forward (right) 	CUF 	ESC [ Pn C
Cursor backward (left) 	CUB 	ESC [ Pn D
Cursor position 	CUP 	ESC [ Pl ; Pc H
Cursor position (home) 	CUP 	ESC [ H
Horizontal and vertical position 	HVP 	ESC [ Pl ; Pc f
Horizontal and vertical position (home) 	HVP 	ESC [ f
Index 	IND 	ESC D
Reverse index 	RI 	ESC M
Next line 	NEL 	ESC E
Save cursor (and attributes) 	DECSC 	ESC 7
Restore cursor (and attributes) 	DECRC 	ESC 8
"""

class BaseTerminal(object):

    FOO = chr(0x0E);
    CRLF = "\r\n"
    NL = "\r\n"
    ESCAPE = chr(27)
    CLEAR_SCREEN = ESCAPE + "[2J"
    PROMPT_CHARACTER = ": "
    DO_ECHO = True

    TERM_WIDTH = 64

    def __init__(self, bbs, device_io, user_session):
        self.bbs          = bbs
        self.device_io    = device_io
        self.user_session = user_session

    def pause(self):
        self.write(f" --- press enter to continue ---")
        typed_character = self.readln()
        self.writeln()
        self.writeln()
        return typed_character

    def character_prompt(self, prompt):
        self.write(f"{prompt}" + self.PROMPT_CHARACTER)
        typed_character = self.read()
        return typed_character

    def string_prompt(self, prompt):
        self.write(f"{prompt}" + self.PROMPT_CHARACTER)
        typed_string = self.readln()
        self.writeln("")
        return typed_string

    def write(self, data=""):
        self.device_io.write(data)

    def writeln(self, data=""):
        self.device_io.write(data)
        self.device_io.write(self.CRLF)
        print()

    def get_string_hline(self):
        return "-"*80

    def read(self):
        _chr = self.device_io.read()
        if self.DO_ECHO:
            self.write(_chr)
        return _chr

    def readln(self):
        read_string = ""
        _chr = ""
        #while _chr != self.CRLF:
        while _chr not in (self.CRLF, '\n', '\r', '\t', '\r\x00'):
            logging.debug(f"readln() received [{_chr}] which is type: {type(_chr)}")
            logging.debug(f"    [{_chr.encode()}]")
            _chr = self.read()
            #read_string.append(_chr)
            read_string += _chr
        return read_string[:-1]

    def newline(self):
        self.device_io.write(self.CRLF)
        return

    #menu_string += "| " + l + " "*(WIDTH-4-len(l)) + " |" + self.term.CRLF
    #menu_string += "+"+"-"*(WIDTH-2)+"+" + self.term.CRLF
    #menu_string += "+"+"-"*(WIDTH-2)+"+" + self.term.CRLF


    def make_box_title(self, title, crlf=True):
        padded = title.center(self.TERM_WIDTH-4, " ")
        return self.make_box_string(padded, crlf=crlf)


    def make_box_string(self, data, crlf=True):
        _s = "| " + data + " "*(self.TERM_WIDTH-4-len(data)) + " |"
        if crlf:
            _s += self.CRLF
        return _s

    def make_box_hr(self, crlf=True):
        _s = "+"+"-"*(self.TERM_WIDTH-2)+"+"
        if crlf:
            _s += self.CRLF
        return _s



    def color_test(self):
        """
        some code from Michael Alyn Miller and Hermes BBS
        doesn't work with console.  Does it work with ANSI?
        """

        for y in range(7):
            for x in range(7):
                #self.write('\033[%d;%dm\261\261\033[0m' & (30+x, 40+y))
                self.write(f'\033[(30+x);(40+y)m\261\261\033[0m')


##################################################
#                    CONSOLE                     #
##################################################

class ConsoleTerminal(BaseTerminal):
    """
    For linux console.  Not telnet, not serial
    """

    CRLF = "\n"
    ESCAPE = ""
    CLEAR_SCREEN = ""
    DO_ECHO = False
    NL = "\n"

    def readln(self):
        _chr = self.read()
        logging.debug(f"ConsoleTerminal: readln() received [{_chr}] which is type: {type(_chr)}")
        logging.debug(f"    [{_chr.encode()}]")
        return _chr

    def writeln(self, data=""):
        self.device_io.write(data)
        #self.device_io.write(self.CRLF)
        print()

#    def text_normal(self):
#        self.device_io.write(f"{Escape}[m".encode())
#        self.device_io.write(f"{Escape}[0m".encode())
#    def text_bold(self):
#        self.device_io.write(f"{Escape}[1m".encode())
#    def text_underline(self):
#        self.device_io.write(f"{Escape}[4m".encode())
#    def text_blink(self):
#        self.device_io.write(f"{Escape}[5m".encode())
#    def text_reverse_video(self):
#        self.device_io.write(f"{Escape}[5m".encode())
#
#    def clearscreen(self):
#        self.newline()
#        self.device_io.write(vt102['clearscreen'].encode())
#        pass
#
#    def get_line(self, max_length = 80, echo=True, local_echo=True):
#        """
#        Gets a line of input from the user.  Returns a string.
#        echo=True         echo user's input back to the user's terminal
#        local_echo=True   echo user's input onto the host computer's terminal
#        """
#
#        byte      = ""   # This stores the most recently received byte/character 
#        bytelist  = []
#        while byte not in [b'\n', b'\r']:
#            byte = self.device_io.read()
#            if local_echo:
#                # arguments passed to print() let it show one character at a time
#                print(byte.decode(), end='', flush=True)
#            if echo:
#                self.device_io.write(byte)
#            if byte == b'\x08':         # backspace
#                bytelist.pop()          # remove last byte
#            else:
#                bytelist.append(byte)
#            if len(bytelist) > 25:
#                break
#        line = "".join([x.decode('utf-8') for x in bytelist[0:-1]])
#        return line
#
#
#    def write(self, _s, local_echo=True):
#        """
#        Sends a string out to the serial conenction
#        """
#
#        encoded_string = _s.encode()
#        self.device_io.write(encoded_string)
#        if local_echo:
#            print(_s, end='', flush=True)
#        return
#
#    def writeln(self, text, local_echo=True, do_wrap=True, do_dedent=True):
#        """
#        Sends a string out to the serial conenction and adds a newline.
#        """
#        for _s in wrap(dedent(text)):
#            self.write(_s)
#            self.newline()
#            if local_echo:
#                print(_s, flush=True)
