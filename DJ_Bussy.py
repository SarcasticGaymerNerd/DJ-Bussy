import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp as youtube_dl
import asyncio
import os

# Load environment variables
DISCORD_API_KEY = os.getenv('DISCORD_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

prefix = os.getenv('BOT_PREFIX', '-')
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Use environment variables for Spotify credentials
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': "C:/ffmpeg/ffmpeg/bin/ffmpeg.exe", 
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

commands_list = [
        ("-join", "Join the voice channel you're currently in"),
        ("-leave", "Leave the current voice channel"),
        ("-play <song name or URL>", "Play a song from YouTube"),
        ("-volume <0-100>", "Set the volume of the bot"),
        ("-pause", "Pause the currently playing song"),
        ("-resume", "Resume a paused song"),
        ("-stop", "Stop the current song and clear the queue"),
        ("-create_playlist <name>", "Create a new playlist with the given name"),
        ("-add_to_playlist <playlist_name> <song name or URL>", "Add a song to the specified playlist"),
        ("-play_playlist <name>", "Play all songs in the specified playlist"),
        ("-play_spotify <Spotify URL>", "Play a Spotify track or playlist"),
        ("-my_spotify_playlists", "List all your Spotify playlists"),
        ("-help", "Display this help message")
    ]

# Add a music queue and current_song variable
bot.music_queue = []
bot.current_song = None
bot.playlists = {}

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def play(ctx, *, query):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))
    
    if ctx.voice_client:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
            
            bot.music_queue.append({'title': title, 'url': url})
            await ctx.send(f"Added to queue: {title}")
            
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def play_next(ctx):
    if bot.music_queue:
        bot.current_song = bot.music_queue.pop(0)
        ctx.voice_client.play(discord.FFmpegPCMAudio(bot.current_song['url']), after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f"Now playing: {bot.current_song['title']}")
    else:
        bot.current_song = None

@bot.command()
async def volume(ctx, volume: int):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel.")
        return
    
    if not ctx.voice_client.is_playing():
        await ctx.send("Nothing is currently playing.")
        return
    
    if 0 <= volume <= 100:
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Volume set to {volume}%")
    else:
        await ctx.send("Volume must be between 0 and 100.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused the current song")
    else:
        await ctx.send("No song is currently playing.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed the current song")
    else:
        await ctx.send("No song is paused.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        bot.music_queue.clear()
        bot.current_song = None
        await ctx.send("Stopped the current song and cleared the queue")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def create_playlist(ctx, name):
    if name not in bot.playlists:
        bot.playlists[name] = []
        await ctx.send(f"Created playlist: {name}")
    else:
        await ctx.send(f"Playlist '{name}' already exists.")

@bot.command()
async def add_to_playlist(ctx, playlist_name, *, query):
    if playlist_name in bot.playlists:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['formats'][0]['url']
            title = info['title']
        
        bot.playlists[playlist_name].append({'title': title, 'url': url})
        await ctx.send(f"Added '{title}' to playlist '{playlist_name}'")
    else:
        await ctx.send(f"Playlist '{playlist_name}' doesn't exist.")

@bot.command()
async def play_playlist(ctx, name):
    if name in bot.playlists:
        if not ctx.voice_client:
            await ctx.invoke(bot.get_command('join'))
        
        if ctx.voice_client:
            bot.music_queue.extend(bot.playlists[name])
            await ctx.send(f"Added playlist '{name}' to the queue")
            
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
    else:
        await ctx.send(f"Playlist '{name}' doesn't exist.")

@bot.command()
async def play_spotify(ctx, url):
    if 'track' in url:
        track = spotify.track(url)
        query = f"{track['name']} {track['artists'][0]['name']}"
        await ctx.invoke(bot.get_command('play'), query=query)
    elif 'playlist' in url:
        playlist = spotify.playlist(url)
        for item in playlist['tracks']['items']:
            track = item['track']
            query = f"{track['name']} {track['artists'][0]['name']}"
            await ctx.invoke(bot.get_command('play'), query=query)
        await ctx.send(f"Added {len(playlist['tracks']['items'])} songs from Spotify playlist to the queue")
    else:
        await ctx.send("Invalid Spotify URL. Please provide a track or playlist URL.")

@bot.command()
async def my_spotify_playlists(ctx):
    # Note: This requires user authentication, which is not implemented in this example
    await ctx.send("This feature requires Spotify user authentication, which is not implemented in this example.")

bot.remove_command('help')
@bot.command()
async def help(ctx):
    help_message = "**Available Commands:**\n"
    for command, description in commands_list:
        help_message += f"{command}: {description}\n"
    await ctx.send(help_message)

bot.run(DISCORD_API_KEY)
