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
    archive_name = 'user_entered_url'    # used in filepath, so no weird characters

    def __init__(self, user_session, files=None):
        self.files = files
        rooms.Room.__init__(self, user_session)

    def run_room(self):
        logging.debug(f"Running a GenericAppPage for the file/s: {self.files}")
        self.menu_list = []
        for link in self.files:
            link.load_header_info()
            self.menu_list.append(self.create_menu_entry(link))
        self.do_menu(menu_list=self.menu_list, title="Available Downloads", menu_type='Download')
        return

    def create_menu_entry(self, link):
        """
        link is a Link instance
        """
        entry = {
               "key" : None,
              "label": link.filename,
           "command" : self.get_file_from_archive,
              "args" : { 'link':link },
              "test" : None
        }
        return entry

