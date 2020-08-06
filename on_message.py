import discord
from embed import chess_board_embed, chess_message_embed, play_track_embed


async def message(self, message, client, prefix):
    if message.content.startswith(prefix):
        # await message.channel.send("message from " + str(message.author) + " contains " + str(message.content))
        if message.content == prefix + "join":
            await message.channel.send(
                "joined " + str(message.author.voice.channel),
                delete_after=20
            )
            await self.join(message.author)

        elif message.content == prefix + "stop":
            await message.channel.send(
                "stop song in " + str(message.author.voice.channel),
                delete_after=20
            )
            await self.pause()
        elif message.content == prefix + "pause":
            await message.channel.send(
                "stop song in " + str(message.author.voice.channel),
                delete_after=20
            )
            await self.pause()
        elif message.content == prefix + "resume":
            await message.channel.send(
                "resume song in " + str(message.author.voice.channel),
                delete_after=20
            )
            await self.resume()
        elif str(message.content).find(prefix + "read") != -1:
            await message.channel.send(
                str(message.content).split(
                    prefix + "read",
                    maxsplit=1)[-1],
                tts=True,
                delete_after=10
            )
        elif message.content == prefix + "info":
            await message.channel.send(discord.AppInfo)
        elif message.content == prefix + "leave":
            await message.channel.send(
                str(client.user) + " left " + str(message.author.voice.channel),
                delete_after=10
            )
            await self.leave()
        elif message.content.startswith(prefix + "move"):
            if self.chess.player1 and self.chess.player2:
                if (self.chess.board.turn and self.chess.player1 == message.author or
                        not self.chess.board.turn and self.chess.player2 == message.author):
                    move = str(message.content).split("move ")[-1]
                    return_move = self.chess.make_move(move)
                    if return_move:
                        await message.channel.send(
                            embed=chess_message_embed(self, "Moved", f'moved from {move[:2]} to {move[2:]}'),
                            delete_after=15
                        )
                        if type(return_move) != bool:
                            await message.channel.send(
                                embed=chess_message_embed(self, return_move[0], return_move[1]),
                                delete_after=15
                            )
                    else:
                        move = str(message.content).split("move ")[-1]
                        await message.channel.send(
                            embed=chess_message_embed(self, "Invalid", f'{move} is not an Valid move',
                                                      color=0xff0004),
                            delete_after=10
                        )
                    await self.play_chess(message)
                else:
                    await message.channel.send(
                        embed=chess_message_embed(self, "Not Your Turn",
                                                  "It's not your Turn wait until your opponent is done",
                                                  color=0xff0004),
                        delete_after=15
                    )
            else:
                await message.channel.send(
                    embed=chess_message_embed(self, "Invalid",
                                              "Invalid request there is no active Chess Game\n"
                                              "to start one type: `?play chess`",
                                              color=0xff0004),
                    delete_after=20
                )
        elif message.content.startswith(prefix + "play chess"):
            await self.play_chess(message)
        elif message.content.startswith(prefix + "play playlist"):
            await self.setup_for_playing_playlist()
            await self.play_from_playlist(
                message, str(message.content).split("play playlist ")[-1]
            )
        elif message.content.startswith(prefix + "play"):
            await self.play(
                str(message.content).split(
                    prefix + "play ",
                    maxsplit=1)[-1],
                message
            )
        elif message.content.startswith(prefix + "skip"):
            await self.play_from_playlist(message)
        elif message.content.startswith(prefix + "create "):
            if str(message.content).find("uri ") != -1:
                await self.create_playlist_from_spotify_uri(
                    str(message.content).split("create ")[1].split("from uri ")[0],
                    str(message.content).split("from uri ")[-1]
                )
            else:
                await self.create_playlist_from_spotify(
                    str(message.content).split("create ")[-1], str(message.content).split("create ")[-1]
                )
        elif str(message.content).find(prefix + "volume") != -1:
            value = str(message.content).split(prefix + "volume")[-1]
            value = float(value.strip(" "))
            if type(value) == float:
                if 1 >= value > 0:
                    self.volume = value
                    await message.channel.send(
                        "volume set to " + str(value),
                        delete_after=20
                    )
                else:
                    await message.channel.send(
                        "volume must be smaller then or equal to 1",
                        delete_after=10
                    )
            else:
                await message.channel.send(
                    "volume must be an Number smaller then or equal to 1",
                    delete_after=10
                )