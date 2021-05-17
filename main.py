#!./venv/bin/python3
from colorama import init, Fore
from polly.bot import PollyBot

init(True)

print(Fore.GREEN + "Starting PollyBot\r", end="")
bot = PollyBot()
bot.run()
