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


class Downloader:
    def __init__(self):
        pass
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

    def download(self, search, list_name, link=None):
        search_result = self.alt_search(search)
        vid = search_result[0]["id"]
        print(f'video id: {vid}')
        if str(search_result[0]["title"]) not in [str(e).split(".")[0] for e in list_name]:
            with yt.YoutubeDL(ydl_opts) as ydl:
                print("start ydl.extract_info")
                name = str(search_result[0]["title"]) + "." + str(file_format)
                print(name)
                if name not in list_name:
                    print("start ydl.download")
                    if link:
                        ydl.download([link])
                    else:
                        ydl.download(["https://www.youtube.com/watch?v=" + vid])
                return name, vid
        else:
            print("Video already local skipping download")
            return str(search_result[0]["title"]) + "." + file_format, vid
