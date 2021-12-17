import lightbulb
import logging

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
            if action == "reload":
                ctx.bot.reload_extensions()
            elif action == "load":
                ctx.bot.load_extensions()
            elif action == "unload":
                ctx.bot.unload_extensions()
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
async def shutdown(ctx) -> None:
    await ctx.bot.close()

@plugin.command
@lightbulb.option("extensions", "What extension", required=False)
@lightbulb.command(name="reload", description="Reloads an extension")
@lightbulb.implements(commands.PrefixCommand)
async def reload(ctx:  context.Context):
    await handle_extensions(ctx, ctx.options.extensions, "reload")

@plugin.command
@lightbulb.option("extensions", "What extension", required=False)
@lightbulb.command(name="load", description="Loads an extension", )
@lightbulb.implements(commands.PrefixCommand)
async def extension_load(ctx:  context.Context):
    await handle_extensions(ctx, ctx.options.extensions, "load")

@plugin.command
@lightbulb.option("extensions", "What extension", required=False)
@lightbulb.command(name="unload", description="Unloads an extension", )
@lightbulb.implements(commands.PrefixCommand)
async def unload(ctx:  context.Context):
    await handle_extensions(ctx, ctx.options.extensions, "unload")

@plugin.command
@lightbulb.option(name="statement", description="What do you want to do.")
@lightbulb.command(name="eval", description="It does something.. I think")
@lightbulb.implements(commands.PrefixCommand)
async def eval_cmd(ctx) -> None:
    result = eval(ctx.options.statement)
    print(result)
    await ctx.respond(f"```py\n>>> {result}```")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)