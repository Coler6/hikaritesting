import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context 
import traceback

plugin = lightbulb.Plugin("Events")
guild_id = 727195918180548728 # your guild
channel_id = 916801420525715536 # channel to be sent
owner_id = 674629871074279434 # owner of the bot

@plugin.listener(hikari.GuildUpdateEvent)
async def on_guild_update(event): #ban
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    old_guild = event.old_guild
    new_guild = event.guild
    embed = hikari.Embed(
        title="Channel updated",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    old_values = ""
    new_values = ""
    if old_guild.icon_hash != new_guild.icon_hash:
        icon_embed = hikari.Embed(
            title="Guild updated",
            description="Icon updated",
            color="0x00FFFF",
            timestamp=dt.datetime.now().astimezone(),
        )
        icon_embed.add_field("**Icon:**", new_guild.icon_url)
        icon_embed.set_image(new_guild.icon_url)
        await log_channel.send(embed=icon_embed)
    if old_guild.banner_hash != new_guild.banner_hash:
        banner_embed = hikari.Embed(
            title="Guild updated",
            description="Banner updated",
            color="0x00FFFF",
            timestamp=dt.datetime.now().astimezone(),
        )
        banner_embed.add_field("**Icon:**", new_guild.banner_url)
        await log_channel.send(embed=banner_embed)
    if old_guild.discovery_splash_hash != new_guild.discovery_splash_hash:
        banner_embed = hikari.Embed(
            title="Guild updated",
            description="Discovery splash updated",
            color="0x00FFFF",
            timestamp=dt.datetime.now().astimezone(),
        )
        banner_embed.add_field("**Icon:**", new_guild.discovery_splash_url)
        banner_embed.set_image(new_guild.discovery_splash_url)
        await log_channel.send(embed=banner_embed)
    if old_guild.splash_hash != new_guild.splash_hash:
        splash_embed = hikari.Embed(
            title="Guild updated",
            description="Invite splash updated",
            color="0x00FFFF",
            timestamp=dt.datetime.now().astimezone(),
        )
        disovery_embed.add_field("**Icon:**", new_guild.splash_url)
        disovery_embed.set_image(new_guild.splash_url)
        await log_channel.send(embed=splash_embed)
    if old_guild.name != new_guild.name:
        old_values += "\n**Name:** " + old_guild.name
        new_values += "\n**Name:** " + new_guild.name
    if old_guild.verification_level != new_guild.verification_level:
        old_values += "\n**Verification level:** " + str(old_guild.verification_level)
        new_values += "\n**Verification level:** " + str(new_guild.verification_level)
    if old_guild.description != new_guild.description:
        old_values += "\n**Description:** " + (old_guild.description if old_guild.description != None else "No description")
        new_values += "\n**Description:** " + (new_guild.description if new_guild.description != None else "No description")
    if old_guild.explicit_content_filter != new_guild.explicit_content_filter:
        old_values += "\n**Explicit content filter:** " + str(old_guild.explicit_content_filter)
        new_values += "\n**Explicit content filter:** " + str(new_guild.explicit_content_filter)
    if old_guild.public_updates_channel_id != new_guild.public_updates_channel_id:
        old_values += "\n**Public updates channel:** " + old_guild.get_channel(old_guild.public_updates_channel_id).mention
        new_values += "\n**Public updates channel:** " + new_guild.get_channel(new_guild.public_updates_channel_id).mention
    if old_guild.rules_channel_id != new_guild.rules_channel_id:
        old_values += "\n**Rules channel:** " + old_guild.get_channel(old_guild.rules_channel_id).mention
        new_values += "\n**Rules channel:** " + new_guild.get_channel(new_guild.rules_channel_id).mention
    if old_guild.system_channel_id != new_guild.system_channel_id:
        old_values += "\n**System channel:** " + old_guild.get_channel(old_guild.system_channel_id).mention
        new_values += "\n**System channel:** " + new_guild.get_channel(new_guild.system_channel_id).mention
    if old_values != "" and new_values != "":
        embed.add_field("Before", old_values, inline=True)
        embed.add_field("After", new_values, inline=True)
        await log_channel.send(embed=embed)

@plugin.listener(hikari.BanCreateEvent)
async def on_ban(event): #ban
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    user = event.user
    audit = await event.app.rest.fetch_audit_log(event.guild_id, event_type=22)
    for i in audit[0].entries.items():
        audit = i[1]
        break
    reason = audit.reason or None
    action_user = await audit.fetch_user()
    embed = hikari.Embed(
        title="Member banned", 
        description=user.mention + f" ({user.id})", 
        timestamp=dt.datetime.now().astimezone(), 
        color=(user.accent_color if user.accent_color != None else "0x000000")
    )
    embed.set_author(name=user.username, icon=user.avatar_url)
    if reason != None:
        embed.add_field("Reason", reason)
    embed.add_field("Action user", f"{action_user.username} ({action_user.id})")
    await log_channel.send(embed=embed)

@plugin.listener(hikari.BanDeleteEvent)
async def on_unban(event): #unban
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    user = event.user
    audit = await event.app.rest.fetch_audit_log(event.guild_id, event_type=23)
    for i in audit[0].entries.items():
        audit = i[1]
        break
    reason = audit.reason or None
    action_user = await audit.fetch_user()
    embed = hikari.Embed(
        title="Member unbanned", 
        description=user.mention + f" ({user.id})", 
        timestamp=dt.datetime.now().astimezone(), 
        color=(user.accent_color if user.accent_color != None else "0x000000")
    )
    embed.set_author(name=user.username, icon=user.avatar_url)
    if reason != None:
        embed.add_field("Reason", reason)
    embed.add_field("Action user", f"{action_user.username} ({action_user.id})")
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildJoinEvent)
async def on_bot_join(event): #Bot joins
    guild = event.guild
    owner = await event.app.rest.fetch_user(owner_id)
    embed =  hikari.Embed(
        title="Joined server",
        description=f"{guild.name} ({guild.id})",
        timestamp=dt.datetime.now().astimezone(),
        )
    embed.add_field("Members", guild.member_count)
    await owner.send(embed=embed)

