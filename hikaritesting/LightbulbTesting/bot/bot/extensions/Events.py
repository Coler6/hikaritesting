import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context 
import traceback
from bot.bot.utils import conv, image


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
        splash_embed.add_field("**Icon:**", new_guild.splash_url)
        splash_embed.set_image(new_guild.splash_url)
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
        color=(user.accent_color if user.accent_color != None else "0x00FFFF")
    )
    embed.set_author(name=user.username, icon=user.avatar_url)
    if reason != None:
        embed.add_field("Reason", reason)
    embed.add_field("Action author", f"{action_user.username} ({action_user.id})")
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
        color=(user.accent_color if user.accent_color != None else "0x00FFFF")
    )
    embed.set_author(name=user.username, icon=user.avatar_url)
    if reason != None:
        embed.add_field("Reason", reason)
    embed.add_field("Action author", f"{action_user.username} ({action_user.id})")
    await log_channel.send(embed=embed)

@plugin.listener(hikari.MemberCreateEvent)
async def on_member_join(event): #member joins
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    member = event.member
    embed =  hikari.Embed(
        title="Member joined",
        description=f"{member.display_name} ({member.id})",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_thumbnail(member.avatar_url)
    await log_channel.send(embed=embed)

@plugin.listener(hikari.MemberDeleteEvent)
async def on_member_leave(event): #member joins
    if event.guild_id != guild_id:
        return
    log_channel = event.get_guild().get_channel(channel_id)
    member = event.old_member
    embed =  hikari.Embed(
        title="Member left",
        description=f"{member.display_name} ({member.id})",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.set_thumbnail(member.avatar_url)
    await log_channel.send(embed=embed)

@plugin.listener(hikari.MemberUpdateEvent)
async def on_member_update(event):
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    old_member = event.old_member
    member = event.member
    if old_member.nickname != member.nickname:
        embed =  hikari.Embed(
            title="Member nickname updated",
            timestamp=dt.datetime.now().astimezone(),
            color="0x00FFFF"
        )
        embed.set_author(name=member.username, icon=member.avatar_url)
        embed.add_field("Before:", str(old_member.nickname), inline=True)
        embed.add_field("After:", str(member.nickname), inline=True)
        await log_channel.send(embed=embed)
    if set(old_member.role_ids) != set(member.role_ids):
        roles_removed = list(set(old_member.role_ids) - set(member.role_ids))
        roles_added = list(set(member.role_ids) - set(old_member.role_ids))
        embed =  hikari.Embed(
            title="Member roles updated",
            timestamp=dt.datetime.now().astimezone(),
            color="0x00FFFF"
        )
        embed.set_author(name=member.username, icon=member.avatar_url)
        if roles_added != []:
            roles = ""
            for role in roles_added:
                roles += guild.get_role(role).mention + " "
            embed.add_field("Added:", roles, inline=True)
        if roles_removed != []:
            roles = ""
            for role in roles_removed:
                roles += guild.get_role(role).mention + " "
            embed.add_field("Removed:", roles, inline=True)
        await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildJoinEvent)
async def on_bot_join(event): #Bot joins
    guild = event.guild
    owner = await event.app.rest.fetch_user(owner_id)
    embed =  hikari.Embed(
        title="Joined server",
        description=f"{guild.name} ({guild.id})",
        color="0x00FFFF",
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
        color="0x00FFFF",
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
        color="0x00FFFF",
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
        color="0x00FFFF",
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
        description=new_channel.mention,
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
        overwrite_add = set(new_channel.permission_overwrites) - set(old_channel.permission_overwrites) # add
        overwrite_remove = set(old_channel.permission_overwrites) - set(new_channel.permission_overwrites) # remove
        for _perm in new_channel.permission_overwrites:
            if _perm in overwrite_add or _perm in overwrite_remove: # It will continue if overwrite has just been added or removed
                continue
            perm = new_channel.permission_overwrites.get(_perm)
            old_perm = old_channel.permission_overwrites.get(_perm)
            new_allow = set(perm.allow) - set(old_perm.allow)
            new_deny = set(perm.deny) - set(old_perm.deny)
            old_allow = set(old_perm.allow) - set(perm.allow)
            old_deny = set(old_perm.deny) - set(perm.deny)
            for permission in new_allow:
                embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", f"{'⬜' if permission not in old_allow and permission not in old_deny else '❎'} -> ✅", inline=True)
            for permission in new_deny:
                embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", f"{'⬜' if permission not in old_allow and permission not in old_deny else '✅'} -> ❎", inline=True)
            for permission in old_allow:
                if permission in new_allow or permission in new_deny:
                    continue
                embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", f"✅ -> ⬜", inline=True)
            for permission in old_deny:
                if permission in new_allow or permission in new_deny:
                    continue
                embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", f"❎ -> ⬜", inline=True)
            print(new_allow)
            print(new_deny)
            print(old_allow)
            print(old_deny)
        if overwrite_add != ():
            for permission in overwrite_add:
                overwrite_embed = hikari.Embed(
                    title="Channel overrides updated",
                    description=new_channel.mention,
                    color="0x00FFFF",
                    timestamp=dt.datetime.now().astimezone(),
                )
                perm = new_channel.permission_overwrites.get(permission)
                print(perm)
                if perm.type.value == 0: # Role overwrite
                    overwrite_embed.add_field("Added role overwrites", guild.get_role(perm.id).mention)
                if perm.type.value == 1: # Member overwrite
                    overwrite_embed.add_field("Added member overwrites", guild.get_member(perm.id).mention)
                if str(perm.allow) != "NONE":
                    overwrite_embed.add_field("Allow:", str(perm.allow).replace("|", " | "))
                if str(perm.deny) != "NONE":
                    overwrite_embed.add_field("Deny:", str(perm.deny).replace("|", " | "))
                await log_channel.send(embed=overwrite_embed)
        if overwrite_remove != ():
            for permission in overwrite_remove:
                print(permission)
                overwrite_embed = hikari.Embed(
                    title="Channel overwrites updated",
                    description=new_channel.mention,
                    color="0x00FFFF",
                    timestamp=dt.datetime.now().astimezone(),
                )
                perm = old_channel.permission_overwrites.get(permission)
                print(perm)
                if perm.type.value == 0: # Role overwrite
                    overwrite_embed.add_field("Removed role overwrites", guild.get_role(perm.id).mention)
                if perm.type.value == 1: # Member overwrite
                    overwrite_embed.add_field("Removed member overwrites", guild.get_member(perm.id).mention)
                if str(perm.allow) != "NONE":
                    overwrite_embed.add_field("Allow:", str(perm.allow).replace("|", " "))
                if str(perm.deny) != "NONE":
                    overwrite_embed.add_field("Deny:", str(perm.deny).replace("|", " "))
                await log_channel.send(embed=overwrite_embed)
    if embed.fields != []:
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
        color="0x00FFFF",
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
        color="0x00FFFF",
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
    embed = hikari.Embed(
        title="Message deleted",
        description=f"In channel <#{event.channel_id}>",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    log = await event.app.rest.fetch_audit_log(event.guild_id, event_type=72)
    for i in log[0].entries.items():
        print(i)
        log = i[1]
        break
    action_user = await log.fetch_user()
    if message == None:
        embed.add_field("ID", str(event.message_id))
        embed.add_field("Uh oh!", "Discord didn't give me the message!")
    else:
        print(log)
        print(message)
        print(action_user)
        embed.set_author(name=message.author.username, icon=message.author.avatar_url)
        embed.add_field("ID", str(event.message_id))
        embed.add_field("Content", message.content)
        if message.author.id == log.target_id:
            print("equal :D")
            embed.add_field("Action author", f"{action_user.username} ({action_user.id})")
        else:
            print("Not equal :(")
            embed.add_field("Action author", f"{message.author.username} ({message.author.id})")
    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildMessageUpdateEvent)
async def on_message_edit(event): #Message edited
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    message = event.old_message
    new_message = event.message
    print(message)
    print(new_message)
    print(message.content)
    print(new_message.content)
    if message.content == None or new_message.content == None:
        return
    if message.content == new_message.content:
        return
    channel = guild.get_channel(message.channel_id)
    embed = hikari.Embed(
        title="Message edited",
        description=f"In channel {channel.mention}",
        color="0x00FFFF",
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
    messages = event.old_messages
    channel = event.get_channel()
    embed = hikari.Embed(
        title="Messages purged",
        description=f"In channel {channel.mention}",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    embed.add_field("Amount", len(messages), inline=True)
    await log_channel.send(embed=embed)
    
@plugin.listener(hikari.RoleCreateEvent)
async def on_role_create(event): #Role added
    if event.guild_id != guild_id:
        return
    guild = await event.app.rest.fetch_guild(event.guild_id)
    log_channel = guild.get_channel(channel_id)
    role = event.role
    embed = hikari.Embed(
        title="Role created",
        description=role.mention,
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    await log_channel.send(embed=embed)

@plugin.listener(hikari.RoleDeleteEvent)
async def on_role_delete(event): #Role deleted
    if event.guild_id != guild_id:
        return
    guild = await event.app.rest.fetch_guild(event.guild_id)
    log_channel = guild.get_channel(channel_id)
    role = event.old_role
    embed = hikari.Embed(
        title="Role deleted",
        description=f"{role.mention} ({role.name})",
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    await log_channel.send(embed=embed)

@plugin.listener(hikari.RoleUpdateEvent)
async def on_role_updated(event): #Role updaed
    if event.guild_id != guild_id:
        return
    guild = await event.app.rest.fetch_guild(event.guild_id)
    log_channel = guild.get_channel(channel_id)
    new_role = event.role
    old_role = event.old_role
    embed = hikari.Embed(
        title="Role updated",
        description=new_role.mention,
        color="0x00FFFF",
        timestamp=dt.datetime.now().astimezone(),
    )
    old_values = ""
    new_values = ""
    if old_role.name != new_role.name: 
        old_values += "\n**Name:** " + old_role.name
        new_values += "\n**Name:** " + new_role.name
    if old_role.position != new_role.position:
        old_values += "\n**Position:** " + str(old_role.position)
        new_values += "\n**Position:** " + str(new_role.position)
    if old_role.color != new_role.color:
        old_values += "\n**Color:** " + str(old_role.color)
        new_values += "\n**Color:** " + str(new_role.color)
    if old_role.unicode_emoji != new_role.unicode_emoji:
        old_values += "\n**Emoji:** " + str(old_role.unicode_emoji)
        new_values += "\n**Emoji:** " + str(new_role.unicode_emoji)
    if old_role.icon_url != new_role.icon_url:
        old_values += "\n**Icon:** " + str(old_role.icon_url)
        new_values += "\n**Icon:** " + str(new_role.icon_url)
    if old_role.is_hoisted != new_role.is_hoisted:
        old_values += "\n**Display separately:** " + str(old_role.is_hoisted)
        new_values += "\n**Display separately:** " + str(new_role.is_hoisted)
    if old_role.is_mentionable != new_role.is_mentionable:
        old_values += "\n**Mentionable:** " + str(old_role.is_mentionable)
        new_values += "\n**Mentionable:** " + str(new_role.is_mentionable)
    if old_values != "" and new_values != "":
        embed.add_field("Before", old_values, inline=True)
        embed.add_field("After", new_values, inline=True)
    if old_role.permissions != new_role.permissions:
        perm_embed = hikari.Embed(
            title="Role permissions updated",
            description=new_role.mention,
            timestamp=dt.datetime.now().astimezone(),
        )
        new_perms = new_role.permissions
        old_perms = old_role.permissions
        new_perm = set(new_perms) - set(old_perms)
        old_perm = set(old_perms) - set(new_perms)
        for permission in new_perm:
            perm_embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", "❎ -> ✅", inline=True)
        for permission in old_perm:
            perm_embed.add_field(f"{(str(permission.name).lower()).replace('_', ' ').replace(str(permission.name)[0].lower(), str(permission.name)[0], 1)}:", "✅ -> ❎", inline=True)
        print(new_perm)
        print(old_perm)
        await log_channel.send(embed=perm_embed)
    if embed.fields != []:
        await log_channel.send(embed=embed)

@plugin.listener(hikari.EmojisUpdateEvent)
async def on_emojis_update(event): #Emoji updated, deleted, created
    if event.guild_id != guild_id:
        return
    guild = event.get_guild()
    log_channel = guild.get_channel(channel_id)
    old_emojis = event.old_emojis
    new_emojis = event.emojis
    created_emojis = set(new_emojis) - set(old_emojis)
    deleted_emojis = set(old_emojis) - set(new_emojis)
    if created_emojis != ():
        for emoji in created_emojis:
            print(type(emoji.user))
            embed = hikari.Embed(
                title="Emoji created",
                color="0x00FFFF",
                description=conv.msg_emoji(emoji) + "\n" + emoji.id,
                timestamp=dt.datetime.now().astimezone(),
            )
            embed.add_field("Name:", emoji.name)
            embed.set_image(emoji.url)
            if emoji.user != None:
                embed.set_author(name=emoji.user.display_name, icon=emoji.user.avatar_url)
            if embed.fields != []:
                await log_channel.send(embed=embed)
            break
    if deleted_emojis != ():
        embed = hikari.Embed(
            title="Emoji deleted",
            color="0x00FFFF",
            timestamp=dt.datetime.now().astimezone(),
        )
        for emoji in deleted_emojis:
            embed.add_field("Name:", emoji.name)
            embed.set_image(emoji.url)
            if emoji.user != None:
                embed.set_author(name=emoji.user.display_name, icon=emoji.user.avatar_url)
            break
        if embed.fields != []:
            await log_channel.send(embed=embed)
    for emoji in new_emojis:
        for o_emoji in old_emojis:
            if emoji.id == o_emoji.id:
                if emoji.name != o_emoji.name:
                    embed = hikari.Embed(
                        title="Emoji updated",
                        description=conv.msg_emoji(emoji),
                        color="0x00FFFF",
                        timestamp=dt.datetime.now().astimezone(),
                    )
                    embed.add_field("Before", o_emoji.name)
                    embed.add_field("After", emoji.name)
                    await log_channel.send(embed=embed)

@plugin.listener(hikari.GuildReactionAddEvent)
async def on_reaction_add(event): #Reaction added
    pass

@plugin.listener(hikari.GuildReactionDeleteEvent)
async def on_reaction_remove(event): #Reaction removed
    pass

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_update(event): #Voice updated
    pass

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)