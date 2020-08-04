import discord


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
        elif message.content.startswith(prefix + "play"):
            await self.play(
                str(message.content).split(
                    prefix + "play",
                    maxsplit=1)[-1].strip(" "),
                message
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