@plugin.listener(hikari.GuildLeaveEvent)
async def on_bot_leave(event): #Bot leave
    guild = event.old_guild
    owner = await event.app.rest.fetch_user(owner_id)
    embed =  hikari.Embed(
        title="Left server",
        description=f"{guild.name} ({guild.id})",
        timestamp=dt.datetime.now().astimezone(),
        )
    embed.add_field("Members", guild.member_count)
    await owner.send(embed=embed)

@plugin.listener(hikari.GuildChannelCreateEvent)
async def on_channel_create(event): #Channel created
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    channel = event.channel
    embed = hikari.Embed(
        title="Channel created",
        description=f"{channel.name} ({channel.id})\n{channel.mention}", 
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.add_field("Type", channel.type)
    embed.add_field("Nsfw?", channel.is_nsfw)
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildChannelDeleteEvent)
async def on_channel_delete(event): #Channel deleted
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    channel = event.channel
    embed = hikari.Embed(
        title="Channel deleted",
        description=f"{channel.name} ({channel.id})", 
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.add_field("Type", channel.type)
    embed.add_field("Nsfw?", channel.is_nsfw)
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildChannelUpdateEvent)
async def on_channel_update(event): #Channel deleted
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    old_channel = event.old_channel
    new_channel = event.channel
    embed = hikari.Embed(
        title="Channel updated",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    old_values = ""
    new_values = ""
    if old_channel.name != new_channel.name: 
        old_values += "\n**Name:** " + old_channel.name
        new_values += "\n**Name:** " + new_channel.name
    if old_channel.is_nsfw != new_channel.is_nsfw:
        old_values += "\n**Nsfw?:** " + str(old_channel.is_nsfw)
        new_values += "\n**Nsfw?:** " + str(new_channel.is_nsfw)
    if old_channel.position != new_channel.position:
        old_values += "\n**Position:** " + str(old_channel.position)
        new_values += "\n**Position:** " + str(new_channel.position)
    if old_values != "" and new_values != "":
        embed.add_field("Before", old_values, inline=True)
        embed.add_field("After", new_values, inline=True)
    if old_channel.permission_overwrites != new_channel.permission_overwrites:
        print(old_channel.permission_overwrites)
        print(new_channel.permission_overwrites)
        for new_perm in new_channel.permission_overwrites.items():
            print("new")
            print(new_perm)
            for old_perm in old_channel.permission_overwrites.items():
                print("old")
                if new_perm[1].id != old_perm[1].id:
                    print("different ids")
                    continue
                if new_perm[1].allow == old_perm[1].allow and new_perm[1].deny == old_perm[1].deny:
                    print("both equal")
                    continue
                print(old_perm)
                new_perm_id = new_perm[1].id
                if new_perm[1].type.value == 0: # Role overwrite
                    role = guild.get_role(new_perm_id)
                    old_allow_perm = ""
                    new_allow_perm = ""
                    old_deny_perm = ""
                    new_deny_perm = ""
                    for e_new_perm in new_perm[1].allow:
                        print("new allow")
                        print(e_new_perm)
                        for e_old_perm in old_perm[1].allow:
                            print("old allow")
                            print(e_old_perm)
                            if e_new_perm == e_new_perm:
                                continue
                            old_allow_perm += str(e_old_perm) + " "
                            new_allow_perm += str(e_new_perm) + " "
                    for i_old_perm in old_perm[1].deny:
                        print("new deny")
                        print(i_old_perm)
                        for i_new_perm in new_perm[1].deny:
                            print("old deny")
                            print(i_new_perm)
                            if i_old_perm == i_new_perm:
                                continue
                            old_deny_perm += str(i_old_perm) + " "
                            new_deny_perm += str(i_new_perm) + " "
                    print("old allow\n" + old_allow_perm)
                    print("old deny\n" + old_deny_perm)
                    print("new allow\n" + new_allow_perm)
                    print("new deny\n" + new_deny_perm)
                    embed.add_field(f"Role permissions updated", f"{role.name} ({role.id})")
                    embed.add_field("Before", f"✅ {old_allow_perm}\n❎ {old_deny_perm}")
                    embed.add_field("After", f"✅ {new_allow_perm}\n❎ {new_deny_perm}")
                    print("role")
                elif new_perm[1].type.value == 1: # Member overwrite
                    member = guild.get_member(new_perm_id)
                    old_allow_perm = ""
                    new_allow_perm = ""
                    old_deny_perm = ""
                    new_deny_perm = ""
                    for new_perm in new_perm[1].allow:
                        print("new")
                        print(new_perm)
                        for old_perm in old_perm[1].allow:
                            print("old")
                            print(old_perm)
                            if old_perm == new_perm:
                                continue
                            old_allow_perm += str(old_perm) + " "
                            new_allow_perm += str(new_perm) + " "
                    for new_perm in new_perm[1].deny:
                        print("new")
                        print(new_perm)
                        for old_perm in old_perm[1].deny:
                            print("old")
                            print(old_perm)
                            if old_perm == new_perm:
                                continue
                            old_deny_perm += str(old_perm) + " "
                            new_deny_perm += str(new_perm) + " "
                    print("old allow\n" + old_allow_perm)
                    print("old deny\n" + old_deny_perm)
                    print("new allow\n" + new_allow_perm)
                    print("new deny\n" + new_deny_perm)
                    embed.add_field(f"Member permissions updated", f"{member.name} ({member.id})")
                    embed.add_field("Before", f"✅ {old_allow_perm}\n❎ {old_deny_perm}")
                    embed.add_field("After", f"✅ {new_allow_perm}\n❎ {new_deny_perm}")
                    print("member")
    await log_channel.send(embed=embed)

@plugin.listener(hikari.InviteCreateEvent)
async def on_invite_create(event): #Invite created
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    invite = event.invite
    invite_channel = event.get_channel()
    embed = hikari.Embed(
        title="Invite created",
        description="https://discord.gg/" + event.code,
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_author(name=invite.inviter.username, icon=invite.inviter.avatar_url)
    embed.add_field("Channel", invite_channel.mention)
    embed.add_field("Uses", f"{invite.uses}/{invite.max_uses}")
    if invite.is_temporary is True:
        embed.add_field("Temporary membership?", str(invite.is_temporary))
    if invite.expires_at != None:
        embed.add_field("Expires", str(invite.expires_at.strftime('%d/%m/%Y %H:%M:%S')))
    await log_channel.send(embed=embed)
    

@plugin.listener(hikari.InviteDeleteEvent)
async def on_invite_delete(event): #Invite deleted
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    invite = event.old_invite
    invite_channel = event.get_channel()
    embed = hikari.Embed(
        title="Invite deleted",
        description="https://discord.gg/" + event.code,
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_author(name=invite.inviter.username, icon=invite.inviter.avatar_url)
    embed.add_field("Channel", invite_channel.mention)
    embed.add_field("Uses", f"{invite.uses}/{invite.max_uses}")
    if invite.is_temporary is True:
        embed.add_field("Temporary membership?", str(invite.is_temporary))
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildMessageDeleteEvent)
async def on_message_delete(event): #Message deleted
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    message = event.old_message
    channel = guild.get_channel(message.channel_id)
    embed = hikari.Embed(
        title="Message deleted",
        description=f"In channel {channel.mention}",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_author(name=message.author.username, icon=message.author.avatar_url)
    embed.add_field("Content", message.content)
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildMessageUpdateEvent)
async def on_message_edit(event): #Message edited
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    message = event.old_message
    new_message = event.message
    channel = guild.get_channel(message.channel_id)
    embed = hikari.Embed(
        title="Message edited",
        description=f"In channel {channel.mention}",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_author(name=message.author.username, icon=message.author.avatar_url)
    embed.add_field("Before", message.content, inline=True)
    embed.add_field("After", new_message.content, inline=True)
    await log_channel.send(embed=embed)
    
@plugin.listener(hikari.GuildBulkMessageDeleteEvent)
async def on_message_purge(event): #Mass message deleted
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    message = event.old_message
    new_message = event.message
    channel = guild.get_channel(message.channel_id)
    embed = hikari.Embed(
        title="Messages purged",
        description=f"In channel {channel.mention}",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_author(name=message.author.username, icon=message.author.avatar_url)
    embed.add_field("Before", message.content, inline=True)
    embed.add_field("After", new_message.content, inline=True)
    await log_channel.send(embed=embed)
    
@plugin.listener(hikari.GuildReactionAddEvent)
async def on_reaction_add(event): #Reaction added
    pass

@plugin.listener(hikari.GuildReactionDeleteEvent)
async def on_reaction_remove(event): #Reaction removed
    pass

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_update(event): #Reaction removed
    pass

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)