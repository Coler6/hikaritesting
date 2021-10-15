from __future__ import annotations

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import hikari
from pathlib import Path
from hikari import intents
import lightbulb
from pytz import utc

from bot import __version__

HOME_GUILD_ID = 727195918180548728
STDOUT_CHANNEL_ID = 727196459518263437

class BotMain(lightbulb.Bot):
    def __init__(self) -> None:
        self._extensions = [p.stem for p in Path(".").glob("./bot/bot/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read().strip("\n")


        super().__init__(
            prefix="hk!",
            insensitive_commands=True,
            token=token,
            intents=hikari.Intents.ALL,
        )

    
    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name=f"Hikari-lightbulb | version {__version__}",
                type=hikari.ActivityType.WATCHING
            ))

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        for ext in self._extensions:
            self.load_extension(f"bot.bot.extensions.{ext}")
            logging.info(f"{ext} extention loaded")
        
    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        logging.info("Bot online!")
        self.home_guild = await self.rest.fetch_guild(HOME_GUILD_ID)
        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Lightbulb online for testing, version {__version__}.")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()
        await self.stdout_channel.send("Shutting down")