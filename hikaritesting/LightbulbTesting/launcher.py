from bot.bot.Bot import BotMain
from bot import __version__
from bot.bot import Bot

import os

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    bot = BotMain()
    bot.run()
