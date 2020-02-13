import discord
import asyncio
import random
import Shared
from Shared import Output
from discord.ext import commands, tasks

class Rand_Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.randomPresanceChange()

    async def randomPresanceChange(self):
        rand_watching = [f'for {Shared.Vars.prefix}', 'Dead By Daylight', 'the server', 'YouTube', 'Dark Souls Remastered', f'for {Shared.Vars.prefix}help', 'commands', f'for messages starting with \'{Shared.Vars.prefix}\'', 'for urban', 'for you']
        while not Shared.Vars.Stopping and not Shared.Vars.presance_overridden:
            await asyncio.sleep(Shared.Vars.Settings['Bot_Settings']['Rand_Presence']['Presence_Update_Tick'] / 1000)
            if not Shared.Vars.Stopping and not Shared.Vars.presance_overridden:
                await self.bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)

    @commands.command()
    async def status(self, ctx, time, Type, *, Name):
        devs = "169501254899335168"
        if str(ctx.message.author.id) == devs:
            Shared.Vars.presance_overridden = True
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
            Output(f"presance updated to: {str(Type)} {Name} ({time}s)")
            try:
                await ctx.message.delete()
            except:
                Output(Type="Error", Msg="Was not able to delete status command.")
            try:
                time = int(time)
                await asyncio.sleep(time)
                await self.bot.change_presence(activity=discord.Activity(name="for " + prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
                Shared.Vars.presance_overridden = False
                await randomPresanceChange()
            except:
                Shared.Vars.presance_overridden = False
                await self.randomPresanceChange()
                msg = ctx.send(":x: Invalid arg given: time.")
                await asyncio.sleep(5)
                await msg.delete()
        else:
            msg = ctx.send(":x: You do not have the required permissions to run this command.")
            await asyncio.sleep(5)
            await msg.delete()

def setup(bot):
    bot.add_cog(Rand_Presence(bot))