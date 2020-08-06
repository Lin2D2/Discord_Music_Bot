import discord
import datetime
import time


def chess_board_embed(self, message):
    embed = discord.Embed(
        title=f'Chess {self.chess.player1} vs {self.chess.player2}', colour=discord.Colour(0xdbff),
        description=f'''It's {f'**{self.chess.player1}**' if self.chess.board.turn else f'**{self.chess.player2}**'} turn.
    ```        a b c d e f g h 
        ----------------
    1 | {self.chess.newBoard[0][0]} {self.chess.newBoard[0][1]} {self.chess.newBoard[0][2]} {self.chess.newBoard[0][3]} {self.chess.newBoard[0][4]} {self.chess.newBoard[0][5]} {self.chess.newBoard[0][6]} {self.chess.newBoard[0][7]}
    2 | {self.chess.newBoard[1][0]} {self.chess.newBoard[1][1]} {self.chess.newBoard[1][2]} {self.chess.newBoard[1][3]} {self.chess.newBoard[1][4]} {self.chess.newBoard[1][5]} {self.chess.newBoard[1][6]} {self.chess.newBoard[1][7]}
    3 | {self.chess.newBoard[2][0]} {self.chess.newBoard[2][1]} {self.chess.newBoard[2][2]} {self.chess.newBoard[2][3]} {self.chess.newBoard[2][4]} {self.chess.newBoard[2][5]} {self.chess.newBoard[2][6]} {self.chess.newBoard[2][7]}
    4 | {self.chess.newBoard[3][0]} {self.chess.newBoard[3][1]} {self.chess.newBoard[3][2]} {self.chess.newBoard[3][3]} {self.chess.newBoard[3][4]} {self.chess.newBoard[3][5]} {self.chess.newBoard[3][6]} {self.chess.newBoard[3][7]}
    5 | {self.chess.newBoard[4][0]} {self.chess.newBoard[4][1]} {self.chess.newBoard[4][2]} {self.chess.newBoard[4][3]} {self.chess.newBoard[4][4]} {self.chess.newBoard[4][5]} {self.chess.newBoard[4][6]} {self.chess.newBoard[4][7]}
    6 | {self.chess.newBoard[5][0]} {self.chess.newBoard[5][1]} {self.chess.newBoard[5][2]} {self.chess.newBoard[5][3]} {self.chess.newBoard[5][4]} {self.chess.newBoard[5][5]} {self.chess.newBoard[5][6]} {self.chess.newBoard[5][7]}
    7 | {self.chess.newBoard[6][0]} {self.chess.newBoard[6][1]} {self.chess.newBoard[6][2]} {self.chess.newBoard[6][3]} {self.chess.newBoard[6][4]} {self.chess.newBoard[6][5]} {self.chess.newBoard[6][6]} {self.chess.newBoard[6][7]}
    8 | {self.chess.newBoard[7][0]} {self.chess.newBoard[7][1]} {self.chess.newBoard[7][2]} {self.chess.newBoard[7][3]} {self.chess.newBoard[7][4]} {self.chess.newBoard[7][5]} {self.chess.newBoard[7][6]} {self.chess.newBoard[7][7]}```
''',
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))

    embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def chess_message_embed(self, titel, description, color=0xdbff):
    embed = discord.Embed(title=titel, colour=discord.Colour(color), description=description)
    # removed from above. timestamp=datetime.datetime.utcfromtimestamp(int(time.time()))
    # embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed


def play_track_embed(self, title, message):
    embed = discord.Embed(
        title=title, colour=discord.Colour(0x5cff00), url="https://discordapp.com",
        description=f'playing {title} in {message.author.voice.channel}',
        timestamp=datetime.datetime.now().utcfromtimestamp(int(time.time())))
    if not str(message.content).find("playlist") == -1:
        embed.set_thumbnail(url=self.current_playlist[self.playlist_i]["image"])
    else:
        try:
            embed.set_thumbnail(url=self.spotify.spotify_search(track=str(message.content).split("play ")[-1])["image"])
        except TypeError:
            try:
                embed.set_thumbnail(url=self.spotify.spotify_search(track=title)["image"])
            except TypeError:
                pass
    embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    return embed
