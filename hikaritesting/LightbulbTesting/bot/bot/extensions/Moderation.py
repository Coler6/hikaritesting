from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import datetime as dt
import asyncio
from lightbulb import commands, context
from bot.bot.utils import conv

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
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.option("member", "The member that is getting muted", hikari.User, required=True)
@lightbulb.option("time", "How long they get timed out for. ex: 5d (s=second, m=minute, h=hour, d=day, w=week)", str, default="7d", required=False)
@lightbulb.command(name="timeout", description="Times out another user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def timeout(ctx):
    guild = ctx.get_guild()
    member = ctx.options.member
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    if member.communication_disabled_until() != None:
        return await ctx.respond("That member is already timed out!")
    time = conv.time_amount(ctx.options.time, max=2419200)
    print(time)
    if time[0] == None:
        if time[1] == 0:
            return await ctx.respond("Invalid time or error converting")
        if time[1] == 1:
            return await ctx.respond("Sorry, the max is 28 days!")
    await member.edit(communication_disabled_until=dt.datetime.utcnow() + dt.timedelta(0, time[0]), reason=f"Timed out for {str(time[2]) + ' ' + str(time[1]) + ('s' if time[2] != 1 else '')} by {ctx.author.username}")
    embed = (hikari.Embed(title = f"Timed out {member.username} ({member.id}) for {str(time[2]) + ' ' + str(time[1]) + ('s' if time[2] != 1 else '')}", description = "Shush it and stop being a pain in the **horn**", color = (0x0036FF)))
    await ctx.respond(embed = embed)
    # for role in await guild.fetch_roles():
    #     if role.name.lower() == "muted":
    #         await member.add_role(role, reason=f"Muted by {ctx.author.username}")
    #         embed = (hikari.Embed(title = f"Muted {member.username} ({member.id})", description = "Shush it and stop being a pain in the **horn**", color = (0x0036FF)))
    #         await ctx.respond(embed = embed)
    #         return
    # await ctx.respond("Could not find a `muted` role.")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.option("member", "The member that is getting untimed out", hikari.User, required=True)
@lightbulb.command(name="untimeout", description="Untimes out another user from the server.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def untimeout(ctx):
    guild = ctx.get_guild()
    member = ctx.options.member
    if member.id == ctx.author.id:
        return await ctx.respond("That's you!")
    if member.communication_disabled_until() == None:
        return await ctx.respond("That member is not timed out!")
    await member.edit(communication_disabled_until=None, reason=f"Untimed out by {ctx.author.username}")
    embed = (hikari.Embed(title = f"Untimed out {member.username} ({member.id})", description = "Better not **butt** in to the conversation", color = (0x0036FF)))
    await ctx.respond(embed = embed)
    # for role in await guild.fetch_roles():
    #     if role.name.lower() == "muted":
    #         await member.remove_role(role, reason=f"Unmuted by {ctx.author.username}")
    #         embed = (hikari.Embed(title = f"Unmuted {member.username} ({member.id})", description = "Better not **butt** in to the conversation", color = (0x0036FF)))
    #         await ctx.respond(embed = embed)
    #         return
    # await ctx.respond("Could not find a `muted` role.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)