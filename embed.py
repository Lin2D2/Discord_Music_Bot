import discord
import datetime
import time
from PIL import Image
import requests
from io import BytesIO


def chess_board_embed(self, message):
    endline = "\n"
    embed = discord.Embed(
        title=f'Chess {self.chess.player1} vs {self.chess.player2}', colour=discord.Colour(0xdbff),
        description=f'''It's {f'**{self.chess.player1}**' if self.chess.board.turn else f'**{self.chess.player2}**'} turn.
```{endline.join([" ".join(e) for e in self.chess.newBoard])}```''',
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))

    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def new_chess_board_embed(self, message):

    embed = discord.Embed(
        title=f'Chess {self.chess.player1} vs {self.chess.player2}', colour=discord.Colour(0xdbff),
        description=f'''It's {f'**{self.chess.player1}**' if self.chess.board.turn else f'**{self.chess.player2}**'} turn.
''',
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))

    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def chess_message_embed(self, title, description, color=0xdbff):
    embed = discord.Embed(title=title, colour=discord.Colour(color), description=description)
    # removed from above. timestamp=datetime.datetime.utcfromtimestamp(int(time.time()))
    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def normal_message_embed(self, title, message, color=0x4a4a4a):
    embed = discord.Embed(
        title=title, colour=discord.Colour(color),
        description=message,
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))
    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def play_track_embed(self, title, message, vid, autoloop=None):
    if not self:
        print("self was None in play_track_embed")
        return
    embed = discord.Embed(
        title="Auto loop" if autoloop else title, colour=discord.Colour(0x5cff00),
        description=f'playing {title} in {message.author.voice.channel}',
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))
    try:
        embed.set_thumbnail(url=self.current_playlist["tracks"][self.shuffel[self.playlist_i]]["image"]
                            if self.shuffel else
                            self.current_playlist["tracks"][self.playlist_i]["image"])
    except TypeError:
        try:
            embed.set_thumbnail(url=self.spotify.spotify_search(
                track=str(message.content).split("?play ", maxsplit=1)[-1])["image"])
        except TypeError:
            try:
                embed.set_thumbnail(url=self.spotify.spotify_search(track=title)["image"])
            except TypeError:
                try:
                    print("used youtube thumbnail")
                    # TODO find a way to show sized image instead of the 16:9
                    # response = requests.get(self.downloader.info_extract(vid=vid)["thumbnails"][1]["url"])
                    # img = Image.open(BytesIO(response.content))
                    # img.thumbnail((400, 400))
                    # file = discord.File(img, filename="thumbnail.png")
                    embed.set_thumbnail(url=self.downloader.info_extract(vid=vid)["thumbnails"][1]["url"])
                except TypeError:
                    self.logger.error("No Idea what went wrong")
    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def search_track_embed(self, title, search):
    embed = discord.Embed(title=f'Search for {title}', colour=discord.Colour(0x9b9b9b),
                          description="Type a Number to select a song or `cancel` to quit",
                          timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))
    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    for item in search:
        embed.add_field(name=f'`{int(search.index(item))+1}`.',
                        value=f'[{item["title"]}](https://www.youtube.com/watch?v={item["id"]}) {item["duration"]}...',
                        inline=False)
    return embed
