import random
import praw
import requests
import hikari
import tanjun
from aiohttp import request
from bot.bot.client import Client
import asyncio
component = tanjun.Component()

@component.with_command
@tanjun.as_message_command("clear", ["purge", "Clear", "Purge"])
async def clear(ctx: tanjun.abc.Context, amount=5) -> None:
    """Purges messages."""
    print(tanjun.PermissionCheck.get_permissions(8192))
    await ctx.channel.delete_messages(amount)
    message = await ctx.respond(f"Purged {amount} message(s)")
    await asyncio.sleep(3)
    await message.delete_message()

@component.with_command
@tanjun.as_message_command("kick", "Kick")
async def kick(ctx: tanjun.abc.Context, member : discord.Member, *, reason=None) -> None:
    """Kicks another user from the server."""
    if member.respond >= ctx.author.top_role:
        await ctx.send("That person is higher than you or the same role!")
        return
    await ctx.guild.kick(reason=reason)
    embed = hikari.Embed(title = f"Kicked {member.name} ({member.id}))", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF))
    await ctx.respond(embed = embed)

@component.with_command
@tanjun.as_message_command("ban", "Ban")
async def ban(ctx: tanjun.abc.Context, member : discord.Member, *, reason=None):
    """Bans another user from the server. (Do not use it on your self.)"""
    if member.top_role >= ctx.author.top_role or member.top_role == None:
        await ctx.respond("That person is higher than you or you have the same role!")
        return
    user = await self.bot.fetch_user(member.id)
    await ctx.guild.ban(user=user, reason=reason, delete_message_days=0)
    embed = hikari.Embed(title = f"Banned {member.name} ({member.id})", description = "Next time do not be so **BAAAAA**d", color = (0x0036FF))
    await ctx.respond(embed = embed)

@component.with_command
@tanjun.as_message_command("unban", "Unban")
async def unban(ctx: tanjun.abc.Context, *, member: discord.Member):
    """Unbans another user from the server."""
    banned_users = await ctx.rest.fetch_bans(ctx.guild)
    if member.isdigit() == True:
        peeps = await self.bot.fetch_user(member)
    else:
        member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if member.isdigit() == True:
            if user.id == peeps.id:
                await ctx.guild.unban(user)
                embed = hikari.Embed(title = "Unbanned {}" .format(peeps.name,ctx.author.mention), description = "Better not be a pain in the **horn**", color = (0x0036FF))
                await ctx.respond(embed = embed)
                return
        else:
            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = hikari.Embed(title = "Unbanned {}" .format(member.name,ctx.author.mention), description = "Better not be a pain in the **horn**", color = (0x0036FF))
                await ctx.respond(embed = embed)
                return



@component.with_command
@tanjun.as_message_command("unban", "Ubnan")
async def mute(ctx: tanjun.abc.Context, member : discord.Member):
    """Mutes another user. Stop talking."""
    guild = ctx.guild
    embed = hikariEmbed(title = "Muted {}" .format(member.name,ctx.author.mention), description = "Next time stop being a pain in the **horn**" , color = (0x0036FF))
    await ctx.respond(embed = embed)
    role = discord.utils.get(ctx.author.server.roles, name="Muted")
    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            newRole = await guild.create_role(name="Muted")
            overwrite = discord.PermissionOverwrite(send_messages=False)
            for channel in guild.text_channels:
                await channel.set_permissions(newRole,overwrite=overwrite)
            await member.add_roles(newRole)
            return

@component.with_command
@tanjun.as_message_command("unban", "Ubnan")
async def unmute(ctx: tanjun.abc.Context, member : discord.Member):
    """Unmutes another user. Keep talking"""
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            embed = hikari.Embed(title = "Unmuted {}" .format(member.name,ctx.author.mention), description = "Better not **butt** in to the conversion", color = (0x0036FF))
            await ctx.respond(embed = embed)
            return

@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())