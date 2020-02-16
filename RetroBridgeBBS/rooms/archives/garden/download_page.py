import re, os
import logging
import requests
from bs4 import BeautifulSoup
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.menu as menu
import RetroBridgeBBS.rooms.archives.garden as garden
#import RetroBridgeBBS.file_transfer as transfer
import pdb

cache = {
}

class DownloadPage(garden.Room):

    def run_room(self):
        return

#    def print_report(self, url, file_list, meta_dict, soup):
#        WIDTH = 80
#        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
#        self.terminal.writeln("| " + url + " "*(WIDTH-4-len(url)) + " |")
#        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
#
#        import textwrap
#        from textwrap import wrap, dedent
#        raw_desc = meta_dict['description']
#        desc_list = wrap(raw_desc, WIDTH-4)
#        for line in desc_list:
#            self.terminal.writeln("| " + line+ " "*(WIDTH-4-len(line)) + " |")
#        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
#
#        for idx, f in enumerate(file_list):
#            _name = f['name']
#            _url  = f['url']
#            _notes = []
#            _notes.append(f['size'])
#            _notes.append(f['compatibility'])
#            if _name[-4:] in ['.sit', '.SIT']:
#                # DL Headers and look at files
#                headers = {"Range": "bytes=0-200", 'User-Agent': self.USER_AGENT}
#                full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
#                header = requests.get(full_url, headers=headers).content
#                for _p in sit_patterns:
#                    _r = re.compile(_p[0])
#                    _m = _r.match(header)
#                    if _m:
#                        _notes.append(_p[1])
#                _r = re.compile(b"\.img")
#                _m = _r.match(header)
#                if _m:
#                    _notes.append("Disk Image")
#                    _notes.append(header.content[88:96])
#            if _name[-4:] in ['.img']:
#                # DL Headers and look at files
#                headers = {"Range": "bytes=0-200", 'User-Agent': self.USER_AGENT}
#                full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
#                header = requests.get(full_url, headers=headers).content
#                _found = False
#                for _p in disk_copy_pattens:
#                    _r = re.compile(_p[0])
#                    _m = _r.match(header)
#                    if _m:
#                        _found = True
#                        _notes.append(_p[1])
#                if _found == False:
#                    _notes.append("Probably not Disk Copy 4.2")
#
#            notes_string = " : ".join(_notes)
#            self.terminal.writeln(f"| {idx+1:2} | {_name:{WIDTH-9}} |")
#            self.terminal.writeln(f"|    | {notes_string:{WIDTH-9}} |")
#
#        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
#        self.terminal.writeln(f"| B  | {'Back to Search Results':{WIDTH-9}} |")
#        self.terminal.writeln("+"+"-"*(WIDTH-2)+"+")
#
#        return
#
#    def get_page(self, url):
#
#        descr = soup.findAll("div", {"class": "descr"})
#        descr_rows = soup.findAll("tr")
#
#        # Extract Meta Data
#        meta_data = dict()
#        for row in descr_rows[1:]:      #first row has rating info, and we handle it after this loop
#            table_cells = row.findAll("td")
#            cell_name = table_cells[0].text
#            if cell_name.endswith(':'):         # Should be all of them, but just in case.
#                cell_name = cell_name[:-1]
#            if cell_name == 'Category':
#                cell_info = table_cells[1].find("a").attrs['href']
#            else:
#                cell_info = table_cells[1].text
#                cell_info = " ".join(cell_info.split(sep=None))     # Get rid of tabs, newlines and excessive whitespace
#            if len(cell_info) > 0:
#                meta_data[cell_name] = cell_info
#
#
#        meta_data['description'] = soup.find("p").text
#        if len(meta_data['description']) > 255:
#            meta_data['description'] = meta_data['description'][0:255] + '...'
#
#        meta_data['page_name'] = soup.find('h1').text
#
#        DL_divs = soup.find("div", {"class":"descr"}).findAll("div", {"class": "note download"})
#
#        download_links = []
#        for div in DL_divs:
#            file_dict = {}
#
#            # <a href="/sites/macintoshgarden.org/files/games/mazewarsplus.zip">www</a>
#            href = div.find('a')
#            _url = href.attrs['href']
#            _name = _url.split('/')[-1]
#            file_dict['url'] = _url
#            file_dict['name'] = _name
#
#            # <small>mazewarsplus.zip <i>(1.61 MB</i>)</small>
#            _size = " ".join(div.findAll('small')[-2].text.split()[1:])[1:-1]
#            file_dict['size'] = _size
#
#            # compatibility text is after last <br>
#            _compat = ''.join(div.findAll('br')[-1].next_siblings)
#            # strip tabs, newlines and extraspace
#            _compat = " ".join(_compat.split(sep=None))
#            system_list = _compat.split('-')
#            condensed = system_list[0] + '-' + system_list[-1]
#            file_dict['compatibility'] = condensed
#
#            download_links.append(file_dict)
#
#        return download_links, meta_data, soup
#
