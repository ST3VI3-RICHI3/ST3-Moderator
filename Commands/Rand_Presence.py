import discord
import asyncio
import random
from discord.ext import commands, tasks

presance_overridden = False

class Rand_Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(name="for " + self.bot.command_prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
        print("\r[Info] Bot loaded [100%]", end = "\n")
        print("[Info] Bot running.")
        await self.randomPresanceChange()

    async def randomPresanceChange(self):
        rand_watching = ['for {}'.format(self.bot.command_prefix), 'Dead By Daylight', 'the server', 'YouTube', 'Dark Souls Remastered', 'for {}help'.format(self.bot.command_prefix), 'commands', 'for messages starting with \'{}\''.format(self.bot.command_prefix), 'for urban', 'for you']
        global presance_overridden
        #while not stopping and not presance_overridden:
        while not presance_overridden:
            await asyncio.sleep(60)
            #if not stopping and not presance_overridden:
            if not presance_overridden:
                await self.bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)

    @commands.command()
    async def status(self, ctx, time, Type, *, Name):
        devs = "169501254899335168"
        if str(ctx.message.author.id) == devs:
            global presance_overridden
            presance_overridden = True
            if Type == "playing":
                Type = discord.ActivityType.playing
            elif Type == "watching":
                Type = discord.ActivityType.watching
            elif Type == "listening":
                Type = discord.ActivityType.listening
            elif tpye == "streaming":
                tpye = discord.ActivityType.streaming
            elif Type == "unknown":
                Type = discord.ActivityType.unknown
            else:
                Type = discord.ActivityType.playing
            await self.bot.change_presence(activity=discord.Activity(name=Name, type=Type), status=discord.Status.online, afk=False)
            print("presance updated to: " + str(Type) + " " + Name + " (" + time + "s)")
            try:
                await ctx.message.delete()
            except:
                print("Was not able to delete status command.")
            try:
                time = int(time)
                await asyncio.sleep(time)
                await self.bot.change_presence(activity=discord.Activity(name="for " + prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
                presance_overridden = False
                await randomPresanceChange()
            except:
                presance_overridden = False
                await self.randomPresanceChange()
                msg = ctx.send(":x: Invalid arg given: time.")
                await asyncio.sleep(5)
                await msg.delete()
        else:
            msg = ctx.send(":x: You do not have the required permissions to run this command.")
            await asyncio.sleep(5)
            await msg.delete()

def setup(bot):
    print("[Info] Random Presance module successfully loaded.") #This is a small indicator to show the bot has found the cog.
    bot.add_cog(Rand_Presence(bot))