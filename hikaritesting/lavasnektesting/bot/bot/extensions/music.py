import sys
import inspect
import hikari
import typing as t
from lightbulb import slash_commands
import lavasnek_rs
import lightbulb
from lavasnek_rs import NoSessionPresent
import logging as log
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from bot import STDOUT_CHANNEL_ID, TEST_GUILD_ID, __version__
import asyncio

os.environ['SPOTIPY_CLIENT_ID'] = 'a68a4a64a63340748b7c99d96c5cacc5'
os.environ['SPOTIPY_CLIENT_SECRET'] = '7eb1004ad1f0404e94dea5eae80e92b6'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

async def _join(ctx: slash_commands.SlashCommandContext) -> t.Optional[hikari.Snowflake]:
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    if not voice_state:
        await ctx.respond("Connect to a voice channel first")
        return None

    channel_id = voice_state[0].channel_id

    if not channel_id:
        await ctx.respond("You are in a voice channel but not in a voice channel?")
        return None

    await ctx.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    connection_info = await ctx.bot.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    await ctx.bot.lavalink.create_session(connection_info)
    return channel_id

class Connect(slash_commands.SlashCommand):
    description: str = "Connect to a voice channel"
    enabled_guilds: None

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        channel_id = await _join(ctx)
        if channel_id:
            await ctx.respond(f"Joined <#{channel_id}>")
        
class Disconnect(slash_commands.SlashCommand):
    description: str = "Disconnect from a voice channel."
    enabled_guilds: None
    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.bot.lavalink.destroy(ctx.guild_id)
        await ctx.bot.update_voice_state(ctx.guild_id, None)
        await ctx.bot.lavalink.wait_for_connection_info_remove(ctx.guild_id)
        await ctx.bot.lavalink.remove_guild_node(ctx.guild_id)
        await ctx.bot.lavalink.remove_guild_from_loops(ctx.guild_id)
        await ctx.respond("Disconnected from voice channel.")

class Play(slash_commands.SlashCommand):
    description: str = "Play some music!"
    enabled_guilds: None
    query: str = slash_commands.Option("Song to play")

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        cxn = await ctx.bot.lavalink.get_guild_gateway_connection_info(ctx.guild_id)
        if not cxn:
            channel_id = await _join(ctx)
        query_info = await ctx.bot.lavalink.auto_search_tracks(ctx.options.query)
        if not query_info.tracks:
            await ctx.respond("Could not find that query")
            return
        try:
            await ctx.bot.lavalink.play(ctx.guild_id, query_info.tracks[0]).requester(ctx.author.id).queue()
        except NoSessionPresent:
            await ctx.respond("No session present error! Use the /connect command to resolve this.")
            return
        await ctx.respond(f"Added `{query_info.tracks[0].info.title}` to the queue.")


class Pause(slash_commands.SlashCommand):
    description: str = "Pauses the music."
    enabled_guilds: None

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.bot.lavalink.pause(ctx.guild_id)
        await ctx.respond("Paused the music!")

class Resume(slash_commands.SlashCommand):
    description: str = "Resumes the music."
    enabled_guilds: None

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.bot.lavalink.resume(ctx.guild_id)
        await ctx.respond("Resumed the music!")

class Volume(slash_commands.SlashCommand):
    description: str = "Change the volume."
    enabled_guilds: None
    volume: int = slash_commands.Option("Volume you want to change to. (min 0, max 150)")

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        if ctx.options.volume > 250:
            await ctx.respond("The max is 250!")
            return
        if ctx.options.volume < 0:
            await ctx.respond("The min is 0!")
            return
        await ctx.bot.lavalink.volume(ctx.guild_id, ctx.options.volume)
        await ctx.respond(f"Changed the volume to {ctx.options.volume}")

class Skip(slash_commands.SlashCommand):
    description: str = "Skips the song"
    enabled_guilds: None

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        skip = await ctx.bot.lavalink.skip(ctx.guild_id)
        node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
        if not skip:
            await ctx.respond("Nothing left to skip")
            return
        if not node.queue and not node.now_playing:
            await ctx.bot.lavalink.stop(ctx.guild_id)
        await ctx.respond(f"Skipped from `{skip.track.info.title}` to `{node.now_playing.track.info.title if node.now_playing == None else 'Its none'}`")

        
