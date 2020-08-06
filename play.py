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


async def play(self, serach, message, after=None, self_loop=False):
    print(f'starting play function serach:{serach} message:{message.content}')
    start = time.time()
    if len(self.voice_clients) > 0:
        boptions = "-nostdin"
        aoptions = "-vn"
        files_dates = []
        for e in os.listdir("music"):
            files_dates.append(e)
        name = self.downloader.download(serach, files_dates)
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
        self.voice_clients[0].play(_source, after=after)
        print("time of play function " + str(time.time() - start))
        # await message.channel.send(
        #     "playing " + name.strip(".webm") + " in  " + str(message.author.voice.channel)
        # )
        await message.channel.send(embed=play_track_embed(name.strip(".webm"), message))
    else:
        if not self_loop:
            print("try join")
            await self.join(message.author)
            await self.play(serach, message, self_loop=True)
        else:
            await message.channel.send("Failed!", delete_after=20)
