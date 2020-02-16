import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu as menu
import RetroBridgeBBS.rooms.archives
import RetroBridgeBBS.rooms.archives.garden as garden
import RetroBridgeBBS.rooms.archives.garden.download_page
import requests
from bs4 import BeautifulSoup

cache = {
}

class SearchGarden(garden.Room):

    def run_room(self):
        self.do_search()

    def do_search(self):
        search_term = self.get_search_term()
        results, soup = self.query_mac_garden(search_term)
        if len(results) >= 1:       # 2, because all results have "Back" appended
            self.terminal.writeln("Here are some applications that match your search term:")
            self.search_term = search_term
            self.do_link_menu(results)
        else:
            self.terminal.writeln(f"Sorry, no matches found for '{search_term}'")
            self.terminal.newline()
        return

    def do_link_menu(self, url_list):
        # Build menu from list
        _menu = []
        for item in url_list:
            _menu.append({'key':None, 'label':item['name'], 'command':item['url']})
        _menu.append({'key':'B', 'label':'Back to search', 'command':'back'})

        # Display and Handle menu
        m = menu.Menu(self.user_session, _menu, title=f"Search results for '{self.search_term}'")
        self.do_menu(m=m, menu_list=_menu)

        """
            url = menu_results['fn']
            if menu_results['valid']:
                if url != 'back':
                    GardenApplicationPage.GardenApplicationPage(self.user_session, url)
            else:
                # invalid selection.  We just ignore it an reprint the
                # menu at the beginning of the while loop
                pass
        """
        return 

    def do_string_command(self, command_string):
        if command_string in ('quit', 'back'):
            return True
        else:
            url = command_string
            RetroBridgeBBS.rooms.archives.garden.download_page.DownloadPage(self.user_session, url)
            return False


    def get_search_term(self):
        self.terminal.newline()
        self.terminal.newline()
        self.terminal.write('Enter Search Term: ')
        search_term = self.terminal.readln()
        self.terminal.writeln()
        self.terminal.writeln()
        self.terminal.writeln(f'Searching for {search_term}...')
        return search_term

    def query_mac_garden(self, search_term):

        if search_term in cache.keys():
            print("Getting soup from cache")
            soup = cache[search_term]
        else:
            SEARCH_URL = f"https://macintoshgarden.org/search/node/type%3Aapp%2Cgame%20{search_term}"
            page = requests.get(SEARCH_URL, headers={'User-Agent': self.USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            cache[search_term] = soup

        link_list = soup.find_all("a")

        valid_url_prefixes = [
                'https://macintoshgarden.org/apps/',
                'https://macintoshgarden.org/games/',
        ]

        search_result_webpages = []

        for l in link_list:
            url = l.get_attribute_list('href')[0]
            for valid_prefix in valid_url_prefixes:
                if url.startswith(valid_prefix):
                    name = url.split("/")[-1]
                    search_result_webpages.append({'name':name,'url':url})

        return search_result_webpages, soup
