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
file_format = "opus"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': file_format,
        'preferredquality': '192',
    }],
    'outtmpl': str(os.getcwd())+slash+'music'+slash+'%(title)s.%(ext)s',
}


class Downloader:
    def __init__(self):
        pass

    @staticmethod
    def search(name):
        return yts.search(name, sMax=8, sType=["video"])

    @staticmethod
    def download(id, list_name, link=None):
        with yt.YoutubeDL(ydl_opts) as ydl:
            print("start ydl.extract_info")
            start = time.time()
            if link:
                result = ydl.extract_info("{}".format(link))
            else:
                result = ydl.extract_info("{}".format("https://www.youtube.com/watch?v=" + id))
            name = str(result.get("title", None)) + "." + str(file_format)
            print(time.time() - start)
            print(name)
            if name not in list_name:
                print("start ydl.download")
                start = time.time()
                if link:
                    ydl.download([link])
                else:
                    ydl.download(["https://www.youtube.com/watch?v=" + id])
                print(time.time() - start)
            return name
