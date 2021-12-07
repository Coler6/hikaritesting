import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context
import traceback
plugin = lightbulb.Plugin("Misc")

def badges(badges):
    print("badges")
    if str(badges) == "NONE":
        return "No badges"
    badge_list = ""
    all_badges = {
        "BUG_HUNTER_LEVEL_1": "<:BugHunterLV1:916092123693064232>",
        "BUG_HUNTER_LEVEL_2": "<:BugHunterLV2:916092123885998181>",
        "DISCORD_CERTIFIED_MODERATOR": "<:DiscordCertifiedModerator:916098293023522927>", 
        "DISCORD_EMPLOYEE": "<:Employee:916092124137672804>",
        "EARLY_SUPPORTER": "<:EarlySupporter:916092123206516757>",
        "EARLY_VERIFIED_DEVELOPER": "<:EarlyVerifiedDeveloper:916097664255393802>",
        "HYPESQUAD_BALANCE": "<:HypeSquadBalance:916092123349143572>",
        "HYPESQUAD_BRAVERY": "<:HypeSquadBravery:916092122556420146>",
        "HYPESQUAD_BRILLIANCE": "<:HypeSquadBrillance:916092122652868629>",
        "HYPESQUAD_EVENTS": "<:HypeSquadEvents:916092123210715166>",
        "PARTNERED_SERVER_OWNER": "<:HypeSquadEvents:916092123210715166>",
    }
    print(badges)
    for badge in badges:
        badge_list = str(badge_list)
        badge_list = badge_list + all_badges[str(badge)]
    print(badge_list)
    return badge_list

@plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", description="Shows the info of a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
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
            color= ("0x000000"),
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
        fields = [("Name", str(target), True),
                    ("Discriminator", target.discriminator, True),
                    ("ID", target.id, True),
                    ("Bot?", target.is_bot, True),
                    ("Top role", top_role.mention if top_role.mention else '@everyone', True),
                    #("Status", str(target.status), True),
                    ("Presence", presence.visible_status if presence != None else "Offline" + presence.activities[0].name if presence != None else "Offline", True),
                    ("Created at", target.created_at.strftime('%d/%m/%Y %H:%M:%S'), True),
                    ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                    ("Boosted since", getattr(target.premium_since, "strftime", lambda x: "Not boosting")("%d/%m/%Y %H:%M:%S"), True),
                    ("Badges", badges(target.flags), True)
                    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.respond(embed=embed)

@plugin.command
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
    fields = [("ID", guild.id, True),
                ("Owner", owner, True),
                ("Created at", guild.created_at.strftime('%d/%m/%Y %H:%M:%S'), True),
                ("Boosts", str(f"{guild.premium_subscription_count if guild.premium_subscription_count != None else '0'} boost{'s' if guild.premium_subscription_count != 1 else ''} (level {guild.premium_tier.value})"), True),
                ("Members", len(guild.get_members()), True),
                ("Humans", len(list(filter(lambda m: not m.is_bot, list(guild.get_members().values())))), True),
                ("Bots", len(list(filter(lambda m: m.is_bot, list(guild.get_members().values())))), True),
                ("Banned members", len(await ctx.bot.rest.fetch_bans(guild)), True),
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
@lightbulb.option("target", "The user to get the banner.", hikari.User, required=False)
@lightbulb.command("banner", description="The banner of a user.", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banner(ctx):
    target = ctx.options.target or ctx.member
    color = target.get_top_role().color
    target = await ctx.bot.rest.fetch_user(target.id)
    embed = hikari.Embed(title=f"Banner for {target.username}", description=None, color=color)
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
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("channel", "Where the logs will be posted", type=hikari.TextableGuildChannel)
@lightbulb.command("logging", description="Adds logging!", auto_defer=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def logging(ctx):
    channel_id = ctx.options.channel.id

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)