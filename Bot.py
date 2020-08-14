import os
import sys
import json
import logging
import random

import discord
import asyncio

from downloader import Downloader
from on_message import message as message_func
from spotify import Spotify
from play import play as play_func
from _chess import Chess
from embed import chess_board_embed, chess_message_embed, search_track_embed

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix = "?"
loop = asyncio.get_event_loop()

if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"

try:
    if "music" not in os.listdir(os.getcwd()):
        os.mkdir("music")
    if "playlist" not in os.listdir(os.getcwd()):
        os.mkdir("playlist")
    else:
        pass
except OSError:
    logging.error("os error")


# TODO make separated function to delete old songs

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

def create_logger():
    logger = logging.getLogger("Discord_Bot_Logger")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s: :%(levelname)s: %(message)s",
                                  "%Y-%m-%d %H:%M:%S")

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


class Bot(discord.Client):
    def __init__(self):
        super().__init__(loop=loop)
        self.logger = create_logger()
        self.client = None
        self.ws = None
        self.volume = 0.2
        self.downloader = Downloader(self.logger)
        self.spotify = Spotify(self.logger)
        self.last_song = None
        self.playlist_i = -1
        self.shuffel = None
        self.current_playlist_name = None
        self.current_playlist = None
        self.next_song_ready = (False, None)
        self.skipping = False
        self.end_playlist_loop = False
        self.active_search = None
        self.last_message = None

        self.chess = Chess()

    async def on_ready(self):
        self.logger.info(f'{client.user} has connected to Discord!')
        self.client = client
        self.ws._keep_alive.name = 'Gateway keep alive'
        # await discord.Guild.fetch_member(self, client.user.id)

    async def loop_playlist(self):
        while True:
            if self.end_playlist_loop:
                self.end_playlist_loop = True
                break
            if self.next_song_ready[0]:
                self.logger.debug("next song ready")
                if not self.voice_clients[0].is_playing():
                    self.logger.debug(self.next_song_ready)
                    message = self.next_song_ready[1]
                    await self.play_from_playlist(message)
                    self.logger.debug("setting next song ready False")
                    self.next_song_ready = (False, None)
                else:
                    await asyncio.sleep(0.25)
            else:
                await asyncio.sleep(0.25)

    @staticmethod
    async def add_playlist(playlist_name, items):
        with open(f'playlist{slash}{str(playlist_name).strip(" ")}.json', "w") as playlist:
            json.dump(items, playlist)

    @staticmethod
    async def get_playlists():
        return os.listdir("playlist")

    @staticmethod
    async def add_to_playlist(playlist_name, item):
        with open(f'playlist{slash}{str(playlist_name).strip(" ")}', "w") as playlist:
            items = json.load(playlist)
            json.dump(items.append(item), playlist)

    @staticmethod
    async def get_content_from_playlist(playlist_name):
        with open(f'playlist{slash}{str(playlist_name).strip(" ")}.json', "r") as playlist:
            items = json.load(playlist)
        return items

    async def shuffel_playlist(self):
        numbers = []
        for i in self.current_playlist["tracks"]:
            numbers.append(random.randrange(0, len(self.current_playlist["tracks"])))
        numbers = list(dict.fromkeys(numbers))
        range_list = range(0, len(self.current_playlist["tracks"]))
        for e in range_list:
            if e not in numbers:
                numbers.append(int(e))
        self.shuffel = numbers

    async def make_random_playlist(self):
        # TODO fix!!!
        files_dates = [e for e in os.listdir("music")]
        self.logger.debug(files_dates)
        items = [self.spotify.spotify_search(track=str(e).split(".")[0]) for e in files_dates]
        self.logger.debug(items)
        with open(f"playlist{slash}random", "w+") as playlist:
            json.dump(items, playlist)

    async def on_message(self, message):
        if not self.active_search:
            if message.author == client.user:
                return
            self.last_message = message
            await message_func(self, message, client, prefix)
        else:
            if message.author == client.user:
                return
            if str(message.content) != "cancel":
                await play_func(self, self.active_search[int(message.content) - 1]["title"], message)
            self.active_search = None

    async def join(self, author):
        self.logger.info("joined")
        channel = author.voice.channel
        await channel.connect()
        self.voice_clients[0].is_connected()
        await self.ws.voice_state(channel.guild.id, channel.id, False, True)

    async def move_to(self, channel):
        await self.voice_clients[0].move_to(channel)

    async def leave(self):
        await self.voice_clients[0].disconnect()
        self.logger.info("left")

    async def search(self, search, message):
        search_result = self.downloader.alt_search(search)
        self.active_search = search_result
        await message.channel.send(embed=search_track_embed(self, search, search_result))

    def my_after(self, error):
        async def ready():
            self.next_song_ready = (True, None)
            self.logger.debug(f'next song ready triggered: {self.next_song_ready[0]}')
            if self.current_playlist is None:
                self.logger.debug(self.last_song[0])
                await self.play(self.last_song[0], self.last_song[1], autoloop=True)
            else:
                self.logger.debug(f'current_playlist {self.current_playlist_name} content: {self.current_playlist}')

        coro = ready()
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result()
        except OSError:
            self.logger.error(f'error: {error}')

    async def play(self, search, message, autoloop=False):
        self.logger.debug("starting play {}".format(search))
        await play_func(self, search, message, after=self.my_after, autoloop=autoloop)

    async def setup_for_playing_playlist(self):
        self.playlist_i = -1
        self.next_song_ready = (False, None)
        self.shuffel = None
        self.loop.create_task(self.loop_playlist())

    # TODO problem when playing new playlist playing after normal play
    async def play_from_playlist(self, message, playlist_name=None):
        if self.current_playlist:
            self.logger.debug(
                f'crrent playlist i {self.playlist_i} len playlist {len(self.current_playlist["tracks"])}')
            if self.playlist_i == len(self.current_playlist["tracks"]):
                await message.channel.send(
                    f'Playlist ended {self.current_playlist_name} in {str(message.author.voice.channel)} playing from start'
                )
                self.playlist_i = -1
        self.logger.debug("start play from playlist function")
        self.logger.info(f'current playlist {self.current_playlist_name}')
        if not playlist_name:
            if not self.current_playlist_name:
                await self.stop()
        if self.current_playlist_name != playlist_name or not self.current_playlist_name:
            if playlist_name:
                try:
                    self.current_playlist = await self.get_content_from_playlist(playlist_name)
                except FileNotFoundError:
                    self.logger.debug(playlist_name)
                    self.logger.error("File Not Found!!!")
                self.current_playlist_name = playlist_name
        self.logger.info("shuffeling")
        if not self.shuffel:
            await self.shuffel_playlist()
            # TODO add shuffel call in on_message
        self.logger.info(f'shuffel: {self.shuffel}')
        if self.playlist_i == -1:
            await message.channel.send(f'Playing https://open.spotify.com/playlist/{self.current_playlist["uri"]}')
        self.playlist_i += 1
        await play_func(
            self,
            f'{self.current_playlist["tracks"][self.shuffel[self.playlist_i]]["track"]} {self.current_playlist["tracks"][self.shuffel[self.playlist_i]]["artists"][0]}'
            if self.shuffel else
            f'{self.current_playlist["tracks"][self.playlist_i]["track"]} {self.current_playlist["tracks"][self.playlist_i]["artists"][0]}',
            message,
            after=self.my_after
        )

    async def play_chess(self, message):
        # TODO init of this need 2 players to accept to start the game
        if not self.chess.player1:
            self.chess.player1 = message.author
            await message.channel.send(
                embed=chess_message_embed(self, f'{self.chess.player1} whats to begin a Chess Game',
                                          f'To enter just type: `?play chess`')
            )
        # elif not self.chess.player2 and message.author != self.chess.player1:
        elif not self.chess.player2:
            self.chess.player2 = message.author
            await message.channel.send(
                embed=chess_message_embed(
                    self, f'**{self.chess.player1}** begone a Chess Game',
                    f'**{message.author}** entered the Game and it will start now.\n'
                    f'White Player is **{self.chess.player1}** and Black Player is **{self.chess.player2}**.\n'
                    f'To make a move just type: `?move (your move, for example: b2b4)`'
                )
            )
            await self.play_chess(message)
        elif self.chess.player1 and self.chess.player2:
            await message.channel.send(embed=chess_board_embed(self, message))
        else:
            await message.channel.send(
                embed=chess_message_embed(self, "You need 2 Players for Chess you cant play with your self",
                                          f'To enter the game just type: `?play chess`. '
                                          f'In Game currently **{self.chess.player1}**'
                                          ),
                delete_after=30
            )

    # TODO implement skip incremt i and start playfromplaylist

    async def pause(self):
        self.voice_clients[0].pause()
        self.logger.info("paused")

    async def resume(self):
        self.voice_clients[0].resume()
        self.logger.info("resumed")

    async def stop(self):
        self.voice_clients[0].stop()
        self.logger.info("stopped")

    # TODO function to show avilable playlists

    async def create_playlist_from_spotify(self, name, message):
        self.logger.debug(name + message)
        tracks = self.spotify.get_playlist_content(self.spotify.spotify_search(playlist=message)["uri"])
        await self.add_playlist(name, tracks)
        # TODO send message when done

    async def create_playlist_from_spotify_uri(self, name, message):
        self.logger.debug(name + message)
        tracks = self.spotify.get_playlist_content(str(message).split(":")[-1])
        await self.add_playlist(name, tracks)
        self.logger.info("Done with playlist creation")

    async def create_playlist_from_spotify_link(self, name, message):
        self.logger.debug(name + message)
        tracks = self.spotify.get_playlist_content(str(message).split("/")[-1].split("?")[0])
        await self.add_playlist(name, tracks)
        self.logger.info("Done with playlist creation")


client = Bot()
client.run(TOKEN)
