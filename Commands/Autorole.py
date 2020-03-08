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
from discord.ext import commands

class Autorole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ARole: discord.role = None
        Guilds = Shared.Database.Load("Guilds.json")
        if str(member.guild.id) in Guilds:
            if Guilds[str(member.guild.id)]["AutoroleID"] and Guilds[str(member.guild.id)]["AutoroleID"] != None:
                ARole = Guilds[str(member.guild.id)]["AutoroleID"]
                ARole = member.guild.get_role(ARole)
                await member.add_roles(ARole)

    @commands.command(aliases=["SetAutorole"])
    async def setautorole(self, ctx, role: discord.Role = None):
        if ctx.message.author.guild_permissions.administrator:
            Guilds = Shared.Database.Load("Guilds.json")
            if str(ctx.message.guild.id) not in Guilds:
                Guilds[str(ctx.message.guild.id)] = {}
                Guilds[str(ctx.message.guild.id)]["Mute_Role"] = None
                Guilds[str(ctx.message.guild.id)]["Mute_Ban_On_Leave"] = False
                Guilds[str(ctx.message.guild.id)]["AutoroleID"] = None
                Shared.Database.dump("Guilds.json", Guilds)
            if Guilds[str(ctx.message.guild.id)]["AutoroleID"] == None:
                if role == None:
                    await ctx.send(":x: Autorole is already disabled.")
                else:
                    await ctx.send(":white_check_mark: Set aturole role.")
                    Guilds[str(ctx.message.guild.id)]["AutoroleID"] = role.id
                    Shared.Database.dump("Guilds.json", Guilds)
            else:
                if role == None:
                    await ctx.send(":white_check_mark: Disabled autorole.")
                    Guilds[str(ctx.message.guild.id)]["AutoroleID"] = None
                    Shared.Database.dump("Guilds.json", Guilds)
                else:
                    await ctx.send(":white_check_mark: Updated aturole role.")
                    Guilds[str(ctx.message.guild.id)]["AutoroleID"] = role.id
                    Shared.Database.dump("Guilds.json", Guilds)


def setup(bot):
    bot.add_cog(Autorole(bot))