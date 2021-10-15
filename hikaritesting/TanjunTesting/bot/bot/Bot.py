import logging
import typing as t
from pathlib import Path
import asyncio
import hikari
import time
from bot import STDOUT_CHANNEL_ID, TEST_GUILD_ID, __version__
from .client import Client

_BotT = t.TypeVar("_BotT", bound="Bot")


class Bot(hikari.GatewayBot):
    __slots__ = hikari.GatewayBot.__slots__ + ("client", "stdout_channel")

    def __init__(self: _BotT) -> None:
        with open("./secrets/token") as f:
            token = f.read().strip("\n")

        super().__init__(
            token=token,
            intents=hikari.Intents.ALL,
        )

    def create_client(self: _BotT) -> None:
        self.client = Client.from_gateway_bot(self, set_global_commands=TEST_GUILD_ID)
        self.client.load_modules()

    def run(self: _BotT) -> None:
        self.create_client()
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)

        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name=f"/help | Version {__version__}",
                type=hikari.ActivityType.WATCHING,
            )
        )

    async def on_starting(self: _BotT, event: hikari.StartingEvent) -> None:
        pass

    async def on_started(self: _BotT, event: hikari.StartedEvent) -> None:
        self.client.scheduler.start()
        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Tanjun online for testing, version {__version__}")

        logging.info("Bot ready")

    async def on_stopping(self: _BotT, event: hikari.StoppingEvent) -> None:
        await self.stdout_channel.send("Shutting down")
        self.client.scheduler.shutdown()