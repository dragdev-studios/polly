# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Config(commands.Cog):
    """Cog containing commands related to configuration."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cfg", aliases=["config", "settings"])
    


def setup(bot):
    bot.add_cog(Test(bot))
