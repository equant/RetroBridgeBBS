from types import ModuleType
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu  as menu
import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.external_sites.garden.search_garden

class FileAreaMainMenu(rooms.Room):

    def run_room(self):

        self.menu_list = [
            {
               "key" : "S",
              "label": "Search Macintosh Garden Downloads",
           "command" : RetroBridgeBBS.rooms.external_sites.garden.search_garden.SearchGarden,
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

        self.do_menu()

    def receive_file(self):
        transfer.receive_file(self.user_session)
