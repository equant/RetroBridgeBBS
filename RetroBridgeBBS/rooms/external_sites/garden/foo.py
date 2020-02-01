import re, os
import logging
#import RetroBridgeBBS.rooms as rooms
#import RetroBridgeBBS.menu as menu
#import RetroBridgeBBS.rooms.external_sites
#import RetroBridgeBBS.rooms.external_sites.garden as garden

import requests
from bs4 import BeautifulSoup
import pdb

"""
This is just a test script to work out scraping in ipythong
"""

class foo(object):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

self = foo()

url = 'https://macintoshgarden.org/games/maze-wars'

page = requests.get(url, headers={'User-Agent': self.USER_AGENT})
soup = BeautifulSoup(page.content, 'html.parser')

# Extract Table with ratings, year, and download links
T = soup.find("table")
table_rows = T.find_all("tr")

# Extract Meta Data
meta_data = dict()
meta_data['rating'] = float(table_rows[0].find_all('div')[-1].find_all('span')[2].find('span').text)
meta_data['category_string'] = table_rows[1].find("a").text
meta_data['category_url']    = table_rows[1].find("a").attrs['href']
#year_string = table_rows[2].find("a").text
#year_url    = table_rows[2].find("a").attrs['href']
#author_string = table_rows[3].find("a").text
#author_url    = table_rows[3].find("a").attrs['href']
#publisher_string = table_rows[4].find("a").text
#publisher_url    = table_rows[4].find("a").attrs['href']
meta_data['description'] = soup.find("p").contents[0]

DL_divs = soup.findAll("div", {"class": "note download"})

download_links = []
for div in DL_divs:
    href = div.find('a')
    _url = href.attrs['href']
    _name = _url.split('/')[-1]
    download_links.append([_name, _url])

#return download_links, meta_data, soup
