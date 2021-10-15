from bot.bot.Bot import Bot
from bot import __version__
from lavastart import lavarun
import os

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    lavarun.run2()
    bot = Bot()
    bot.run()