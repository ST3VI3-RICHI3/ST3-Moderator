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
import Shared

class Whois(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None, type=None):
        if ctx.message.author.guild_permissions.administrator or member == None or ctx.message.author.id == member.id or ctx.author.id in Shared.Vars.devs:
            if member == None:
                member = ctx.message.author
            if type != None:
                if type.lower() == "avatar":
                    await ctx.send(member.avatar_url)
            else:
                embed=discord.Embed(title="Whois", description="Details of: {} ({})".format(member.name, member.id), color=0x00ff00)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="Username", value=str(member.name), inline=True)
                embed.add_field(name="ID", value=str(member.id), inline=True)
                if member.nick != None:
                    embed.add_field(name="Nickname", value=str(member.nick), inline=True)
                embed.add_field(name="Status", value=str(member.status), inline=True)
                embed.add_field(name="Joined server at", value=str(member.joined_at), inline=True)
                embed.add_field(name="Joined discord at", value=str(member.created_at), inline=True)
                embed.add_field(name="Highest role", value=str(member.top_role), inline=True)
                await ctx.send(embed=embed)
           
        else:
            await ctx.send(f":x: <@!{ctx.message.author.id}> You lack the required permissions to run this command")

def setup(bot):
    bot.add_cog(Whois(bot))