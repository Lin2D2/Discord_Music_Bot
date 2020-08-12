from __future__ import unicode_literals
from dotenv import load_dotenv
import youtube_dl as yt
import yt_search
import sys
import os
import time


if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

yts = yt_search.build(API_KEY)
file_format = "webm"

ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
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

    @staticmethod
    def search(name):
        return yts.search(name, sMax=8, sType=["video"])

    def download(self, search, list_name, link=None):
        search_result = self.search(search)
        vid = search_result.videoId[0]
        print(f'video id: {vid}')
        if str(search_result.title[0]) not in [str(e).split(".")[0] for e in list_name]:
            with yt.YoutubeDL(ydl_opts) as ydl:
                print("start ydl.extract_info")
                start = time.time()
                if link:
                    result = ydl.extract_info("{}".format(link))
                else:
                    result = ydl.extract_info("{}".format("https://www.youtube.com/watch?v=" + vid))
                name = str(result.get("title", None)) + "." + str(file_format)
                print(time.time() - start)
                print(name)
                if name not in list_name:
                    print("start ydl.download")
                    start = time.time()
                    if link:
                        ydl.download([link])
                    else:
                        ydl.download(["https://www.youtube.com/watch?v=" + vid])
                    print(time.time() - start)
                return name
        else:
            return str(search_result.title[0]) + "." + file_format
