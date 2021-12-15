from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import logging
from lightbulb import commands, context

plugin = lightbulb.Plugin("Help")

@plugin.command
@lightbulb.command(name="help", description="Shows the help command.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def help(ctx):
    menu_embed = hikari.Embed(title="Help command", description="Use the select below to go to different extension's help menu.", color=(ctx.member.get_top_role().color if ctx.member != None else 0x2f3136))
    select = ctx.bot.rest.build_action_row()
    select = select.add_select_menu("Select a extension!")
    embeds = {}
    for extension in ctx.bot.extensions:
        extension = extension.split(".")[-1]
        extension = ctx.bot.get_plugin(extension)
        if extension.name == "Admin" and ctx.author.id != 674629871074279434:
            continue
        if extension.name == "ErrorHandler":
            continue
        embed = hikari.Embed(title=f"{extension.name} extension", color=(ctx.member.get_top_role().color if ctx.member != None else 0x2f3136))
        for command in extension.raw_commands:
            embed.add_field(name=f"{command.name} {f'({command.aliases})' if command.aliases != [] else ''}", value=f"{command.description}", inline=True)
        embeds[extension.name] = embed
        select.add_option(extension.name, extension.name).add_to_menu()
    message = await ctx.respond(embed=menu_embed, component=select.add_to_container())
    while True:
        try:
            event = await ctx.bot.event_manager.wait_for(hikari.InteractionCreateEvent, timeout=120)
            inter: hikari.ComponentInteraction = event.interaction
        except:
            await message.edit(content="Timed out", embed=None, components=[])
            break
        else:
            await message.edit(embed=embeds[event.interaction.values[0]])

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)