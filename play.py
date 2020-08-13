import time
import os
import sys
import subprocess
from discord import FFmpegPCMAudio, PCMVolumeTransformer, AudioSource
from embed import play_track_embed


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
        self.logger.debug(f'search: {search}')
        name, vid = self.downloader.download(search, files_dates)
        self.logger.info(f'song playing: {name}')
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
            self.logger.debug("stop")
            await self.stop()
        self.voice_clients[0].play(_source, after=after)
        # await message.channel.send(
        #     "playing " + name.strip(".webm") + " in  " + str(message.author.voice.channel)
        # )
        try:
            await message.channel.send(embed=play_track_embed(self, str(name).split(".")[0],
                                                              message, vid, autoloop=autoloop))
        except AttributeError:
            await self.last_song[1].channel.send(embed=play_track_embed(self, str(name).split(".")[0],
                                                                        self.last_song[1], vid, autoloop=autoloop))
        if self.last_song:
            self.last_song = (search, self.last_song[1])
        else:
            self.last_song = (search, message)
    else:
        await self.join(message.author)
        await self.play(search, message)
