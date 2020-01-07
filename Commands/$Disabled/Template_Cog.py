import discord
import asyncio
from discord.ext import commands

class Template(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Example(self, ctx): #Self must always be passed as a first paramater.
        print("This is an example command") #Bot command code goes here.

def setup(bot):
    print("[Info] Template cog successfully loaded.") #This is a small indicator to show the bot has found the cog.
    bot.add_cog(Template(bot))