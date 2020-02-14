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

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

class Patterns(object):
    file_url_patterns  = ['^.*\.(?!html$|htm$|php$|pdf$)[^\.]+$']
    file_text_patterns = []

class Link(object):
    """
    metadata:
        url             string
        filename        string
        label           string
        category        string
        description     string
        file_size       string
        notes           array of strings
    """

    filesize = None
    header_loaded = False
    notes = []
    description = None
    category = None
    category = None
    label = None

    def __init__(self, soup_link, base_url, translate_url_function=None, filename=None, label=None, description=None, notes=None, filesize=None, category=None):
        self.soup_link   = soup_link
        self.base_url    = base_url
        if filename is not None:
            self.filename = filename
        else:
            self.filename = soup_link.attrs['href'].split("/")[-1]
        if category is not None:
            self.category = category
        if filesize is not None:
            self.filesize = filesize
        if notes is not None:
            self.notes = notes
        if description is not None:
            self.description = description
        if label is not None:
            self.label = label
        else:
            self.label = soup_link.text
        self.url = urljoin(base_url, soup_link.attrs['href'])

    def __repr__(self):
        return self.filename

class Directory(Link):
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
            logging.debug(f"Loading header... Checking extension of {self.filename}")
            self.header_loaded = True
            if self.filename[-4:] in ['.sit', '.SIT']:
                logging.debug(f"Filename: {self.filename} matches!")
                # DL Headers and look at files
                headers = {"Range": "bytes=0-200", 'User-Agent': USER_AGENT}
                #full_url = _url.replace("/sites", "http://mirror.macintosharchive.org")
                header = requests.get(self.url, headers=headers).content
                for p in self.sit_patterns:
                    r = re.compile(p[0])
                    m = r.match(header)
                    if m:
                        self.notes.append(p[1])
            if self.filesize is None:
                size_in_bytes = int(requests.head(self.url, headers={'User-Agent': USER_AGENT}).headers['Content-Length'])
                self.filesize = f"{round(size_in_bytes / 1000)}k"


class Room(rooms.Room):
    #USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    USER_AGENT = USER_AGENT
    archive_name = 'archive'    # used in filepath, so no weird characters

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
        self.do_menu(menu_list=self.menu_list)
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
              "label": link.filename,
           "command" : generic_app_page.GenericAppPage,
              "args" : { 'files':[link] },
              "test" : None
        }
        return entry

    def follow_link(self, link):
        logging.debug(f"Here we are, following the link for {link}!")
        link.load_header_info()
        logging.debug(f"{link} size: {link.filesize}")
        logging.debug(f"{link} notes: {link.notes}")

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
        dl_file  = link.filename
        full_url = link.url
        self.terminal.writeln(f"Starting DL of {dl_file}")
        #full_url = self.massage_download_url(dl_url, file_metadata=file_metadata)
        myfile = requests.get(full_url)
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



# parse_web_tree isn't used.  It's here for reference.

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
