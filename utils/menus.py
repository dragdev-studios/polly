import discord
from discord.ext.menus import Menu, button

N_ = "\N{variation selector-16}\N{combining enclosing keycap}"
NUMBERS = [str(n) + N_ for n in range(10)]
NUMBERS.append("\N{keycap ten}")


class ConfigMenuIndex(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    async def send_initial_message(self, ctx, channel):
        cursor = await ctx.bot.db.execute("SELECT prefix, channel, poll_roll, remove_reactions FROM configs WHERE id=?", (ctx.guild.id,))
        try:
            prefix, channel, role, remove = await cursor.fetchone()
        except ValueError:
            # what
            return
        embed = discord.Embed(
            title="Edit configuration - " + ctx.guild.id,
            description=f"{NUMBERS[0]} - Set prefix ("
        )
