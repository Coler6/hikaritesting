from bot.bot.Bot import Bot
from bot import __version__

import os

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
