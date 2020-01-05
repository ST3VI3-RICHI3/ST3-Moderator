import discord
import asyncio
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        devs = "169501254899335168"
        if str(ctx.message.author.id) in devs:
            msg = await ctx.send(":ok_hand: I am working!")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await msg.delete()

def setup(bot):
    print("[Info] Test command successfully loaded.")
    bot.add_cog(Test(bot))