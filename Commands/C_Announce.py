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
from discord.ext import commands

class C_Announce(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def C_Announce(self, ctx, *, message = ""):
        if ctx.message.author.guild_permissions.administrator:
            if message == "":
                msg = await ctx.send(":x:Error: Noting to announce.")
                asyncio.sleep(5)
                msg.delete()
            else:
                await ctx.message.delete()
                await ctx.send("@everyone Channel announcement: {}".format(message))
        else:
            msg = await ctx.send(":warning:WARNING:warning: <@{}> has invalid permissions.".format(ctx.message.author.id))
            asyncio.sleep(10)
            ctx.message.delete()
            msg.delete()

def setup(bot):
    bot.add_cog(C_Announce(bot))