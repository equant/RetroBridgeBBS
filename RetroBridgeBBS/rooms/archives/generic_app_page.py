import os, pathlib, re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
#import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives as archives

"""
This generates a room with a menu to download all of the RetroBridgeBBS.rooms.archives.links
containted within the list 'files'.
"""


class GenericAppPage(archives.Room):
    archive_id = 'generic_app_page'    # used in filepath, so no weird characters
    archive_name = 'generic_app_page'

    def __init__(self, user_session, files=None, menu_title="Available Downloads", menu_intro=None, menu_outro=None):
        self.menu_intro = menu_intro
        self.menu_outro = menu_outro
        self.menu_title = menu_title
        if files is not None:
            self.files = files
        else:
            self.files = self.get_files()
        rooms.Room.__init__(self, user_session)

    def get_files(self):
        pass

    def run_room(self):
        logging.debug(f"Running a GenericAppPage for the file/s: {self.files}")
        self.menu_list = []
        for link in self.files:
            link.load_header_info()
            self.menu_list.append(self.create_menu_entry(link))
        self.do_menu(menu_list  = self.menu_list,
                     title      = self.menu_title,
                     menu_intro = self.menu_intro,
                     menu_outro = self.menu_outro,
                     menu_type  = 'Download')
        return

    def create_menu_entry(self, link):
        """
        link is a Link instance
        """
        entry = {
               "key" : None,
              "label": link.metadata['filename'],
           "command" : self.get_file_from_archive,
              "args" : { 'link':link },
              "test" : None
        }
        return entry

