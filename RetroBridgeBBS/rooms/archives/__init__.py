import os, pathlib, re
import requests
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer

"""
RetroBridgeBBS/rooms/archives/__init__.py
"""

class Patterns(object):
    file_url_patterns  = ['.*\..*']
    # https://stackoverflow.com/questions/14473180/regex-to-get-a-filename-from-a-url
    #file_url_patterns  = ['[^/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))']
    #file_url_patterns  = ['(?:.+\/)([^#?]+)']
    file_text_patterns = []

class Link(object):
    """
    metadata:
        name
        category
        description
    """

    def __init__(self, url, metadata=None, files=None):
        self.url = url
        self.metadata = metadata
    pass

class Directory(Link):
    TYPE = 'Directory'

class File(Link):
    TYPE = 'File'
    file_url_patterns  = ['.*\..*']
    #file_text_patterns = []



class Room(rooms.Room):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    archive_name = 'archive'    # used in filepath, so no weird characters

    def run_room(self):
        if False:
            url=self.url
            soup = self.get_page(url)
        soup = self.get_page()
        links, metadata = self.parse_soup(soup)

        self.print_report(url, files, meta, soup)
        return

    def parse_soup(self, soup):
        links_dict = self.extract_links(soup)
        breakpoint()

    def extract_links(self, soup):
        links = soup.findAll('a')
        ignored_links      = []
        file_links         = []
        for idx, link in enumerate(links):
            for p in Patterns.file_url_patterns:
                r = re.compile(p)
                m = r.match(link.attrs['href'].split("/")[-1])
                #breakpoint()
                if m:
                    file_links.append([link, p])
                    break
            for p in Patterns.file_text_patterns:
                r = re.compile(p)
                m = r.match(link.text)
                if m:
                    file_links.append([link, p])
                    break
            ignored_links.append(link)
        links = {
            'files' : file_links,
            'ignored' : ignored_links,
            'all' : links,
        }
        return links

    def massage_download_url(self, dl_url, file_dict=None):
        return

    def get_page(self, url=None):
        #page = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        ## html.parser has issues correctly parsing macintoshgarden div tags.
        ##soup = BeautifulSoup(page.content, 'html.parser')
        ##soup = BeautifulSoup(page.content, 'html5lib')
        #self.soup = BeautifulSoup(page.content, 'lxml')
        #self.parse_soup

        test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/getting_started.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _archive.info-mac.org__Art_&_Info.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _archive.info-mac.org__Game.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _archive.info-mac.org.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _~archive_mac_game_arcade.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _~archive_mac_game.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _~archive_mac.html'
        #test_path = '/home/equant/projects/68k/macintosh_garden_bbs/RetroBridgeBBS/RetroBridgeBBS/rooms/archives/soup_sandbox/saved_html/Index of _max1zzz.co.uk_+Mac OS Classic_Games.html'
        soup = BeautifulSoup(open(test_path), "lxml")
        return soup

    def get_file_from_archive(self, file_metadata=None, send_over_modem=True):
        dl_url  = file_metadata['url']
        dl_file = file_metadata['name']
        self.terminal.writeln(f"Starting DL of {dl_file}")
        #self.terminal.newline()
        #breakpoint()
        #full_url = dl_url.replace("/sites", "http://mirror.macintosharchive.org")
        full_url = self.massage_download_url(dl_url, file_metadata=file_metadata)
        myfile = requests.get(full_url)
        #saved_dl = f"/tmp/{dl_file}"
        local_save_dir = os.path.join(self.bbs.archive_downloads_path, self.archive_name)
        pathlib.Path(local_save_dir).mkdir(parents=True, exist_ok=True)
        saved_dl = os.path.join(local_save_dir, f"{dl_file}")
        open(saved_dl, 'wb').write(myfile.content)
        try:
            transfer.send_file(self.user_session, saved_dl)
        except:
            logging.info("Skipped X/Y/ZModem transfer because terminal doesn't support it")
            self.terminal.writeln()
            self.terminal.writeln("Skipped X/Y/ZModem transfer because terminal doesn't support it")
            self.terminal.writeln()

def parse_web_tree(soup):

    all_links = soup.findAll('a')

    # remove all of the links before (and including)
    # "Parent Directory"
    for _idx, _l in enumerate(all_links):
        if _l.text == 'Parent Directory':
            break
    links = all_links[_idx+1:-1]

    all_rows = soup.findAll("tr")
    size_rows = all_rows[3:-1]

    # Break up links into different groups...
    # Files
    # Subcategories
    # Abstract/s
    # ignored links

    ignored_links      = []
    sub_category_links = []
    file_links         = []
    abstract_links     = []
    unsorted_links     = []

    ignore_url_patterns= [
        '^mailto:'        
    ]
    ignore_text_patterns = ['^\s*$']

    sub_category_url_patterns  = ['^_\.*']
    sub_category_text_patterns = []

    abstract_url_patterns  = []
    abstract_text_patterns = ['.*abstracts\.txt$']

    file_url_patterns  = ['.*\..*']
    file_text_patterns = []

    for idx, link in enumerate(links):
        for p in ignore_url_patterns:
            r = re.compile(p)
            m = r.match(link.attrs['href'])
            if m:
                ignored_links.append([link, p])
                break
        for p in ignore_text_patterns:
            r = re.compile(p)
            m = r.match(link.text)
            if m:
                ignored_links.append([link, p])
                break

        for p in abstract_url_patterns:
            r = re.compile(p)
            m = r.match(link.attrs['href'])
            if m:
                abstract_links.append([link, p])
                break
        for p in abstract_text_patterns:
            r = re.compile(p)
            m = r.match(link.text)
            if m:
                abstract_links.append([link, p])
                break

        for p in sub_category_url_patterns:
            r = re.compile(p)
            m = r.match(link.attrs['href'])
            if m:
                sub_category_links.append([link, p])
                break
        for p in sub_category_text_patterns:
            r = re.compile(p)
            m = r.match(link.text)
            if m:
                sub_category_links.append([link, p])
                break

        for p in file_url_patterns:
            r = re.compile(p)
            m = r.match(link.attrs['href'])
            if m:
                file_links.append([link, p])
                break
        for p in file_text_patterns:
            r = re.compile(p)
            m = r.match(link.text)
            if m:
                _date = s.findAll('td')[2].text.split(" ")[0]
                _size = s.findAll('td')[-2].text
                file_links.append([link, p])
                break
