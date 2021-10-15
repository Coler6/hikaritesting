import hikari
from bot.bot import Bot
from bot.bot.Bot import Bot as _bot_
import typing as t
import datetime as dt
import tanjun
from bot.bot.client import Client

component = tanjun.Component()

async def complete_giveaway(self, channel_id, message_id):
        print("it worked")
        message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        print("1")
        winner = choice([u for u in await message.reactions[0].users().flatten() if not u.bot])
        print("2")
        if winner != None:
            print("someone entered and won")
            await message.channel.send(f"Congratulations {winner.mention}, you won!")
            return
        else:
            print("no one entered...")
            await message.channel.send("No one entered the giveaway...")
            return

@component.with_slash_command
@tanjun.with_member_slash_option("target", "Leave none if you want to show the info for yourself", default=None)
@tanjun.as_slash_command("userinfo", "Shows the info of a user or yourself!")
async def userinfo(ctx: tanjun.abc.Context, target) -> None:
    target = target or ctx.member
    top_role = target.get_top_role()
    presence = target.get_presence() 
    embed = (
        hikari.Embed(
        title="User information",
        color= top_role.colour,
        timestamp=dt.datetime.now().astimezone(),
        )
        .set_thumbnail(target.avatar_url)
        .set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    )
    fields = [("Name", str(target), True),
                ("Discriminator", target.discriminator, True),
                ("ID", target.id, True),
                ("Bot?", target.is_bot, True),
                ("Top role", top_role.mention if top_role.mention else '@everyone', True),
                #("Status", str(target.status), True),
                ("Presence", presence.visible_status if presence != None else "Offline" + presence.activities[0].name if presence != None else "Offline", True),
                ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Boosted since", getattr(target.premium_since, "strftime", lambda x: "Not boosting")("%d/%m/%Y %H:%M:%S"), True)
                ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.respond(embed=embed)

@component.with_slash_command
@tanjun.as_slash_command("serverinfo", "Shows the info of the server!")
async def server_info(ctx: tanjun.abc.Context) -> None:
    guild = ctx.get_guild()
    owner = await guild.fetch_owner()
    embed = (
        hikari.Embed(
        title="Server information",
        color=owner.get_top_role().color,
        timestamp=dt.datetime.now().astimezone(),
        )
        .set_thumbnail(guild.icon_url)
        .set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    )
    members = guild.get_members()
    online = 0
    idle = 0
    dnd = 0
    offline = 0
    for mem, m in members.items():
        presence = m.get_presence()
        if presence == None: offline += 1
        elif presence.visible_status == "online": online += 1
        elif presence.visible_status == "idle": idle += 1
        elif presence.visible_status == "dnd": dnd += 1
        
    channels = guild.get_channels()
    text_channels = 0
    voice_channels = 0
    categories = 0
    for mem, m in channels.items():
        chan_type = str(m.type)
        if chan_type == "GUILD_TEXT": text_channels += 1
        elif chan_type == "GUILD_VOICE": voice_channels += 1
        elif chan_type == "GUILD_CATEGORY": categories += 1
    fields = [("ID", guild.id, True),
                ("Owner", f"{owner} ({owner.id})", True),
                ("Created at", guild.created_at.strftime("%d/%m/%Y"), True),
                ("Members", len(members), True),
                ("Humans", len(list(filter(lambda m: not m.is_bot, (m for mem, m in members.items())))), True),
                ("Bots", len(list(filter(lambda m: m.is_bot, (m for mem, m in members.items())))), True),
                ("Banned members", len(await ctx.client.rest.fetch_bans(guild)) if await ctx.client.rest.fetch_bans(guild) != None else "Not available", True),
                ("Statuses", f"🟢 {online} 🟠 {idle} 🔴 {dnd} ⚪ {offline}", True),
                ("Text channels", text_channels, True),
                ("Voice channels", voice_channels, True),
                ("Categories", categories, True),
                ("Roles", len(await guild.fetch_roles()), True),
                ("\u200b", "\u200b", True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.respond(embed=embed)

@tanjun.as_loader
def load_component(client: Client) -> None:
    client.add_component(component.copy())