from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import datetime as dt
import asyncio
from lightbulb import commands, context

plugin = lightbulb.Plugin("Moderation")
plugin.add_checks(lightbulb.guild_only)

@plugin.command
@lightbulb.option("amount", "Choose how many messages you want to delete. (default 5)", type=int, required=False)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.command(name="purge", description="Purges messages.", aliases=['clear'])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def purge(ctx):
    amount = ctx.options.amount or 5
    channel = ctx.channel_id
    if amount <= 0:
        await ctx.respond("Please pick a number higher than 0!")
        return
    if isinstance(ctx, context.PrefixContext):
        await ctx.event.message.delete()
    messages = await ctx.bot.rest.fetch_messages(channel).limit(amount)
    await ctx.bot.rest.delete_messages(channel, messages)
    msg = await ctx.respond(f"Deleted {len(messages)} messages!")
    await asyncio.sleep(3)
    await msg.delete()

@plugin.command
@lightbulb.option("reason", "Reason of the kick.", required=False)
@lightbulb.option("member", "The member that is getting kicked", hikari.User, required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.command(name="kick", description="Kicks another user from the server.",)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def kick(ctx):
    member = ctx.options.member
    reason = ctx.options.reason or None
    if member.get_top_role().position >= ctx.member.get_top_role().position:
        await ctx.respond("You are not high enough to kick that user!")
        return
    await member.kick(reason=f'Kicked by {ctx.author.username} for: {reason}')
    embed = (hikari.Embed(title = f"Kicked {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
    if reason != None:
        embed.add_field("Reason", reason)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.option("reason", "Reason of the ban.", required=False)
@lightbulb.option("member", "The member that is getting banned", hikari.User, required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.command(name="ban", description="Bans another user from the server.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def ban(ctx: context.Context):
    member = ctx.options.member
    reason = ctx.options.reason or None
    guild = ctx.get_guild()
    member_obj = guild.get_member(member.id)
    if member_obj != None: # if user is in the server
        if member.id == ctx.author.id:
            await ctx.respond("You can't ban your self")
            return
        if member_obj.get_top_role().position >= ctx.member.get_top_role().position:
            await ctx.respond("That person is higher than you or you have the same role!")
            return
    await ctx.bot.rest.ban_user(ctx.guild_id, member, reason=f"Banned by {ctx.author.username} for: {'no reason provided' if reason == None else reason}")
    embed = (hikari.Embed(title = f"Banned {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
    if reason != None:
        embed.add_field("Reason", reason)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.option("reason", "Reason of the kick.", required=False)
@lightbulb.option("member", "The member that is getting unbanned", hikari.User, required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.command(name="unban", description="Unbans a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def unban(ctx):
    member = ctx.options.member
    bans = await ctx.bot.rest.fetch_bans(ctx.guild_id)
    for bans in bans:
        print(bans.user.username)
        if bans.user.id == member.id:
            await ctx.bot.rest.unban_user(ctx.guild_id, member, reason=f"Unbanned by {ctx.author.username} for: {'no reason provided' if ctx.options.reason == None else ctx.options.reason}")
            embed = (hikari.Embed(title = f"Unbanned {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
            await ctx.respond(embed=embed)
            return
    embed = (hikari.Embed(title = f"Uh oh!", description = "Could not find that user in the ban list", color = (0xff0000), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("member", "The member that is getting muted", hikari.User, required=True)
@lightbulb.command(name="mute", description="Mutes another user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def mute(ctx):
    guild = ctx.get_guild()
    member = ctx.options.member
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    for role in await guild.fetch_roles():
        if role.name.lower() == "muted":
            await member.add_role(role, reason=f"Muted by {ctx.author.username}")
            embed = (hikari.Embed(title = f"Muted {member.username} ({member.id})", description = "Shush it and stop being a pain in the **horn**", color = (0x0036FF)))
            await ctx.respond(embed = embed)
            return
    await ctx.respond("Could not find a `muted` role.")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("member", "The member that is getting unmuted", hikari.User, required=True)
@lightbulb.command(name="unmute", description="Unmuted another user from the server.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def unmute(ctx):
    guild = ctx.get_guild()
    member = ctx.options.member
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    for role in await guild.fetch_roles():
        if role.name.lower() == "muted":
            await member.remove_role(role, reason=f"Unmuted by {ctx.author.username}")
            embed = (hikari.Embed(title = f"Unmuted {member.username} ({member.id})", description = "Better not **butt** in to the conversion", color = (0x0036FF)))
            await ctx.respond(embed = embed)
            return
    await ctx.respond("Could not find a `muted` role.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)