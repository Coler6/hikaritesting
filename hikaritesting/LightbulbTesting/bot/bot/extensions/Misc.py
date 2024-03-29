import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context
import traceback
from bot.bot.utils import db, conv
import asyncio

plugin = lightbulb.Plugin("Misc")

badges = conv.badges

@plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", description="Shows the info of a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand, commands.UserCommand)
async def userinfo(ctx) -> None:
    target = ctx.options.target or ctx.member
    print(target)
    user_target = await ctx.bot.rest.fetch_user(target.id)
    print(user_target)
    if str(type(target)) == "<class 'hikari.users.UserImpl'>":
        embed = (
            hikari.Embed(
            title="Partial user information",
            description=target.mention,
            color= 0x2f3136,
            timestamp=dt.datetime.now().astimezone(),
            )
            .set_thumbnail(target.avatar_url)
            .set_image(user_target.banner_url)
            .set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
        )
        print(5.2)
        fields = [("Name", str(target), True),
                    ("Discriminator", target.discriminator, True),
                    ("ID", target.id, True),
                    ("Bot?", target.is_bot, True),
                    ("Created at", target.created_at.strftime('%d/%m/%Y %H:%M:%S'), True),
                    ("Badges", badges(target.flags), True)
                    ]
    else:
        top_role = target.get_top_role()
        presence = target.get_presence()
        embed = (
            hikari.Embed(
            title="User information",
            description=target.mention,
            color= top_role.color,
            timestamp=dt.datetime.now().astimezone(),
            )
            .set_thumbnail(target.avatar_url)
            .set_image(user_target.banner_url)
            .set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
        )
        print(5)
        print(dt.datetime.utcfromtimestamp(int(dt.datetime.timestamp(target.created_at))))
        print(dt.datetime.timestamp(target.joined_at))
        print(dt.datetime.utcnow())
        fields = [("Name", str(target), True),
                    ("Discriminator", target.discriminator, True),
                    ("ID", target.id, True),
                    ("Bot?", target.is_bot, True),
                    ("Top role", top_role.mention if top_role.mention else '@everyone', True),
                    #("Status", str(target.status), True),
                    ("Presence", presence.visible_status if presence != None else "Offline" + presence.activities[0].name if presence != None else "Offline", True),
                    ("Created at", f"{conv.long_delta(dt.datetime.utcnow() - dt.datetime.utcfromtimestamp(int(dt.datetime.timestamp(target.created_at))))} (<t:{int(dt.datetime.timestamp(target.created_at))}:D>)", True),
                    ("Joined at",f"{conv.long_delta(dt.datetime.utcnow() - dt.datetime.utcfromtimestamp(int(dt.datetime.timestamp(target.joined_at))))} (<t:{int(dt.datetime.timestamp(target.joined_at))}:D>)", True),
                    ("Boosted since", getattr(target.premium_since, "strftime", lambda x: "Not boosting")("%d/%m/%Y %H:%M:%S"), True),
                    ("Badges", badges(target.flags), True)
                    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("serverinfo", description="Shows the info of the server.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def serverinfo(ctx) -> None:
    guild = await ctx.get_guild().fetch_self()
    owner = guild.get_member(guild.owner_id)
    embed =  hikari.Embed(
        title="Server information",
        description=guild.name,
        color=owner.get_top_role().color,
        timestamp=dt.datetime.now().astimezone(),
        )
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    print(4)
    statuses = [len(list(filter(lambda m: str(m.visible_status.value) == "online", list(guild.get_presences().values())))),
                len(list(filter(lambda m: str(m.visible_status.value) == "idle", list(guild.get_presences().values())))),
                len(list(filter(lambda m: str(m.visible_status.value) == "dnd", list(guild.get_presences().values())))),
                len(guild.get_members())-len(list(guild.get_presences()))]

    channel = [len(list(filter(lambda m: m.type.value == 0 or m.type.value == 5, list(guild.get_channels().values())))),
            len(list(filter(lambda m: m.type.value == 2 or m.type.value == 13, list(guild.get_channels().values())))),
            len(list(filter(lambda m: m.type.value == 4, list(guild.get_channels().values())))),
            len(list(filter(lambda m: m.type.value == 13, list(guild.get_channels().values())))),
            len(list(filter(lambda m: m.type.value == 5, list(guild.get_channels().values())))),]
    features = ""
    for i in guild.features:
        features = features + i + "\n"
    print(5)
    bans = await ctx.bot.rest.fetch_bans(guild)
    fields = [("ID", guild.id, True),
                ("Owner", owner, True),
                ("Created at", guild.created_at.strftime('%d/%m/%Y %H:%M:%S'), True),
                ("Boosts", str(f"{guild.premium_subscription_count if guild.premium_subscription_count != None else '0'} boost{'s' if guild.premium_subscription_count != 1 else ''} (level {guild.premium_tier.value})"), True),
                ("Members", len(guild.get_members()), True),
                ("Humans", len(list(filter(lambda m: not m.is_bot, list(guild.get_members().values())))), True),
                ("Bots", len(list(filter(lambda m: m.is_bot, list(guild.get_members().values())))), True),
                ("Banned members", (len(bans) if bans != None else "Not available"), True),
                ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                ("Roles", len(guild.get_roles()), True),
                ("Emojis", len(guild.get_emojis()), True),
                ("Stickers", len(await guild.fetch_stickers()), True),
                ("Total channels", len(guild.get_channels()), True),
                ("Text channels", f"{channel[0]} ({channel[4]} annoucement channel{'s' if channel[4] != 1 else ''})", True),
                ("Voice channels", f"{channel[1]} ({channel[3]} stage channel{'s' if channel[3] != 1 else ''})", True),
                ("Categories", channel[2], True),
                ("Features", features, False),
                ("\u200b", "\u200b", True)]
    print(7)
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    embed.set_thumbnail(guild.icon_url)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.command("privacy", description="What does the bot use?", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand)
async def privacy(ctx):
    await ctx.send("**Privacy info**\nWhat do we store?\nWe store your ID if you use our economy system.\nFor reaction roles we store the emoji id, message id, channel id, and role id.\nFor guild customization we only store the guild id and the prefix and id of the ticket.\n\nIf you have any questions please join the support server below! https://discord.gg/rBwSEyH")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("target", "The user to get the banner.", hikari.User, required=False)
@lightbulb.command("avatar", description="The avatar of a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def avatar(ctx):
    print(1)
    target = ctx.options.target or ctx.member
    print(2)
    print(target.avatar_url)
    embed = hikari.Embed(title=f"Avatar for {target.username}", description=None, color=(target.get_top_role().color))
    print(3)
    embed.set_image(target.avatar_url)
    print(4)
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("target", "The user to get the banner.", hikari.User, required=False)
@lightbulb.command("banner", description="The banner of a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banner(ctx):
    target = ctx.options.target or ctx.member
    target = await ctx.bot.rest.fetch_user(target.id)
    embed = hikari.Embed(title=f"Banner for {target.username}", description=None, color=(ctx.member.get_top_role().color if ctx.member != None else 0x2f3136))
    print(target.avatar_url)
    print(target.banner_url)
    print(target.accent_color)
    if target.banner_url != None:
        embed.set_image(target.banner_url)
    else:
        if target.accent_color == None:
            await ctx.respond("That user does not have banner or a accent color! (or discord didn't give me them)")
            return
        print(5)
        await ctx.respond("That person doesn't have a banner but their accent_color is " + str(target.accent_color))
        print(6)
        return
    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("name", "The name of the emoji", required=False)
@lightbulb.option("emoji", "The emoji you are going to steal", type=hikari.Emoji, required=True)
@lightbulb.command("steal", description="Steals a emoji :)", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand)
async def steal(ctx):
    guild = ctx.get_guild()
    print(type(ctx.options.emoji))
    emoji = await ctx.bot.rest.create_emoji(guild=guild, name=ctx.options.name, image=ctx.options.emoji.url)
    print(emoji)
    await ctx.respond(f"{emoji} Added {'animated ' if emoji.is_animated == True else ''}emoji {emoji.name}")

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("channel", "Where the logs will be posted", type=hikari.TextableGuildChannel)
@lightbulb.command("logging", description="Adds logging!", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def logging(ctx):
    channel_id = ctx.options.channel.id

@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("emoji", "The emoji for the ticket", type=hikari.Emoji, required=False)
@lightbulb.option("category", "The category for the ticket", type=hikari.GuildCategory, required=False)
@lightbulb.command("ticket", description="Creates a ticket message", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand)
async def ticket(ctx):
    ticket_message = await ctx.respond("React to create a ticket!")
    reaction_message = await ticket_message.message()
    emoji = ctx.options.emoji or "🎟️"
    try:
        reaction = await reaction_message.add_reaction(emoji)
    except:
        await ticket_message.edit(content="Invalided emoji or I can not access it.")
        return
    await ctx.event.message.delete()
    guild = ctx.get_guild()
    if ctx.options.category == None:
        category = await guild.create_category("tickets", reason="Automated ticket category created")
    while True:
        try:
            event = await ctx.bot.event_manager.wait_for(hikari.GuildReactionAddEvent, timeout=120)
        except asyncio.TimeoutError as e:
            break
        else:
            if reaction_message.id == event.message_id:
                if event.emoji_id == None:
                    if event.emoji_name != emoji: continue
                else:
                    if event.emoji_id != emoji: continue
                channel = await guild.create_text_channel(f"ticket_{ctx.user.username}", category=ctx.options.category.id or category.id,)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)