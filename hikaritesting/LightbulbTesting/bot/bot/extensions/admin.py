import lightbulb
import logging

from lightbulb.checks import _owner_only
from bot.bot import Bot

class Admin(lightbulb.Plugin):

    async def handle_extensions(self, ctx: lightbulb.Context, extensions: str, action: str):
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

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="shutdown", aliases=("sd", ))
    async def command_shutdown(self, ctx: lightbulb.Context) -> None:
        await ctx.bot.close()

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="reload")
    async def reload(self, ctx: lightbulb.Context, *, extensions: str = ""):
        await self.handle_extensions(ctx, extensions, "reload")

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="load")
    async def load(self, ctx: lightbulb.Context, *, extensions: str = ""):
        await self.handle_extensions(ctx, extensions, "load")

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="unload")
    async def unload(self, ctx: lightbulb.Context, *, extensions: str = ""):
        await self.handle_extensions(ctx, extensions, "unload")

def load(bot: Bot) -> None:
    bot.add_plugin(Admin())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")