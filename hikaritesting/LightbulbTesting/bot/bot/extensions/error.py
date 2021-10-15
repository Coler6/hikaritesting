from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
from lightbulb import plugins
import logging

class ErrorHandler(lightbulb.Plugin):
    
    @plugins.listener()
    async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:

        if isinstance(event.exception, (lightbulb.errors.ExtensionNotLoaded, lightbulb.errors.ExtensionAlreadyLoaded)):
            return
        elif isinstance(event.exception, lightbulb.errors.CommandNotFound):
            return
        elif isinstance(event.exception, lightbulb.errors.ConverterFailure):
            return await event.context.respond("Converter Failure")
        elif isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            return await event.context.respond("Not enough arguements were passed. " + event.exception.missing_args)

        elif isinstance(event.exception, lightbulb.errors.TooManyArguments):
            return await event.context.respond("Too many arguements were passed.")

        elif isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
            return await event.context.respond(f"Command is on cooldown. Try again in {event.exception.retry_after:.0f} seconds")

        else:
            await event.context.respond(f"An unhandled error occurred! `{event.exception}`")

    

def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())

def unload(bot: Bot) -> None:
    bot.remove_plugin("ErrorHandler")