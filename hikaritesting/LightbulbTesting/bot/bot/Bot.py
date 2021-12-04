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

class BotMain(lightbulb.BotApp):
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read().strip("\n")


        super().__init__(
            prefix="hk!",
            ignore_bots=True,
            help_slash_command=True, 
            case_insensitive_prefix_commands=True,
            token=token,
            intents=hikari.Intents.ALL,
            delete_unbound_commands=True,
            help_class=None,
            logs={
                "version": 1,
                "incremental": True,
                "loggers": {
                    "lightbulb": {"level": "DEBUG"},
                }
            }
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
        self.load_extensions_from("./bot/bot/extensions/", must_exist=True)

    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        logging.info("Bot online!")
        self.home_guild = await self.rest.fetch_guild(HOME_GUILD_ID)
        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"Lightbulb online for testing, version {__version__}.")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()
        await self.stdout_channel.send("Shutting down")