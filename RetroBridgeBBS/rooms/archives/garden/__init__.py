import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.rooms.archives as archives

class Room(archives.Room):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    archive_id = 'macintoshgarden'
    archive_name = 'Macintosh Garden'
    
    def massage_download_url(self, dl_url, file_metadata=None):
        full_url = dl_url.replace("/sites", "http://mirror.macintosharchive.org")
        return full_url

    def __init__(self, user_session, url=None):
        if url is None:
            url = 'https://macintoshgarden.org/tracker'
        archives.Room.__init__(self, user_session, url)

