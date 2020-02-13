import os, pathlib, re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
#import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives as archives


class GenericAppPage(archives.Room):
    archive_name = 'user_entered_url'    # used in filepath, so no weird characters

    def __init__(self, user_session, files=None):
        self.files = files
        rooms.Room.__init__(self, user_session)

    def run_room(self):
        logging.debug(f"Running a GenericAppPage for the file/s: {self.files}")
        breakpoint()
        return

    def create_menu_entry(self, link):
        """
        link is a Link instance
        """
        entry = {
               "key" : None,
              "label": link.filename,
           "command" : self.follow_link,
              "args" : { 'link':link },
              "test" : None
        }
        return entry

