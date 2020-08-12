import os
import sys
import json
import functools

import discord
import asyncio

from downloader import Downloader
from on_message import message as message_func
from spotify import Spotify
from play import play as play_func
from _chess import Chess
from embed import chess_board_embed, chess_message_embed, normal_message_embed

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
    print("os error")

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


class Bot(discord.Client):
    def __init__(self):
        super().__init__(loop=loop)
        self.client = None
        self.ws = None
        self.volume = 0.2
        self.downloader = Downloader()
        self.spotify = Spotify()
        self.last_song = ("", None)
        self.playlist_i = -1
        self.current_playlist_name = ""
        self.current_playlist = []
        self.next_song_ready = (False, None)
        self.skipping = False
        self.end_playlist_loop = False

        self.chess = Chess()

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
        self.client = client
        self.ws._keep_alive.name = 'Gateway keep alive'
        # await discord.Guild.fetch_member(self, client.user.id)

    async def loop_playlist(self):
        while True:
            if self.end_playlist_loop:
                self.end_playlist_loop = True
                break
            if self.next_song_ready[0]:
                if not self.voice_clients[0].is_playing():
                    print(self.next_song_ready)
                    message = self.next_song_ready[1]
                    await self.play_from_playlist(message)
                    await asyncio.sleep(0.25)
                    self.next_song_ready = (False, None)
                else:
                    await asyncio.sleep(0.25)
            else:
                await asyncio.sleep(0.25)

    @staticmethod
    async def add_playlist(playlist_name, items):
        with open(f"playlist/{playlist_name}", "w") as playlist:
            json.dump(items, playlist)

    @staticmethod
    async def get_playlists():
        return os.listdir("playlist")

    @staticmethod
    async def add_to_playlist(playlist_name, item):
        with open(f"playlist/{playlist_name}", "w") as playlist:
            items = json.load(playlist)
            json.dump(items.append(item), playlist)

    @staticmethod
    async def get_content_from_playlist(playlist_name):
        with open(f"playlist/{playlist_name}", "r") as playlist:
            items = json.load(playlist)
        return items

    async def make_random_playlist(self):
        # TODO fix!!!
        files_dates = [e for e in os.listdir("music")]
        print(files_dates)
        items = [self.spotify.spotify_search(track=str(e).split(".")[0]) for e in files_dates]
        print(items)
        with open(f"playlist/random", "w+") as playlist:
            json.dump(items, playlist)

    async def on_message(self, message):
        if message.author == client.user:
            return
        await message_func(self, message, client, prefix)

    async def join(self, author):
        channel = author.voice.channel
        await channel.connect()
        self.voice_clients[0].is_connected()
        await self.ws.voice_state(channel.guild.id, channel.id, False, True)

    async def move_to(self, channel):
        await self.voice_clients[0].move_to(channel)

    async def leave(self):
        await self.voice_clients[0].disconnect()

    def my_after(self, error):
        async def ready():
            self.next_song_ready = (True, None)
            print(f'next song ready triggered: {self.next_song_ready[0]}')
            if self.current_playlist == []:
                print(self.last_song)
                await self.play(self.last_song[0], self.last_song[1], autoloop=True)

        coro = ready()
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result()
        except:
            print(f'error: {error}')

    async def play(self, search, message):
        print("starting play function")
        await play_func(self, search, message, after=self.my_after)

    async def setup_for_playing_playlist(self):
        self.playlist_i = -1
        self.next_song_ready = (False, None)
        self.loop.create_task(self.loop_playlist())

    async def play_from_playlist(self, message, playlist_name=None):
        if self.playlist_i > len(self.current_playlist):
            await message.channel.send(
                f'Playlist ended {self.current_playlist_name} in {str(message.author.voice.channel)} playing from start'
            )
            self.playlist_i = 0
        print("start play function")
        print(f'current playlist {self.current_playlist_name}')
        if not playlist_name:
            if not self.current_playlist_name == "":
                playlist_name = self.current_playlist_name
            else:
                await self.stop()
        if self.current_playlist_name != playlist_name:
            self.current_playlist = await self.get_content_from_playlist(playlist_name)
            self.current_playlist_name = playlist_name
        self.playlist_i += 1
        await play_func(
            self,
            f'{self.current_playlist[self.playlist_i]["track"]} {self.current_playlist[self.playlist_i]["artists"][0]}',
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

    async def pause(self):
        self.voice_clients[0].pause()

    async def resume(self):
        self.voice_clients[0].resume()

    async def stop(self):
        self.voice_clients[0].stop()

    async def create_playlist_from_spotify(self, name, message):
        print(name + message)
        tracks = self.spotify.get_playlist_content(self.spotify.spotify_search(playlist=message)["uri"])
        await self.add_playlist(name, tracks)

    async def create_playlist_from_spotify_uri(self, name, message):
        print(name + message)
        tracks = self.spotify.get_playlist_content(message)
        await self.add_playlist(name, tracks)
        print("Done with playlist creation")


client = Bot()
client.run(TOKEN)
