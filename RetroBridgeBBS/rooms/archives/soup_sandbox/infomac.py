import re, os
import logging

import requests
from bs4 import BeautifulSoup
import pdb

"""
This is just a test script to work out scraping in ipythong
"""

class foo(object):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

self = foo()

url = 'http://mirror.macintosharchive.org/archive.info-mac.org/'
url = 'http://mirror.macintosharchive.org/archive.info-mac.org/_Game/'

page = requests.get(url, headers={'User-Agent': self.USER_AGENT})
# html.parser has issues correctly parsing macintoshgarden div tags.
#soup = BeautifulSoup(page.content, 'html.parser')
#soup = BeautifulSoup(page.content, 'html5lib')
soup = BeautifulSoup(page.content, 'lxml')

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

#print(ignored_links)
#print("------------")
#print(abstract_links)
#print("------------")
#print(sub_category_links)
#print("------------")


# descr = soup.findAll("div", {"class": "descr"})
# descr_rows = soup.findAll("tr")
# 
# # Extract Meta Data
# meta_data = dict()
# for row in descr_rows[1:]:      #first row has rating info, and we handle it after this loop
#     table_cells = row.findAll("td")
#     cell_name = table_cells[0].text
#     if cell_name.endswith(':'):         # Should be all of them, but just in case.
#         cell_name = cell_name[:-1]
#     if cell_name == 'Category':
#         cell_info = table_cells[1].find("a").attrs['href']
#     else:
#         cell_info = table_cells[1].text
#         cell_info = " ".join(cell_info.split(sep=None))     # Get rid of tabs, newlines and excessive whitespace
#     if len(cell_info) > 0:
#         meta_data[cell_name] = cell_info
# 
# 
# meta_data['description'] = soup.find("p").text
# if len(meta_data['description']) > 255:
#     meta_data['description'] = meta_data['description'][0:255] + '...'
# 
# meta_data['page_name'] = soup.find('h1').text
# 
# DL_divs = soup.find("div", {"class":"descr"}).findAll("div", {"class": "note download"})
# #DL_divs = soup.findAll("div", {"class": "note download"})
# 
# download_links = []
# for div in DL_divs:
#     file_dict = {}
# 
#     # <a href="/sites/macintoshgarden.org/files/games/mazewarsplus.zip">www</a>
#     href = div.find('a')
#     _url = href.attrs['href']
#     _name = _url.split('/')[-1]
#     file_dict['url'] = _url
#     file_dict['name'] = _name
# 
#     # <small>mazewarsplus.zip <i>(1.61 MB</i>)</small>
#     _size = " ".join(div.findAll('small')[-2].text.split()[1:])[1:-1]
#     file_dict['size'] = _size
# 
#     # compatibility text is after last <br>
#     _compat = ''.join(div.findAll('br')[-1].next_siblings)
#     # strip tabs, newlines and extraspace
#     _compat = " ".join(_compat.split(sep=None))
#     _compat = _compat.replace("For ", "")
#     _compat = _compat.replace("System ", "")
#     system_list = _compat.split('-')
#     condensed = system_list[0] + '-' + system_list[-1]
#     file_dict['compatibility'] = "System " + condensed
# 
#     download_links.append(file_dict)
# 
# #return download_links, meta_data, soup
