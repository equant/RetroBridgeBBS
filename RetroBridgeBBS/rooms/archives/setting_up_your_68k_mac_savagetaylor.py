import os, pathlib, re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer
import RetroBridgeBBS.rooms.archives as archives

class Savagetaylor(archives.Room):
    archive_name = 'savagetaylor_blog'    # used in filepath, so no weird characters

    def __init__(self, user_session, url=None):
        if url is None:
            url = 'http://www.savagetaylor.com/2018/05/28/setting-up-your-vintage-classic-68k-macintosh-creating-your-own-boot-able-disk-image/'
        user_session.terminal.writeln("""

http://www.savagetaylor.com/2018/05/28/

A collection of disk images and files that are useful for "setting up your vintage (classic) 68k Macintosh"
""")

        archives.Room.__init__(self, user_session, url)
