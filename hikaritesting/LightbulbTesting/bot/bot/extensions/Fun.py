from __future__ import annotations

import lightbulb
import hikari
from bot.bot import Bot
import logging
from lightbulb import commands, context
import random
# from bot.bot.memes import Meme
plugin = lightbulb.Plugin("Fun")


#    """Shows a pic of some cute goats."""
#    p = []
#    for photos in os.listdir("./bot/bot/extensions"):
#        p.append(photos)
#    await ctx.respond(random.choice(p))

@plugin.command
@lightbulb.command(name="ping", description="Pong!")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def ping(ctx: context.Context) -> None:
    await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

@plugin.command
@lightbulb.option("subreddit", "Choose wholesomememes, memes, or dankmemes to get your meme from.", choices=["wholesomememes", "memes", "dankmemes"], required=False)
@lightbulb.command(name="memes", description="Shows a meme!", aliases=["meme"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def memes(ctx):
        subreddits = ctx.options.subreddits or None
        if subreddits == "wholesomememes":
            sub = "wholesomememes"
        if subreddits == "memes":
            sub = "memes"
        if subreddits == "dankmemes":
            sub = "dankmemes"
        if subreddits == None:
            reddits = 'wholesomememes','memes','dankmemes'
            sub = random.choice(reddits)
        submission = Meme.rando_meme(sub)
        embed = hikari.Embed(title=f'{sub}', description=f"{submission.title}", color=0xff0000).set_image(submission.url)
        await ctx.respond(embed=embed)

@plugin.command
@lightbulb.command(name="goat", description="Shows a goat!",)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def goat(ctx) -> None:
    """Shows a pic of some cute goats."""
    responses = ["https://i.imgur.com/GaPoxOD.jpg",
                "https://i.imgur.com/Sb7aaeA.jpg",
                "https://i.imgur.com/XRZFBUQ.jpg",
                "https://i.imgur.com/GYtW2rj.jpg",
                "https://i.imgur.com/wBVcBy2.jpg",
                "https://i.imgur.com/bh1rjHU.jpg",
                "https://i.imgur.com/nWtjVb7.jpg",
                "https://i.imgur.com/sMHl52t.jpg",
                "https://i.imgur.com/43EKJqB.jpg",
                "https://i.imgur.com/VmzPmOd.jpg",
                "https://i.imgur.com/GYtW2rj.jpg",
                "https://i.imgur.com/SMvWukk.jpg",
                "https://i.imgur.com/EjDdZUF.jpg",
                "https://i.imgur.com/1jE0hQZ.jpg",
                "https://i.imgur.com/G4tAGGq.jpg",
                "https://i.imgur.com/bEkgXeX.jpg",
                "https://i.imgur.com/hGatqXD.jpg",
                "https://i.imgur.com/iLcF3dI.jpg",
                "https://i.imgur.com/lbD1ULo.jpg",
                "https://i.imgur.com/HLphakw.jpg",
                "https://i.imgur.com/EVMNhq3.jpg",
                "https://i.imgur.com/i8obDzJ.jpg",
                "https://i.imgur.com/fS8UVaG.jpg",
                "https://i.imgur.com/vQdh5eL.jpg",
                "https://i.imgur.com/EkqJG5m.jpg",
                "https://i.imgur.com/RnHej9b.jpg",
                "https://i.imgur.com/4tr2OPW.jpg",
                "https://i.imgur.com/to9mALS.jpg",
                "https://i.imgur.com/BZkNTDG.jpg",
                "https://i.imgur.com/zHCmO6q.jpg",
                "https://i.imgur.com/cd6vYSC.jpg",
                "https://i.imgur.com/g96nPYf.jpg",
                "https://i.imgur.com/vWq4Q2x.jpg",
                "https://i.imgur.com/2fHDgJf.jpg",
                "https://i.imgur.com/u2ghRCK.jpg",
                "https://i.imgur.com/zK8ur8t.jpg",
                "https://i.imgur.com/ec350EO.jpg",
                "https://i.imgur.com/FL2nUQz.jpg",
                "https://i.imgur.com/KaHM9ZS.jpg",
                "https://i.imgur.com/2p9r7YG.jpg",
                "https://i.imgur.com/4LuhRoW.jpg",
                "https://i.imgur.com/RQmPVLE.jpg",
                "https://i.imgur.com/9drPkys.jpg",
                "https://i.imgur.com/qW9J550.jpg",
                "https://i.imgur.com/2ThV2Of.jpg",
                "https://i.imgur.com/9ucdAuz.jpg",
                "https://i.imgur.com/tJXlOPV.jpg",
                "https://i.imgur.com/htW5PLI.jpg",
                "https://i.imgur.com/qzQtY4O.jpg",
                "https://i.imgur.com/K2DkcDw.jpg",
                "https://i.imgur.com/jVqdXRj.jpg",
                "https://i.imgur.com/Ziukby7.jpg",
                "https://i.imgur.com/jGFoA5e.jpg",
                "https://i.imgur.com/uZpogzn.jpg",
                "https://i.imgur.com/9iAnJ6L.jpg",
                "https://i.imgur.com/y3XU87y.jpg",
                "https://i.imgur.com/tDUheKs.jpg"]
    await ctx.respond(random.choice(responses), reply=True)

@plugin.command
@lightbulb.option("animal", "Choose what animal.", choices=["dog", "cat", "panda", "fox", "bird", "koala"], required=True)
@lightbulb.command(name="fact", description="Shows a random fact and a image of either a dog, cat, panda, fox, bird, or koala.",)
@lightbulb.implements(commands.PrefixCommand)
async def fact(ctx):
    """Shows a random fact and a image of either a dog, cat, panda, fox, bird, or koala."""
    animal = ctx.options.animal
    if (animal == animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
        fact_url = f"https://some-random-api.ml/facts/{animal}"
        image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]

            else:
                image_link = None

        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = Embed(title=f"{animal.title()} fact",
                                description=data["fact"],
                                color=ctx.author.color)
                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status")

    else:
        await ctx.send("No facts are available for that animal.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


