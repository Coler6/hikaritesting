import lightbulb
import logging

from lightbulb.checks import _owner_only
from bot.bot import Bot
from lightbulb import commands, context


plugin = lightbulb.Plugin("Admin")
plugin.add_checks(lightbulb.owner_only, lightbulb.guild_only)

async def handle_extensions(  ctx:  context.Context, extensions: str, action: str):
    if extensions:
        extensions = extensions.split(" ")
    else:
        extensions = [e.split(".")[-1] for e in ctx.bot.extensions]
    count = 0
    for ext in extensions:
        try:
            getattr(ctx.bot, f"{action}_extension")(f"bot.bot.extensions.{ext.lower()}")
            logging.info(f"'{ext}' extension {action}ed")
            count += 1
        except lightbulb.errors.ExtensionAlreadyLoaded:
            logging.error(f"Extention '{ext}' is already loaded")
        except lightbulb.errors.ExtensionNotLoaded:
            logging.error(f"Extention '{ext}' is already loaded")
    await ctx.respond(f"{count} extension(s) {action}ed")

@plugin.command
@lightbulb.command(name="shutdown", description="Shutsdown the entire freaking bot.", aliases=("sd", ))
@lightbulb.implements(commands.PrefixCommand)
async def command_shutdown(ctx) -> None:
    await ctx.bot.close()

@plugin.command
@lightbulb.command(name="reload", description="Reloads an extension")
@lightbulb.implements(commands.PrefixCommand)
async def reload(  ctx:  context.Context, *, extensions: str = ""):
    await self.handle_extensions(ctx, extensions, "reload")

@plugin.command
@lightbulb.command(name="load", description="Loads an extension", )
@lightbulb.implements(commands.PrefixCommand)
async def load(  ctx:  context.Context, *, extensions: str = ""):
    await self.handle_extensions(ctx, extensions, "load")

@plugin.command
@lightbulb.command(name="unload", description="Unloads an extension", )
@lightbulb.implements(commands.PrefixCommand)
async def unload(  ctx:  context.Context, *, extensions: str = ""):
    await self.handle_extensions(ctx, extensions, "unload")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)