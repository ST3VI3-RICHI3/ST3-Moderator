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
    print("[Info] C_Annonce command successfully loaded.")
    bot.add_cog(C_Announce(bot))