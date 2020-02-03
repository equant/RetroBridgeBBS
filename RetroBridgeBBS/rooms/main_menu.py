from types import ModuleType
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.rooms.download_tests
import RetroBridgeBBS.rooms.file_area_main_menu
import subprocess
#import SearchGarden

class MainMenu(rooms.Room):

    def run_room(self):
        self.menu_list = [
            {
               "key" : "F",
              "label": "Files (Search, DL, etc)",
           "command" : RetroBridgeBBS.rooms.file_area_main_menu.FileAreaMainMenu,
              "test" : None
            },
            {
               "key" : "D",
               "label": "Download Tests (Test X/Y/ZModem transfer)",
                "command" : RetroBridgeBBS.rooms.download_tests.DownloadTests,
              "test" : None
            },
            {
               "key" : "U",
              "label": "Uptime",
              "command" : self.command_uptime,
              "test" : None
            },
        ]
        self.do_menu()
        return


    def command_uptime(self):
        #self.terminal.writeln("UPTIME!"*5)
        self.terminal.writeln()
        self.terminal.writeln("System uptime...")
        subprocess.call(["uptime"])
        self.terminal.writeln()
        foo = self.terminal.pause()

