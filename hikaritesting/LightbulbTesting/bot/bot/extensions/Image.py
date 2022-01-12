import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context
from bot.bot.utils import db, image 

plugin = lightbulb.Plugin("Image")



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)