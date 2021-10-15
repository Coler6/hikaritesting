import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt

class Misc(lightbulb.Plugin):
    def __init__(self):
        super().__init__()
    
    @lightbulb.command(name="userinfo", aliases=("ui"))
    async def userinfo(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
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

def load(bot: Bot) -> None:
    bot.add_plugin(Misc())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Misc")