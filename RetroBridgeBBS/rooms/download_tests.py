from types import ModuleType
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu  as menu
#import RetroBridgeBBS.rooms.search_garden
#import SearchGarden

class DownloadTests(rooms.Room):

    def run_room(self):

        self.menu_list = [
            {
              "key"     : "X",
              "label"   : "XMODEM Download Test",
              "command" : self.x_modem_test,
            },
            {
              "key"     : "Y",
              "label"   : "YMODEM Download Test",
              "command" : self.y_modem_test,
            },
            {
              "key"     : "Z",
              "label"   : "ZMODEM Download Test",
              "command" : self.z_modem_test,
            },
            {
              "key"     : 'B',
              "label"   : "Back",
              "command" : "back",
            },
        ]

        self.do_menu()

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
