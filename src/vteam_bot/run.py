# run.py

from .bot import bot
import dotenv
import os


def run():
    dotenv.load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)


run()
