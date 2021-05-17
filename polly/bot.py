from pathlib import Path
from json import load

import discord
from tabulate import tabulate
from aiosqlite import connect, Connection
from discord.ext import commands
from discord.ext.commands.core import command
from colorama import Fore


class PollyBot(commands.Bot):
    """PollyBot modified discord.ext.commands.Bot class."""
    def __init__(self, **options):
        super().__init__(
            description="PollyBot - the last poll bot you'll need!",
            command_prefix=self._prefix,
            strip_after_prefix=True,
            **options
        )
        self.cwd = Path(__file__).parent.parent  # have to parent twice to get top-level dir
        self.db = None
        self.loop.run_until_complete(self._init_db())

        with open(self.cwd / "config.json") as cfg:
            self.config = load(cfg)
    
    async def _init_db(self):
        self.db = await connect(self.cwd / "database.sqlite3")
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                channel INT NOT NULL,
                choices TEXT NOT NULL,
                message INT NOT NULL UNIQUE,
                expire TEXT NOT NULL
            );
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
                id INT NOT NULL PRIMARY KEY UNIQUE,
                prefix TEXT DEFAULT 'p!',
                channel INT DEFAULT NULL,
                poll_roll INT DEFAULT NULL,
                remove_reactions INT DEFAULT 0
            );
            """
        )
    
    async def _prefix(self, bot, message: discord.Message):
        bot: PollyBot
        if not message.guild:
            return commands.when_mentioned_or("p!")(bot, message)
        
        cursor = await self.db.execute("SELECT prefix FROM configs WHERE id=?;", (message.guild.id,))
        row = await cursor.fetchone()
        if not row:
            row = ("p!",)
        return commands.when_mentioned_or(*row)(bot, message)
    
    async def on_connect(self):
        print(Fore.GREEN + "[re]connected to discord!")
    
    async def on_disconnect(self):
        print(Fore.RED + "disconnected from discord!")

    async def on_ready(self):
        table = tabulate(
            (
                ("Guilds", len(self.guilds)),
                ("Channels", len(tuple(self.get_all_channels()))),
                ("Users", len(self.users)),
                ("Emojis", len(self.emojis)),
                ("DMs", len(self.private_channels)),
                ("Latency", str(round(self.latency*1000, 2)) + "ms"),
                ("Cogs", len(self.cogs)),
                ("Commands", len(self.walk_commands()))
            ),
            tablefmt="fancy_grid"
        )
        print(Fore.CYAN + table)
    
    async def close(self):
        try:
            await self.db.close()
        except Exception:
            print("Refusing to shut down as database closing failed!")
            raise
        await super().close()
    
    def run(self):
        super().run(self.config["token"])
