from base64 import b64decode
import logging
import typing as t
from pathlib import Path
import asyncio
import hikari
import time
from bot import STDOUT_CHANNEL_ID, TEST_GUILD_ID, __version__
import lightbulb
import lavasnek_rs
_BotT = t.TypeVar("_BotT", bound="Bot")
log = logging.getLogger(__name__)



class EventHandler:
    async def track_start(self, lavalink, event):
        log.info(f"Track started on guild: {event.guild_id}")

    async def track_finish(self, lavalink, event):
        log.info(f"Track finished on guild: {event.guild_id}")

    async def track_exception(self, lavalink, event):
        log.warning(f"Track exception event happened on guild: {event.guild_id}")

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not skip:
            await event.message.respond("Nothing to skip")
            return

        if not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)



class Bot(lightbulb.Bot):
    __slots__ = ("client", "stdout_channel", "lavalink")


    def __init__(self: _BotT) -> None:
        self._extensions = [p.stem for p in Path(".").glob("./bot/bot/extensions/*.py")]
        with open("./secrets/token") as f:
            self.token = token = f.read().strip("\n")

        super().__init__(
            token=token,
            intents=hikari.Intents.ALL,
            slash_commands_only=True,
        )

    def run(self: _BotT) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.VoiceStateUpdateEvent, self.on_voice_state_update)
        self.event_manager.subscribe(hikari.VoiceServerUpdateEvent, self.on_voice_server_update)

        super().run(
            activity=hikari.Activity(
                name=f"Lightbulb with Lavasnek | Version {__version__}",
                type=hikari.ActivityType.WATCHING,
            )
        )
    async def on_starting(self, event: hikari.StartingEvent) -> None:
        test_guild_snowflake = await self.rest.fetch_guild(TEST_GUILD_ID)
        for ext in self._extensions:
            self.load_extension(f"bot.bot.extensions.music")
            logging.info(f"{ext} extention loaded")

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        builder = (
            lavasnek_rs.LavalinkBuilder(self.get_me().id, self.token)
            .set_host("127.0.0.1")
        )

        builder.set_start_gateway(False)
        count = 1
        await asyncio.sleep(5)
        while count <= 5:
            try:
                self.lavalink = await builder.build(EventHandler())
            except:
                log.error(f"Couldn't connect, retrying. (attempt {count} of 5)")
                await asyncio.sleep(3)
                count += 1
                if count > 5:
                    log.error("Could not connect to the lavalink server. Stopping process.")
                    return
            else:
                break
        log.info("Created Lavalink instance")
        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Lightbulb with lavasnek online for testing, version {__version__}")

        log.info("Bot ready")


    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        await self.stdout_channel.send("Shutting down")

    async def on_voice_state_update(self, event: hikari.VoiceStateUpdateEvent) -> None:
        await self.lavalink.raw_handle_event_voice_state_update(
            event.state.guild_id,
            event.state.user_id,
            event.state.session_id,
            event.state.channel_id,
        )

    async def on_voice_server_update(self, event: hikari.VoiceServerUpdateEvent) -> None:
        await self.lavalink.raw_handle_event_voice_server_update(
            event.guild_id, event.endpoint, event.token
        )