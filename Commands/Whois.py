import discord
import asyncio
from discord.ext import commands

class Whois(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        if ctx.message.author.guild_permissions.administrator or member == None or ctx.message.author.id == member.id:
            if member == None:
                member = ctx.message.author
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
            ctx.send(":x: {} You lack the required permissions to run this command".format(ctx.message.author.id))

def setup(bot):
    bot.add_cog(Whois(bot))