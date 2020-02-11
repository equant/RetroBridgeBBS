
def sort_links(links):
    for link in links:
        for _p in ignore_url_patterns:
            _r = re.compile(_p)
            _m = _r.match(link.attrs['href'])
            if _m:
                ignored_links.append([link, _p])
                break
        for _p in ignore_text_patterns:
            _r = re.compile(_p)
            _m = _r.match(link.text)
            if _m:
                ignored_links.append([link, _p])
                break

        for _p in abstract_url_patterns:
            _r = re.compile(_p)
            _m = _r.match(link.attrs['href'])
            if _m:
                abstract_links.append([link, _p])
                break
        for _p in abstract_text_patterns:
            _r = re.compile(_p)
            _m = _r.match(link.text)
            if _m:
                abstract_links.append([link, _p])
                break
