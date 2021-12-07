from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import logging
import datetime as dt
import asyncio
from lightbulb import commands, context

plugin = lightbulb.Plugin("Moderation")

@plugin.command
@lightbulb.option("amount", "Choose how many messages you want to delete. (default 5)", type=int, required=False)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.command(name="purge", description="Purges messages.", aliases=['clear'])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def purge(ctx):
    print(1)
    amount = ctx.options.amount or 5
    print(1.5)
    channel = ctx.channel_id
    print(2)
    if amount <= 0:
        await ctx.respond("Please pick a number higher than 0!")
        return
    print(3)
    if isinstance(ctx, context.PrefixContext):
        await ctx.event.message.delete()
    print(4)
    messages = await ctx.bot.rest.fetch_messages(channel).limit(amount)
    print(5)
    await ctx.bot.rest.delete_messages(channel, messages)
    print(6)
    msg = await ctx.respond(f"Deleted {len(messages)} messages!")
    print(7)
    await asyncio.sleep(3)
    print(8)
    await msg.delete()
    print(9)

@plugin.command
@lightbulb.option("reason", "Reason of the kick.", required=False)
@lightbulb.option("member", "The member that is getting kicked", hikari.User, required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.command(name="kick", description="Kicks another user from the server.",)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def kick(ctx):
    member = ctx.options.member
    reason = ctx.options.reason or None
    print(1)
    if member.get_top_role().position >= ctx.member.get_top_role().position:
        await ctx.respond("You are not high enough to kick that user!")
        return
    print(2)
    await member.kick(reason=f'Kicked by {ctx.author.username} for: {reason}')
    print(3)
    embed = (hikari.Embed(title = f"Kicked {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
    print(4)
    if reason != None:
        embed.add_field("Reason", reason)
        print(5)
    await ctx.respond(embed=embed)
    print(6)

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
        print(1.5)
        if member.id == ctx.author.id:
            await ctx.respond("You can't ban your self")
            return
        print(2)
        if member_obj.get_top_role().position >= ctx.member.get_top_role().position:
            await ctx.respond("That person is higher than you or you have the same role!")
            return
    print(2)
    await ctx.bot.rest.ban_user(ctx.guild_id, member, reason=f"Banned by {ctx.author.username} for: {'no reason provided' if reason == None else reason}")
    print(3)
    embed = (hikari.Embed(title = f"Banned {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
    print(4)
    if reason != None:
        embed.add_field("Reason", reason)
    print(5)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.option("reason", "Reason of the kick.", required=False)
@lightbulb.option("member", "The member that is getting unbanned", hikari.User, required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.command(name="unban", description="Unbans a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def unban(ctx):
    print(.05)
    member = ctx.options.member
    bans = await ctx.bot.rest.fetch_bans(ctx.guild_id)
    print(.1)
    for bans in bans:
        print(bans.user.username)
        if bans.user.id == member.id:
            print(1)
            print(ctx.guild_id)
            print(member)
            await ctx.bot.rest.unban_user(ctx.guild_id, member, reason=f"Unbanned by {ctx.author.username} for: {'no reason provided' if ctx.options.reason == None else ctx.options.reason}")
            print(2)
            embed = (hikari.Embed(title = f"Unbanned {member.username} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF), timestamp=dt.datetime.now().astimezone(),).set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url))
            print(3)
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
    print(.1)
    guild = ctx.get_guild()
    print(.2)
    member = ctx.options.member
    print(1)
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    print(2)
    for role in await guild.fetch_roles():
        if role.name.lower() == "muted":
            print(3)
            await member.add_role(role, reason=f"Muted by {ctx.author.username}")
            print(4)
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
    print(.1)
    guild = ctx.get_guild()
    print(.2)
    member = ctx.options.member
    print(1)
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    print(2)
    for role in await guild.fetch_roles():
        if role.name.lower() == "muted":
            print(3)
            await member.remove_role(role, reason=f"Unmuted by {ctx.author.username}")
            print(4)
            embed = (hikari.Embed(title = f"Unmuted {member.username} ({member.id})", description = "Better not **butt** in to the conversion", color = (0x0036FF)))
            await ctx.respond(embed = embed)
            return
    await ctx.respond("Could not find a `muted` role.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)