from types import ModuleType
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu  as menu
import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives.garden.search_garden
import RetroBridgeBBS.rooms.archives.user_entered_url
import RetroBridgeBBS.rooms.archives.setting_up_your_68k_mac_savagetaylor

class FileAreaMainMenu(rooms.Room):

    def run_room(self):

        self.menu_list = [
            {
               "key" : None,
              "label": "Test New Archive System",
           "command" : RetroBridgeBBS.rooms.archives.Room,
              "test" : None
            },
            {
               "key" : "G",
              "label": "Search Macintosh Garden Downloads",
           "command" : RetroBridgeBBS.rooms.archives.garden.search_garden.SearchGarden,
              "test" : None
            },
            {
               "key" : None,
              "label": "Setting up your vintage (classic) 68k Mac",
           "command" : RetroBridgeBBS.rooms.archives.setting_up_your_68k_mac_savagetaylor.Savagetaylor,
              "test" : None
            },
            {
               "key" : "W",
              "label": "Enter a website URL",
           "command" : RetroBridgeBBS.rooms.archives.user_entered_url.UserEnteredUrl,
              "test" : None
            },
            {
              "key"     : "U",
              "label"   : "Upload a file",
              "command" : self.receive_file,
            },
            {
              "key"     : 'B',
              "label"   : "Back",
              "command" : "back",
            },
        ]

        self.do_menu(title="Online Macintosh Archives")

    def receive_file(self):
        transfer.receive_file(self.user_session)
