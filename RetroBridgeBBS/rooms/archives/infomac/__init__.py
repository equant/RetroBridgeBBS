import os, pathlib, re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives as archives
from RetroBridgeBBS.rooms.archives import File, Directory

class Patterns(object):
    file_url_patterns  = ['^.*\.(?!html$|htm$|php$|pdf$)[^\.]+$']
    file_text_patterns = []
    dir_url_patterns  = []
    dir_text_patterns = ['^_']


class Room(archives.Room):
    archive_id = 'info-mac'    # used in filepath, so no weird characters
    archive_name = 'Info-Mac Archive'

    def __init__(self, user_session, url=None):
        if url is None:
            url = 'http://mirror.macintosharchive.org/archive.info-mac.org/'
        self.abstract_dict = {}
        archives.Room.__init__(self, user_session, url)

    def run_room(self):
        self.get_page(self.url)
        file_links, sub_category_links, abstract_links, ignored_links = self.parse_web_tree(self.soup)

        if len(abstract_links) == 1:
            self.abstract_file = File(abstract_links[0][0], base_url=self.url)
            self.parse_abstract(self.abstract_file)


        self.menu_list = []

        for link, matching_pattern in sub_category_links:
            _dir = Directory(link, base_url=self.url)
            self.menu_list.append(self.create_menu_entry_for_directory(_dir))

        for link,p in file_links:
            #link = File(link, base_url=self.url)
            if link.metadata['filename'] in self.abstract_dict.keys():
                link.metadata['description'] = self.abstract_dict[link.metadata['filename']][0:100]
            self.menu_list.append(self.create_menu_entry(link))

        self.do_menu(menu_list=self.menu_list, title=self.archive_name)

        return

    def parse_abstract(self, abstract):
        foo = requests.get(abstract.url, headers={'User-Agent': self.USER_AGENT})
        A = [x.strip() for x in foo.text.split("####")]
        for entry in A[1:]:
            if entry.startswith("LINK"):
                continue
            try:
                entry_type, filename = entry.split(r'****')[0].split()
                entry_type, filename = entry.split(r'****')[0].split()
                description = " ".join(re.split(r'\s\s+', entry.split('****')[1]))
                self.abstract_dict[filename] = description
            except:
                logging.error("Something went wrong with abstract.txt parsing")
                breakpoint()


    def create_menu_entry_for_directory(self, link):
        """
        link is a Link instance
        """
        import RetroBridgeBBS.rooms.archives.generic_app_page as generic_app_page
        entry = {
               "key" : None,
              "label": link.metadata['label'],
           "command" : Room,
              "args" : { 'url':link.url },
        }
        return entry


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



    def parse_web_tree(self, soup):
        """
        parse_web_tree isn't used.  It's here for reference.
        """

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
                    F = File(link, base_url=self.url)
                    F.metadata['timestamp'] = size_rows[idx].findAll('td')[2].text.split(" ")[0]
                    F.metadata['filesize'] = size_rows[idx].findAll('td')[-2].text
                    file_links.append([F, p])
                    break
            for p in file_text_patterns:
                r = re.compile(p)
                m = r.match(link.text)
                if m:
                    #_date = s.findAll('td')[2].text.split(" ")[0]
                    #_size = s.findAll('td')[-2].text
                    F = File(link, base_url=self.url)
                    file_links.append([F, p])
                    break

        return file_links, sub_category_links, abstract_links, ignored_links
