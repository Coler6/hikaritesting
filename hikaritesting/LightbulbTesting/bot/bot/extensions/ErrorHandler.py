from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import logging
from lightbulb import commands, context
import traceback

plugin = lightbulb.Plugin("ErrorHandler")
    

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    print(traceback.print_exception(*event.exc_info))
    if isinstance(event.exception, (lightbulb.errors.ExtensionNotLoaded, lightbulb.errors.ExtensionAlreadyLoaded)):
        return
    elif isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return
    elif isinstance(event.exception, lightbulb.errors.ConverterFailure):
        return await event.context.respond("Converter Failure", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond(f"Not enough arguements were passed. {event.exception}", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        return await event.context.respond(f"Command is on cooldown. Try again in {event.exception.retry_after:.0f} seconds", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.BotMissingRequiredPermission):
        return await event.context.respond(f"I don't have the permission `{event.exception.missing_perms}` to do this!", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
        return await event.context.respond(f"You don't have the permission `{event.exception.missing_perms}`!", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.NotOwner):
        return await event.context.respond("You are not the owner of the bot!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        return await event.context.respond(f"Error with the command. {event.exception}", flags=hikari.MessageFlag.EPHEMERAL)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)