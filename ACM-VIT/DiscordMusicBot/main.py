from asyncio import Queue

from discord import FFmpegPCMAudio as ffm
from discord.ext import commands

from functions import play_next, song_url, tube_dl

API_KEY = "ACM-VITxD"
bot = commands.Bot(command_prefix=".")
token = "OTQ1NzgwNjUxNjUzNzM4NTE2.YhVI3w.EtZH8RdQtFsayqYSMzeqUuJ3vtk"
queue = Queue()
number = 0


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.guild.voice_client in bot.voice_clients:
        return await ctx.send(f"Already joined voice chat in {channel}")
    else:
        await channel.connect()
        return await ctx.send(f"Joined {channel} voice chat successfully")


@bot.command()
async def leave(ctx):
    if not ctx.guild.voice_client in bot.voice_clients:
        return await ctx.send("Bot is not in voice chat")
    else:
        await ctx.voice_client.disconnect()
        global number
        number = 0
        channel = ctx.author.voice.channel
        queue._queue.clear()
        await ctx.send(f"Left {channel} voice chat successfully")


@bot.command()
async def play(ctx, *, args):
    if not ctx.guild.voice_client in bot.voice_clients:
        return await ctx.send(
            "Make the bot join the voice chat first using .join"
        )
    else:
        vc = ctx.voice_client
        link, v_id = song_url(args)
        if vc.is_playing():
            await queue.put(args)
            global number
            number += 1
            return await ctx.send(
                f"https://api.vegetaxd.me/{API_KEY}/thumb/queued/{v_id}"
            )
        else:
            song = tube_dl(link)
            api = f"https://api.vegetaxd.me/{API_KEY}/thumb/played/{v_id}"
            await ctx.send(api)
            return vc.play(ffm(song))


@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if not vc.is_playing():
        return await ctx.send("Nothing is playing")
    else:
        await ctx.send("Paused Successfully")
        vc.pause()


@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc.is_playing():
        return await ctx.send("Already Playing!")
    else:
        await ctx.send("Resumed Successfully")
        vc.resume()


@bot.command()
async def skip(ctx):
    vc = ctx.voice_client
    if not vc.is_playing():
        return await ctx.send("Nothing is Playing to skip")
    if queue.empty():
        await ctx.send("No More songs In Queue!\nLeaving Video Chat!")
        return await vc.disconnect()
    else:
        stuff = await queue.get()
        global number
        number -= 1
        link, v_id = song_url(stuff)
        song = tube_dl(link)
        api = f"https://api.vegetaxd.me/{API_KEY}/thumb/played/{v_id}"
        await ctx.send(api)
        vc.pause()
        return vc.play(ffm(song))


bot.run(token)
