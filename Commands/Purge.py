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