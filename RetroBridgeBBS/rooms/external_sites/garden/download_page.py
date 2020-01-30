import re
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu as menu
import RetroBridgeBBS.rooms.external_sites
import RetroBridgeBBS.rooms.external_sites.garden as garden
import requests
from bs4 import BeautifulSoup

cache = {
}

sit_patterns = [
        [b"^SIT!",  "pre 5.5"],
        #[b"StuffIt (c)1997", "5.5 or later"],
        [b"^StuffIt", "5.5 or later"],
        #[b"S", "FOO"],
]


class DownloadPage(rooms.Room):

    def __init__(self, session, url):
        self.url = url
        rooms.Room.__init__(self, session)

    def run_room(self):
        url=self.url
        files, meta, soup = self.get_page(url)
        self.print_report(url, files, meta, soup)
        return

    def print_report(self, url, files, meta, soup):
        WIDTH = 64
        #self.terminal.writeln("12343567890" * 8)
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
        self.terminal.writeln("| " + url + " "*(WIDTH-4-len(url)) + " |")
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        import textwrap
        from textwrap import wrap, dedent
        raw_desc = meta['description']
        desc_list = wrap(raw_desc, WIDTH-4)
        for line in desc_list:
            self.terminal.writeln("| " + line+ " "*(WIDTH-4-len(line)) + " |")
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        for idx, f in enumerate(files):
            _name = f[0]
            _url  = f[1]
            _notes = []
            if _name[-4:] in ['.sit', '.SIT']:
                # DL Headers and look at files
                headers = {"Range": "bytes=0-200", 'User-Agent': garden.USER_AGENT}
                full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
                header = requests.get(full_url, headers=headers).content
                for _p in sit_patterns:
                    _r = re.compile(_p[0])
                    _m = _r.match(header)
                    if _m:
                        _notes.append(_p[1])
                _r = re.compile(b"\.img")
                _m = _r.match(header)
                if _m:
                    _notes.append("Disk Image")
                    _notes.append(header.content[88:96])
            notes_string = ":".join(_notes)
            self.terminal.writeln(f"| {idx+1:2} | {_name:20} | {notes_string:32} |")

        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        #self.terminal.write("SELECT >> ")
        #character = self.terminal.comm.read()
        #c = character.decode()
        c = self.terminal.character_prompt("SELECT")
        selected_index = int(c) - 1

        try:
            files[selected_index]
            valid_selection = True
            dl_url   = files[selected_index][1]
            dl_file = files[selected_index][0]
        except IndexError:
            valid_selection = False
            dl_url   = None
            dl_file = None
        except TypeError:
            valid_selection = False
            dl_url   = None
            dl_file = None



        # Send input feedback to terminal
        if valid_selection:
            self.terminal.writeln(f"Starting DL of {dl_file}")
            #self.terminal.newline()
            full_url = dl_url.replace("/sites", "http://mirror.macintosharchive.org")
            myfile = requests.get(full_url)
            saved_dl = f"/tmp/{dl_file}"
            open(saved_dl, 'wb').write(myfile.content)
            import subprocess
            # A very small local file useful for testing the client's ability to download
            #binary_file = 'files/Zippy-S1.5.1.sit' 
            #BAUD = str(self.terminal.comm.baudrate)
            #DEV  = self.terminal.comm.name
            BAUD = "9600"
            DEV  = "/dev/ttyUSB0"
            protocol = 'ymodem'
            self.terminal.writeln(f'Preparing to send {dl_file} using {protocol}MODEM...')
            #subprocess.call(["sudo", "bash", "shell_scripts/ysend.sh", DEV, BAUD, binary_file])
            subprocess.call(["bash", "shell_scripts/send.sh", f"-{protocol}", DEV, BAUD, saved_dl])

        else:
            self.terminal.writeln(f"[{c}] - Invalid!")
            #self.terminal.newline()
            pass

        self.terminal.newline()
        return

    def get_page(self, url):

        if url in cache.keys():
            print("Getting soup from cache")
            soup = cache[url]
        else:
            #self.terminal.debug(url)
            page = requests.get(url, headers={'User-Agent': garden.USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            cache[url] = soup

        # Extract Table with ratings, year, and download links
        T = soup.find("table")
        table_rows = T.find_all("tr")

        # Extract Meta Data
        meta_data = dict()
        meta_data['rating'] = float(table_rows[0].find_all('div')[-1].find_all('span')[2].find('span').text)
        meta_data['category_string'] = table_rows[1].find("a").text
        meta_data['category_url']    = table_rows[1].find("a").attrs['href']
        #year_string = table_rows[2].find("a").text
        #year_url    = table_rows[2].find("a").attrs['href']
        #author_string = table_rows[3].find("a").text
        #author_url    = table_rows[3].find("a").attrs['href']
        #publisher_string = table_rows[4].find("a").text
        #publisher_url    = table_rows[4].find("a").attrs['href']
        meta_data['description'] = soup.find("p").contents[0]

        DL_divs = soup.findAll("div", {"class": "note download"})

        download_links = []
        for div in DL_divs:
            href = div.find('a')
            _url = href.attrs['href']
            _name = _url.split('/')[-1]
            download_links.append([_name, _url])

        return download_links, meta_data, soup

