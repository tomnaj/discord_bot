import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

if bot_token is None:
    raise ValueError("No bot token found.")
# Set up Discord bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configure yt_dlp and FFmpeg options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'default_search': 'ytsearch',  # This will search on YouTube
    'source_address': '0.0.0.0'  # Bind to IPv4
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Queue and loop flag
song_queue = []
is_looping = False

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_title(cls, title, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{title}", download=False))

        if 'entries' in data and data['entries']:
            info = data['entries'][0]
            return cls(discord.FFmpegPCMAudio(info['url'], **ffmpeg_options), data=info)

        return None

async def play_next(ctx):
    """Plays the next song in the queue if there is one."""
    if is_looping and song_queue:
        player = song_queue[0]  # Loop the current song
    elif song_queue:
        player = song_queue.pop(0)  # Pop the next song
    else:
        return  # Stop if the queue is empty and not looping

    ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop).result())
    await ctx.send(f"Now playing: {player.title}")

@bot.command(name="join")
async def join(ctx):
    """Bot joins the voice channel of the user who invoked the command."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You need to be in a voice channel first.")

@bot.command(name="play")
async def play(ctx, *, title: str):
    """Plays audio based on a search query."""
    if not ctx.voice_client:
        await join(ctx)  # Joins if not already in a channel

    async with ctx.typing():
        player = await YTDLSource.from_title(title, loop=bot.loop)
        if player:
            song_queue.append(player)
            await ctx.send(f"Added to queue: {player.title}")

            # Start playing if not currently playing
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
        else:
            await ctx.send("Could not find a track with that title. Please try another search term.")

@bot.command(name="queue")
async def queue(ctx):
    """Displays the current song queue."""
    if song_queue:
        queue_list = "\n".join(f"{i + 1}. {song.title}" for i, song in enumerate(song_queue))
        await ctx.send(f"Current Queue:\n{queue_list}")
    else:
        await ctx.send("The queue is empty.")

@bot.command(name="loop")
async def loop(ctx):
    """Toggles looping of the current song."""
    global is_looping
    is_looping = not is_looping
    status = "enabled" if is_looping else "disabled"
    await ctx.send(f"Looping has been {status}.")

@bot.command(name="pause")
async def pause(ctx):
    """Pauses the current audio."""
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Audio paused.")
    else:
        await ctx.send("No audio is currently playing.")

@bot.command(name="resume")
async def resume(ctx):
    """Resumes paused audio."""
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Audio resumed.")
    else:
        await ctx.send("Audio is not paused.")

@bot.command(name="stop")
async def stop(ctx):
    """Stops the audio and leaves the voice channel."""
    global song_queue
    if ctx.voice_client:
        song_queue.clear()
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped the audio and left the channel.")
    else:
        await ctx.send("I'm not connected to a voice channel.")

@bot.command(name='leave')
async def leave(ctx):
    """Forces the bot to leave the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel!")

# Run the bot with your bot token
bot.run(bot_token)
