import re, os
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu as menu
import RetroBridgeBBS.rooms.external_sites
import RetroBridgeBBS.rooms.external_sites.garden as garden
import requests
from bs4 import BeautifulSoup
import pdb

cache = {
}

sit_patterns = [
        [b"^SIT!",  "StuffIt pre 5.5"],
        #[b"StuffIt (c)1997", "5.5 or later"],
        [b"^StuffIt", "StuffIt 5.5 or later"],
        #[b"S", "FOO"],
]

disk_copy_pattens = [
        [b"dImgdCpy",  "Probably Disk Copy 4.2"],
]



class DownloadPage(garden.Room):

    def __init__(self, session, url):
        self.url = url
        rooms.Room.__init__(self, session)

    def run_room(self):
        url=self.url
        files, meta, soup = self.get_page(url)
        self.print_report(url, files, meta, soup)
        return

    def print_report(self, url, file_list, meta_dict, soup):
        WIDTH = 80
        #self.terminal.writeln("12343567890" * 8)
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
        self.terminal.writeln("| " + url + " "*(WIDTH-4-len(url)) + " |")
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        import textwrap
        from textwrap import wrap, dedent
        raw_desc = meta_dict['description']
        desc_list = wrap(raw_desc, WIDTH-4)
        for line in desc_list:
            self.terminal.writeln("| " + line+ " "*(WIDTH-4-len(line)) + " |")
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        # Figure out column widths

        #DEFAULT_COL_WIDTH_NAME = 20
        #names = [x['name'] for x in file_list]
        #longest_name = max(names, key=len)
        #if len(longest_name) > DEFAULT_COL_WIDTH_NAME:
            #col_width_name = DEFAULT_COL_WIDTH_NAME
        #else:
            #col_width_name = len(longest_name)

        for idx, f in enumerate(file_list):
            _name = f['name']
            _url  = f['url']
            _notes = []
            _notes.append(f['size'])
            _notes.append(f['compatibility'])
            if _name[-4:] in ['.sit', '.SIT']:
                # DL Headers and look at files
                headers = {"Range": "bytes=0-200", 'User-Agent': self.USER_AGENT}
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
            if _name[-4:] in ['.img']:
                # DL Headers and look at files
                headers = {"Range": "bytes=0-200", 'User-Agent': self.USER_AGENT}
                full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
                header = requests.get(full_url, headers=headers).content
                _found = False
                for _p in disk_copy_pattens:
                    _r = re.compile(_p[0])
                    _m = _r.match(header)
                    if _m:
                        _found = True
                        _notes.append(_p[1])
                if _found == False:
                    _notes.append("Probably not Disk Copy 4.2")

            notes_string = " : ".join(_notes)
            #if len(_name) > col_width_name:
                #midpoint = int(col_width_name/2)
                #_name = _name[0:midpoint-1] + '..' + _name[midpoint+1:]
            #col_width_notes = WIDTH - col_width_name - 12
            self.terminal.writeln(f"| {idx+1:2} | {_name:{WIDTH-9}} |")
            self.terminal.writeln(f"|    | {notes_string:{WIDTH-9}} |")

        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
        self.terminal.writeln(f"| B  | {'Back to Search Results':{WIDTH-9}} |")
        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")

        ##################################################
        #                     PROMPT                     #
        ##################################################
        c = self.terminal.character_prompt("SELECT")
        if c in ('B', 'b', 'Q', 'q'):
            return
        if c.isnumeric:
            selected_index = int(c) - 1
            try:
                file_list[selected_index]
                valid_selection = True
                dl_url   = file_list[selected_index]['url']
                dl_file = file_list[selected_index]['name']
            except IndexError:
                valid_selection = False
                dl_url   = None
                dl_file = None
            #except TypeError:
                #valid_selection = False
                #dl_url   = None
                #dl_file = None
        else:
            valid_selection = False
            dl_url   = None
            dl_file = None



        # Send input feedback to terminal
        if valid_selection:
            self.terminal.writeln(f"Starting DL of {dl_file}")
            #self.terminal.newline()
            #breakpoint()
            full_url = dl_url.replace("/sites", "http://mirror.macintosharchive.org")
            myfile = requests.get(full_url)
            #saved_dl = f"/tmp/{dl_file}"
            saved_dl = os.path.join(self.bbs.archive_downloads_path, f"{dl_file}")
            open(saved_dl, 'wb').write(myfile.content)
            try:
                import subprocess
                # A very small local file useful for testing the client's ability to download
                #binary_file = 'files/Zippy-S1.5.1.sit' 
                #BAUD = str(self.terminal.comm.baudrate)
                #DEV  = self.terminal.comm.name
                BAUD = str(self.terminal.device_io.comm.baudrate)
                DEV  = self.terminal.device_io.comm.name
                protocol = 'ymodem'
                self.terminal.writeln(f'Preparing to send {dl_file} using {protocol} protocol...')
                #subprocess.call(["sudo", "bash", "shell_scripts/ysend.sh", DEV, BAUD, binary_file])
                logging.debug(f"subprocess.call(): {protocol}, {DEV}, {BAUD}, {saved_dl}")
                subprocess.call(["bash", "shell_scripts/send.sh", f"-{protocol}", DEV, BAUD, saved_dl])
            except:
                logging.info("Skipped X/Y/ZModem transfer because terminal doesn't support it")
                self.terminal.writeln()
                self.terminal.writeln("Skipped X/Y/ZModem transfer because terminal doesn't support it")
                self.terminal.writeln()
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
            page = requests.get(url, headers={'User-Agent': self.USER_AGENT})
            # html.parser has issues correctly parsing macintoshgarden div tags.
            # so don't use...
            # soup = BeautifulSoup(page.content, 'html.parser')
            soup = BeautifulSoup(page.content, 'html5lib')
            cache[url] = soup

        descr = soup.findAll("div", {"class": "descr"})
        descr_rows = soup.findAll("tr")

        # Extract Meta Data
        meta_data = dict()
        for row in descr_rows[1:]:      #first row has rating info, and we handle it after this loop
            table_cells = row.findAll("td")
            cell_name = table_cells[0].text
            if cell_name.endswith(':'):         # Should be all of them, but just in case.
                cell_name = cell_name[:-1]
            if cell_name == 'Category':
                cell_info = table_cells[1].find("a").attrs['href']
            else:
                cell_info = table_cells[1].text
                cell_info = " ".join(cell_info.split(sep=None))     # Get rid of tabs, newlines and excessive whitespace
            if len(cell_info) > 0:
                meta_data[cell_name] = cell_info


        meta_data['description'] = soup.find("p").text
        if len(meta_data['description']) > 255:
            meta_data['description'] = meta_data['description'][0:255] + '...'

        meta_data['page_name'] = soup.find('h1').text

        DL_divs = soup.findAll("div", {"class": "note download"})

        download_links = []
        for div in DL_divs:
            file_dict = {}

            # <a href="/sites/macintoshgarden.org/files/games/mazewarsplus.zip">www</a>
            href = div.find('a')
            _url = href.attrs['href']
            _name = _url.split('/')[-1]
            file_dict['url'] = _url
            file_dict['name'] = _name

            # <small>mazewarsplus.zip <i>(1.61 MB</i>)</small>
            _size = " ".join(div.findAll('small')[-2].text.split()[1:])[1:-1]
            file_dict['size'] = _size

            # compatibility text is after last <br>
            _compat = ''.join(div.findAll('br')[-1].next_siblings)
            # strip tabs, newlines and extraspace
            _compat = " ".join(_compat.split(sep=None))
            #_compat = _compat.replace("For ", "")
            #_compat = _compat.replace("System ", "")
            system_list = _compat.split('-')
            condensed = system_list[0] + '-' + system_list[-1]
            file_dict['compatibility'] = condensed

            download_links.append(file_dict)

        return download_links, meta_data, soup

