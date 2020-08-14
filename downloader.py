from __future__ import unicode_literals
from dotenv import load_dotenv
import youtube_dl as yt
import yt_search
import sys
import os
import time
from youtube_search import YoutubeSearch


if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"

# load_dotenv()
# API_KEY = os.getenv('YOUTUBE_API_KEY')
#
# yts = yt_search.build(API_KEY)
file_format = "webm"

ydl_opts = {
    'format': 'bestaudio/best',
    'audioformat': file_format,
    'noplaylist': True,
    'nocheckcertificate': True,
    'outtmpl': str(os.getcwd())+slash+'music'+slash+'%(title)s.%(ext)s',
}


# def common_member(first, second):
#     first_set = set(first)
#     second_set = set(second)
#     if len(first_set.intersection(second_set)) > 0:
#         return True
#     return False

# TODO find better way maybe just do postprocessing to change file type to webm
def find_format(name):
    for file in os.listdir(f'music'):
        if file.split(".")[0] == name:
            return file
    name = name.replace("|", "_")
    return f'{name}.{file_format}'


class Downloader:
    def __init__(self, logger):
        self.logger = logger
    #
    # @staticmethod
    # def search(name):
    #     return yts.search(name, sMax=8, sType=["video"])

    @staticmethod
    def alt_search(name):
        return YoutubeSearch(name, max_results=8).to_dict()

    @staticmethod
    def info_extract(vid=None, link=None):
        if vid:
            with yt.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info("{}".format("https://www.youtube.com/watch?v=" + vid))
        elif link:
            with yt.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info("{}".format(link))

    # TODO name cant contain | its changed to _ !!!
    def download(self, search, list_name, link=None):
        search_result = self.alt_search(search)
        vid = search_result[0]["id"]
        self.logger.debug(f'video id: {vid}')
        name = find_format(str(search_result[0]["title"]))
        self.logger.debug(f'name in downloader: {name}')
        if str(search_result[0]["title"]) not in ["".join(str(e).split(".")[:-1]) for e in list_name]:
            with yt.YoutubeDL(ydl_opts) as ydl:
                self.logger.debug("start ydl.extract_info")
                self.logger.debug(name)
                if name not in list_name:
                    self.logger.info("start ydl.download")
                    if link:
                        ydl.download([link])
                    else:
                        ydl.download(["https://www.youtube.com/watch?v=" + vid])
                name = find_format(str(search_result[0]["title"]))
                self.logger.debug(f'song name: {name}')
                return name, vid
        else:
            self.logger.info("already local skipping download")
            self.logger.debug(f'song name: {name}')
            return name, vid
