"""
ST3-Moderator, a moderation bot for discord
    Copyright (C) 2020  ST3VI3 RICHI3

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
import Shared
from Shared import Output
from discord.ext import commands

class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, Ammount: int):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            await ctx.channel.purge(limit=Ammount)
            msg = await ctx.send(f"Purged {Ammount} messages!")
            await asyncio.sleep(5)
            await msg.delete()
    
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): await ctx.send(f"Missing argument (`{error}`).")
        elif isinstance(error, commands.BadArgument): await ctx.send(f"Bad argument (`{error}`).")
        else: Output(Type="Error", Msg=f"Purge error, {str(error)}")

def setup(bot):
    bot.add_cog(Purge(bot))