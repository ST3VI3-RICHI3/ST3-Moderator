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