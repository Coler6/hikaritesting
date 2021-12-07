import hikari
import lightbulb
from bot.bot import Bot
import typing as t
import datetime as dt
from lightbulb import commands, context
import traceback
plugin = lightbulb.Plugin("Image")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)