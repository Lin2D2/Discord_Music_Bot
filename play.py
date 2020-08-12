import time
import os
import sys
import subprocess
from discord import FFmpegPCMAudio, PCMVolumeTransformer, AudioSource
from embed import chess_board_embed, chess_message_embed, play_track_embed


if sys.platform == "win32":
    slash = "\\"
else:
    slash = "/"


class SourcePlaybackCounter(AudioSource):
    def __init__(self, source, progress=0):
        self._source = source
        self.progress = progress

    def read(self):
        res = self._source.read()
        if res:
            self.progress += 1
        return res

    def get_progress(self):
        return self.progress * 0.1

    def cleanup(self):
        self._source.cleanup()


async def play(self, search, message, after=None, autoloop=False):
    if len(self.voice_clients) > 0:
        boptions = "-nostdin"
        aoptions = "-vn"
        files_dates = []
        for e in os.listdir("music"):
            files_dates.append(e)
        print(f'search: {search}')
        name, vid = self.downloader.download(search, files_dates)
        _source = SourcePlaybackCounter(
            PCMVolumeTransformer(
                FFmpegPCMAudio(
                    "music" + slash + str(name),
                    before_options=boptions,
                    options=aoptions,
                    stderr=subprocess.PIPE
                ),
                self.volume
            )
        )
        if self.voice_clients[0].is_playing():
            print("stop")
            await self.stop()
        print("giving play call Here!")
        self.voice_clients[0].play(_source, after=after)
        print("time of play function " + str(time.time() - start))
        # await message.channel.send(
        #     "playing " + name.strip(".webm") + " in  " + str(message.author.voice.channel)
        # )
        await message.channel.send(embed=play_track_embed(self, name.strip(".webm"), message, vid, autoloop=autoloop))
        self.last_song = (search, message)
    else:
        if not self_loop:
            print("try join")
            await self.join(message.author)
            await self.play(search, message, self_loop=True)
        else:
            await message.channel.send("Failed!", delete_after=20)
