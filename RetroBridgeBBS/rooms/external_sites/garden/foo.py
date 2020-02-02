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
# html.parser has issues correctly parsing macintoshgarden div tags.
#soup = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(page.content, 'html5lib')

# Extract Table with ratings, year, and download links
T = soup.find("table")
table_rows = T.find_all("tr")

descr = soup.findAll("div", {"class": "descr"})
descr_rows = soup.findAll("tr")

# Extract Meta Data
meta_data = dict()
for row in descr_rows[1:]:      #first row has rating info, and we handle it after this loop
    table_cells = row.findAll("td")
    cell_name = table_cells[0].text
    if cell_name.endswith(':'):         # Should be all of them, but just in case.
        cell_name = cell_name[:-1]
    if cell_name == 'Category':
        cell_info = table_cells[1].find("a").attrs['href']
    else:
        cell_info = table_cells[1].text
        cell_info = " ".join(cell_info.split(sep=None))     # Get rid of tabs, newlines and excessive whitespace
    if len(cell_info) > 0:
        meta_data[cell_name] = cell_info


meta_data['rating'] = float(table_rows[0].find_all('div')[-1].find_all('span')[2].find('span').text)

meta_data['description'] = soup.find("p").text
if len(meta_data['description']) > 255:
    meta_data['description'] = meta_data['description'][0:255] + '...'

DL_divs = soup.findAll("div", {"class": "note download"})

download_links = []
for div in DL_divs:
    href = div.find('a')
    _url = href.attrs['href']
    _name = _url.split('/')[-1]
    download_links.append([_name, _url])

#return download_links, meta_data, soup
