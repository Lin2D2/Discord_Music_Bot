import os
import os
import sys
import time
import json

import discord
import asyncio

from downloader import Downloader
from on_message import message as message_func
from spotify import Spotify
from play import play as play_func
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix = "?"
loop = asyncio.get_event_loop()


if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"


# TODO make seperat fuction to delete old songs

# def creation_date(path_to_file):
#     if platform.system() == 'Windows':
#         return os.path.getctime(path_to_file)
#     else:
#         stat = os.stat(path_to_file)
#         try:
#             return stat.st_birthtime
#         except AttributeError:
#             # We're probably on Linux. No easy way to get creation dates here,
#             # so we'll settle for when its content was last modified.
#             return stat.st_mtime


class Bot(discord.Client):
    def __init__(self):
        super().__init__(loop=loop)
        self.volume = 0.12
        self.downloader = Downloader()
        self.spotify = Spotify()

    @staticmethod
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        # await discord.Guild.fetch_member(self, client.user.id)

    @staticmethod
    async def add_playlist(playlist_name, items):
        with open(f"playlist/{playlist_name}", "w+") as playlist:
            json.dump(items, playlist)

    @staticmethod
    async def get_playlists():
        return os.listdir("playlist")

    @staticmethod
    async def add_to_playlist(playlist_name, item):
        with open(f"playlist/{playlist_name}", "w+") as playlist:
            items = json.load(playlist)
            json.dump(items.append(item), playlist)

    @staticmethod
    async def get_content_from_playlist(playlist_name):
        with open(f"playlist/{playlist_name}", "w+") as playlist:
            items = json.load(playlist)
        return items

    async def on_message(self, message):
        if message.author == client.user:
            return
        await message_func(self, message, client, prefix)

    async def join(self, author):
        channel = author.voice.channel
        await channel.connect()
        self.voice_clients[0].is_connected()

    async def move_to(self, channel):
        await self.voice_clients[0].move_to(channel)

    async def leave(self):
        await self.voice_clients[0].disconnect()

    async def play(self, serach, message, self_loop=False):
        print("start play function")
        play_func(self, serach, message)

    async def pause(self):
        self.voice_clients[0].pause()

    async def resume(self):
        self.voice_clients[0].resume()

    async def stop(self):
        self.voice_clients[0].stop()


client = Bot()
client.run(TOKEN)