class SkipTo(slash_commands.SlashCommand):
    description: str = "Skips to a specific song"
    enabled_guilds: None
    # query: str = slash_commands.Option()
    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        pass

class SearchSpotifyURL(slash_commands.SlashCommand):
    description: str = "Searches spotify URL then adds the songs"
    enabled_guilds: None
    url: str = slash_commands.Option("URL to search up (Can be a playlist URL or album URL)")
    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
        try:
            album = spotify.album(ctx.options.url)
            URL_type = "album"
        except:
            try:
                album = spotify.playlist(ctx.options.url)
                URL_type = "playlist"
            except:
                log.error("Failed album and playlist")
                await ctx.respond("Not a valid album or playlist.")
                return
        num_of_songs = len(album['tracks']['items'])
        await ctx.respond(f"Adding {num_of_songs} songs...")
        for idx, item in enumerate(album['tracks']['items']):
            if URL_type == "album":
                name = item['name']
                artist = item['artists'][0]['name']
            elif URL_type == "playlist":
                name = item['track']['name']
                artist = item['track']['artists'][0]['name']
            query_info = await ctx.bot.lavalink.auto_search_tracks(f'{name} {artist}')
            try:
                i = await ctx.bot.lavalink.play(ctx.guild_id, query_info.tracks[0]).requester(ctx.author.id).queue().start()
            except NoSessionPresent:
                await ctx.respond("No session present error! Use the /connect command to resolve this.")
                return
            except AttributeError:
                try:
                    i = await ctx.bot.lavalink.play(ctx.guild_id, query_info.tracks[0]).requester(ctx.author.id).queue()
                except NoSessionPresent:
                    await ctx.respond("No session present error! Use the /connect command to resolve this.")
                    return
        if URL_type == "album":
            await ctx.respond(f"Successfully added {num_of_songs} song(s) from the album `{album['name']}` to the queue")
            return
        elif URL_type == "playlist":
            await ctx.respond(f"Successfully added {num_of_songs} song(s) from the playlist `{album['name']}` to the queue")
            return

class queue(slash_commands.SlashCommand):
    description: str = "Shows the current queue"
    enabled_guilds: None

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
        if not node:
            await ctx.respond("No tracks in the queue!")
            return
        amount = node.queue[0].track.info.length
        millis = int(amount)
        l_seconds=(millis/1000)%60
        l_seconds = int(l_seconds)
        l_minutes=(millis/(1000*60))%60
        l_minutes = int(l_minutes)
        requester = await ctx.bot.rest.fetch_member(ctx.guild_id, node.queue[0].requester)
        first_n = int(l_seconds/10)
        embed = (
            hikari.Embed(
                title="Queue",
                description=f"Showing {len(node.queue)} songs",
            )
            .add_field(name="Volume", value=node.volume)
            .add_field(name="Now playing", value=node.queue[0].track.info.title + f"\nLength of song {l_minutes}:{l_seconds if first_n != 0 else f'0{l_seconds}'}\nRequested by {requester.nickname}")
        )
        count = 1
        if len(node.queue) > 1:
            embed.add_field(name="Up Next", value=f"(Showing {'15' if len(node.queue) > 15 else len(node.queue)-1} out of {len(node.queue)-1})")
            for q in node.queue[1:]:
                if count <= 15:
                    amount = q.track.info.length
                    millis = int(amount)
                    l_seconds=(millis/1000)%60
                    l_seconds = int(l_seconds)
                    l_minutes=(millis/(1000*60))%60
                    l_minutes = int(l_minutes)
                    first_n = int(l_seconds/10)
                    embed.add_field(name=f"{count}. {q.track.info.title}", value=f"Length of song {l_minutes}:{l_seconds if first_n != 0 else f'0{l_seconds}'}")
                    count += 1
                else:
                    break
        await ctx.respond(embed=embed)

def load(bot) -> None:
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(obj, slash_commands.SlashCommand):
            bot.add_slash_command(obj)
            log.info(f"Loaded {obj.__name__} command!")