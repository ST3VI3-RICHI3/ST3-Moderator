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
import random
from discord.ext import commands, tasks
from BotBase.Vars import VDict
from BotBase.Core.Print import prt as print

class Rand_Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        rand_watching = [f'for {VDict["Prefix"]}', 'the server', f'for {VDict["Prefix"]}help', 'commands', f'for messages starting with \'{VDict["Prefix"]}\'', 'for you', 'you', 'for commands', f"{len(self.bot.guilds)} servers"]
        await self.bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
        await self.randomPresanceChange()

    async def randomPresanceChange(self):
        rand_watching = [f'for {VDict["Prefix"]}', 'the server', f'for {VDict["Prefix"]}help', 'commands', f'for messages starting with \'{VDict["Prefix"]}\'', 'for you', 'you', 'for commands', f"{len(self.bot.guilds)} servers"]
        while not VDict['Rand_Presence']['presence_overridden']:
            await asyncio.sleep(VDict['Rand_Presence']['Presence_Update_Tick'] / 1000)
            if not VDict['Rand_Presence']['presence_overridden']:
                await self.bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)

    @commands.command()
    async def status(self, ctx, time, Type, *, Name):
        if str(ctx.message.author.id) == VDict['Perms']['Dev']:
            VDict['Rand_Presence']['presence_overridden'] == True
            if Type == "playing":
                Type = discord.ActivityType.playing
            elif Type == "watching":
                Type = discord.ActivityType.watching
            elif Type == "listening":
                Type = discord.ActivityType.listening
            elif Type == "streaming":
                Type = discord.ActivityType.streaming
            elif Type == "unknown":
                Type = discord.ActivityType.unknown
            else:
                Type = discord.ActivityType.playing
            await self.bot.change_presence(activity=discord.Activity(name=Name, type=Type), status=discord.Status.online, afk=False)
            print(f"presance updated to: {str(Type)} {Name} ({time}s)")
            try:
                await ctx.message.delete()
            except:
                print(Type="Error", Msg="Was not able to delete status command.")
            try:
                time = int(time)
                await asyncio.sleep(time)
                await self.bot.change_presence(activity=discord.Activity(name="for " + VDict["Prefix"], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
                VDict['Rand_Presence']['presence_overridden'] = False
                await self.randomPresanceChange()
            except:
                VDict['Rand_Presence']['presence_overridden'] = False
                await self.randomPresanceChange()
                msg = ctx.send(":x: Invalid arg given: time.")
                await asyncio.sleep(5)
                await msg.delete()
        else:
            msg = ctx.send(":x: You do not have the required permissions to run this command.")
            await asyncio.sleep(5)
            await msg.delete()

def setup(bot):
    if "Rand_Presence" not in VDict.keys():
        VDict["Rand_Presence"] = {}
        VDict['Rand_Presence']['Presence_Update_Tick'] = 60000
        VDict['Rand_Presence']['presence_overridden'] = False
    elif type(VDict["Rand_Presence"]) == dict:
        if "Presence_Update_Tick" not in VDict["Rand_Presence"].keys():
            VDict['Rand_Presence']['Presence_Update_Tick'] = 60000
        elif type(VDict["Rand_Presence"]["Presence_Update_Tick"]) == int:
            VDict['Rand_Presence']['Presence_Update_Tick'] = 60000
        if "Rand_List" not in VDict["Rand_Presence"].keys():
            VDict['Rand_Presence']['Rand_List'] = 60000
        elif type(VDict["Rand_Presence"]["Rand_List"]) == int:
            VDict['Rand_Presence']['Rand_List'] = 60000
        if "presence_overridden" not in VDict["Rand_Presence"]:
            VDict['Rand_Presence']['presence_overridden'] = False
        elif type(VDict["Rand_Presence"]["presence_overridden"]) == bool:
            VDict['Rand_Presence']['presence_overridden'] = False
    bot.add_cog(Rand_Presence(bot))