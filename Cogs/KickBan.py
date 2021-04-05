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

class KickBan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, user: discord.Member = None, *, Reason: str = "No reason provided"):
        if ctx.message.author.guild_permissions.administrator:
            if user == None:
                msg = await ctx.send(":x: Missing arg: `User`")
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
            else:
                msg = await ctx.send(":ballot_box_with_check:<@{}> was kicked for: {}".format(user.id, Reason))
                await user.kick(reason=Reason)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()

    @commands.command()
    async def ban(self, ctx, user: discord.Member = None, *, Reason: str = "No reason provided"):
        if ctx.message.author.guild_permissions.administrator:
            if user == None:
                msg = await ctx.send(":x: Missing arg: `User`")
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
            else:
                msg = await ctx.send(":ballot_box_with_check:<@{}> was banned for: {}".format(user.id, Reason))
                await user.ban(reason=Reason)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()

def setup(bot):
    bot.add_cog(KickBan(bot))
