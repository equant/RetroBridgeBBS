import os, pathlib, re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives as archives

class UserEnteredUrl(archives.Room):
    archive_name = 'user_entered_url'    # used in filepath, so no weird characters

    def __init__(self, user_session, url=None):
        if url is None:
            url = 'http://www.savagetaylor.com/2018/05/28/setting-up-your-vintage-classic-68k-macintosh-creating-your-own-boot-able-disk-image/'
        url = user_session.terminal.string_prompt("Enter URL")
        archives.Room.__init__(self, user_session, url)
