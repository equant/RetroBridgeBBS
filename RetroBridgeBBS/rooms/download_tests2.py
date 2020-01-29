from types import ModuleType
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu2 as menu2
#import RetroBridgeBBS.rooms.search_garden
#import SearchGarden

class DownloadTests(rooms.Room):

    def run_room(self):

        self.menu_list = [
            {
               "key"  : "X",
              "label" : "XMODEM Download Test",
                "do"  : self.x_modem_test,
              #"test"  : self.device_io.XYZMODEM_CAPABLE,
            },
            {
               "key"  : "Y",
              "label" : "YMODEM Download Test",
                "do"  : self.y_modem_test,
              #"test"  : self.device_io.XYZMODEM_CAPABLE,
            },
            {
               "key"  : "Z",
              "label" : "ZMODEM Download Test",
                "do"  : self.z_modem_test,
              #"test"  : self.device_io.XYZMODEM_CAPABLE,
            },
            {
               "key"  : ['x'],
              "label" : "Exit",
                "do"  : "exit",
              #"test"  : None
            },
        ]

        self.do_menu()

    def do_menu(self):
        m = menu2.Menu2(self.user_session, self.menu_list, add_global_commands=True)

        fn = None
        while fn != 'exit':
            menu_results = m.handle_menu()
            fn = menu_results['fn']
            if menu_results['valid']:
                if type(fn) == str:
                    pass
                elif issubclass(fn, rooms.Room):
                    #fn.FOO(self.user_session)
                    fn(self.user_session)
                else:
                    F = fn()
            else:
                # invalid selection.  We just ignore it an reprint the
                # menu at the beginning of the while loop
                pass
        return 

    def modem_download_test(self, protocol='Y'):
        if protocol not in ['xmodem', 'ymodem', 'zmodem']:
            error_message = f"Error with test_modem_transfer(), unknown protocol: '{protocol}'"
            self.terminal.writeln(error_message)
            return

        import subprocess
        # A very small local file useful for testing the client's ability to download
        binary_file = 'files/Zippy-S1.5.1.sit' 
        self.terminal.writeln(f'Preparing to send {binary_file} using {protocol}MODEM...')
        BAUD = str(self.terminal.comm.baudrate)
        DEV  = self.terminal.comm.name
        #subprocess.call(["sudo", "bash", "shell_scripts/ysend.sh", DEV, BAUD, binary_file])
        subprocess.call(["bash", "shell_scripts/send.sh", f"-{protocol}", DEV, BAUD, binary_file])

    def x_modem_test(self):
        self.modem_download_test('xmodem')

    def y_modem_test(self):
        self.modem_download_test('ymodem')

    def z_modem_test(self):
        self.modem_download_test('zmodem')