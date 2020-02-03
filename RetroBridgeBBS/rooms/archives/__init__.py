import os, pathlib
import requests
import logging
import RetroBridgeBBS.rooms as rooms
import RetroBridgeBBS.file_transfer as transfer

class Room(rooms.Room):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    archive_name = 'archive'    # used in filepath, so no weird characters

    def massage_download_url(self, dl_url, file_dict=None):
        return

    def get_file_from_archive(self, file_metadata=None, send_over_modem=True):
        dl_url  = file_metadata['url']
        dl_file = file_metadata['name']
        self.terminal.writeln(f"Starting DL of {dl_file}")
        #self.terminal.newline()
        #breakpoint()
        #full_url = dl_url.replace("/sites", "http://mirror.macintosharchive.org")
        full_url = self.massage_download_url(dl_url, file_metadata=file_metadata)
        myfile = requests.get(full_url)
        #saved_dl = f"/tmp/{dl_file}"
        local_save_dir = os.path.join(self.bbs.archive_downloads_path, self.archive_name)
        pathlib.Path(local_save_dir).mkdir(parents=True, exist_ok=True)
        saved_dl = os.path.join(local_save_dir, f"{dl_file}")
        open(saved_dl, 'wb').write(myfile.content)
        try:
            transfer.send_file(self.user_session, saved_dl)
        except:
            logging.info("Skipped X/Y/ZModem transfer because terminal doesn't support it")
            self.terminal.writeln()
            self.terminal.writeln("Skipped X/Y/ZModem transfer because terminal doesn't support it")
            self.terminal.writeln()
