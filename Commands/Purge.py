import discord
import asyncio
from discord.ext import commands

class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, Ammount: int):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            await ctx.channel.purge(limit=Ammount)
    
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): await ctx.send(f"Missing argument (`{error}`).")
        elif isinstance(error, commands.BadArgument): await ctx.send(f"Bad argument (`{error}`).")
        else: await ctx.send(error)

def setup(bot):
    bot.add_cog(Purge(bot))