import os, pathlib, re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer

"""
RetroBridgeBBS/rooms/archives/__init__.py

All archive rooms expect to be created with a url argument in addition to the user_session.
"""

"""
Macintosh garden won't accept whatever the default python requests user agent is, so I
grabbed this off of stack exchange.  I would like to modify it so that it identifies
itself as RetroBridgeBBS someday [TODO]
"""
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

class Patterns(object):
    file_url_patterns  = ['^.*\.(?!html$|htm$|php$|pdf$)[^\.]+$']
    file_text_patterns = []

class Link(object):
    """
    Links is a base class to create File and Directory objects.
    """


    def __init__(self, soup_link, base_url,
                       translate_url_function = None,
                       metadata = None):

        self.soup_link   = soup_link
        self.base_url    = base_url
        self.url = urljoin(base_url, soup_link.attrs['href'])

        if metadata is not None:
            self.metadata = metadata
        else:
            self.metadata      = {
                            'filename'      : None,
                            'filesize'      : None,
                            'category'      : None,
                            'rating'        : None,
                            'label'         : None,
                            'description'   : None,
                            'compatability' : None,
                            'compression_note' : None,
                            'notes'         : [],
                        }

        self.header_loaded = False

        if self.metadata['filename'] is None:
            self.metadata['filename'] = soup_link.attrs['href'].split("/")[-1]
        if self.metadata['label'] is None:
            if soup_link.text.startswith("http"):
                self.metadata['label'] = ""
            else:
                self.metadata['label'] = soup_link.text


    def __repr__(self):
        return self.metadata['filename']


class Directory(Link):
    """
    Unused.  Deprecated?
    """
    TYPE = 'Directory'

class File(Link):
    TYPE = 'File'

    sit_patterns = [
            [b"^SIT!",  "StuffIt pre 5.5"],
            [b"^StuffIt", "StuffIt 5.5 or later"],
    ]

    def load_header_info(self):
        logging.debug("load_header_info()")
        if self.header_loaded is False:
            logging.debug(f"Loading header... Checking extension of {self.metadata['filename']}")
            self.header_loaded = True
            if self.metadata['filename'][-4:] in ['.sit', '.SIT']:
                logging.debug(f"Filename: {self.metadata['filename']} matches!")
                # DL Headers and look at files
                headers = {"Range": "bytes=0-200", 'User-Agent': USER_AGENT}
                #full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
                header = requests.get(self.url, headers=headers).content
                for p in self.sit_patterns:
                    r = re.compile(p[0])
                    m = r.match(header)
                    if m:
                        self.metadata['notes'].append(p[1])
            if self.metadata['filesize'] is None:
                _r = requests.head(self.url, headers={'User-Agent': USER_AGENT})
                if 'Content-Length' in _r.headers:
                    size_in_bytes = int(_r.headers['Content-Length'])
                    self.metadata['filesize'] = f"{round(size_in_bytes / 1000)}k"
                else:
                    self.metadata['filesize'] = '??k'


class Room(rooms.Room):
    USER_AGENT = USER_AGENT
    archive_id = 'archive'    # used in filepath, so no weird characters
    archive_name = 'archive'

    done = False

    def __init__(self, user_session, url=None):
        if url is None:
            url = 'http://www.savagetaylor.com/2018/05/28/setting-up-your-vintage-classic-68k-macintosh-creating-your-own-boot-able-disk-image/'
        self.url = url
        rooms.Room.__init__(self, user_session)

    def run_room(self):
        self.get_page(self.url)
        self.parse_soup(self.soup)

        self.menu_list = []
        for link in self.extracted_links_dict['files']:
            self.menu_list.append(self.create_menu_entry(link))
        self.do_menu(menu_list=self.menu_list, title=self.archive_name)
        return

    def parse_soup(self, soup):
        self.extracted_links_dict = self.extract_links(self.soup)

    def create_menu_entry(self, link):
        """
        link is a Link instance
        """
        import RetroBridgeBBS.rooms.archives.generic_app_page as generic_app_page
        entry = {
               "key" : None,
              "label": link.metadata['filename'],
           "command" : generic_app_page.GenericAppPage,
              "args" : { 'files':[link] },
              "test" : None
        }
        return entry

    #def follow_link(self, link):
        #logging.debug(f"Here we are, following the link for {link}!")
        #link.load_header_info()
        #logging.debug(f"{link} size: {link.filesize}")
        #logging.debug(f"{link} notes: {link.notes}")

    def extract_links(self, soup):
        """
        This is enteded to scrape simple one-page sites, or web-tree style archives.
        More sophisticated websites will not use this function, and will instead
        have their own webscraping function
        """

        links = soup.findAll('a')
        ignored_links      = []
        files              = []
        for idx, link in enumerate(links):
            parsed_url = urlparse(link.get('href'))
            for p in Patterns.file_url_patterns:
                r = re.compile(p)
                m = r.match(parsed_url.path.split('/')[-1])
                if m:
                    f = File(link, base_url=self.url)
                    #if link.attrs['href'].split("/")[-1] == 'OS_608_100MB.zip':
                        #breakpoint()
                    files.append(f)
                    break
            for p in Patterns.file_text_patterns:
                r = re.compile(p)
                m = r.match(link.text)
                if m:
                    f = File(link, base_url=self.url)
                    files.append(f)
                    break
            ignored_links.append(link)
        links = {
            'files' : files,
            'ignored' : ignored_links,
            'all' : links,
        }
        return links

    def massage_download_url(self, dl_url, file_dict=None):
        return

    def get_page(self, url=None):
        self.user_session.terminal.writeln("Connecting to archive...")
        page      = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        self.soup = BeautifulSoup(page.content, 'lxml')
        self.parse_soup(self.soup)
        return

    #def get_file_from_archive(self, file_metadata=None, send_over_modem=True):
    def get_file_from_archive(self, link, send_over_modem=True):
        #dl_url  = file_metadata['url']
        #dl_file = file_metadata['name']
        dl_url   = link.url
        dl_file  = link.metadata['filename']
        full_url = link.url
        #breakpoint()
        self.terminal.writeln(f"Starting DL of {dl_file}")
        #full_url = self.massage_download_url(dl_url, file_metadata=file_metadata)
        myfile = requests.get(full_url, headers={'User-Agent': self.USER_AGENT})
        local_save_dir = os.path.join(self.bbs.archive_downloads_path, self.archive_id)
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



