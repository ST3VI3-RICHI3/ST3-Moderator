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

class Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, func = None, User: discord.Member = None, role: discord.Role = None):
        if ctx.message.author.guild_permissions.administrator:
            if User != None:
                if Role != None:
                    if func.lower() == "add":
                        try:
                            await User.add_roles(role)
                            msg = await ctx.send(":thumbsup: added role!")
                            await asyncio.sleep(5)
                            await msg.delete()
                            try: await ctx.message.delete()
                            except: pass
                        except: await ctx.send("There was an error doing that.")
                    elif func.lower() == "remove":
                        try:
                            await User.remove_roles(role)
                            msg = await ctx.send(":thumbsup: removed role!")
                            await asyncio.sleep(5)
                            await msg.delete()
                            try: await ctx.message.delete()
                            except: pass
                        except: await ctx.send("There was an error doing that.")
                else: await ctx.send("Missing or invalid arguement, `func` (Function). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
            else: await ctx.send("Missing or invalid arguement, `role` (@Role_To_Act_On). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
        else: await ctx.send("Missing or invalid arguement, `User` (@User_Mention). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")

def setup(bot):
    bot.add_cog(Role(bot))
