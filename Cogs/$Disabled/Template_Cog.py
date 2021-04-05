"""
    ST3-Moderator, a moderation bot for discord
    Copyright (C) 2021  ST3VI3 RICHI3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import discord
import asyncio
from discord.ext import commands

class Template(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Example(self, ctx): #Self must always be passed as a first paramater.
        print("This is an example command") #Bot command code goes here.

def setup(bot):
    bot.add_cog(Template(bot))