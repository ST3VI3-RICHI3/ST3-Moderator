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
import Shared
from datetime import datetime
from discord.ext import commands, tasks

class Rand_Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.randomPresanceChange()

    async def randomPresanceChange(self):
        rand_watching = [f'for {Shared.Vars.prefix}', 'the server', f'for {Shared.Vars.prefix}help', 'commands', f'for messages starting with \'{Shared.Vars.prefix}\'', 'for you', 'you', 'for commands', f"{len(self.bot.guilds)} servers"]
        Christmas_rand_watching = [f'for {Shared.Vars.prefix}', 'the snow fall ❄️', f'for {Shared.Vars.prefix}help', 'christmas dinners ❄️', f'for messages starting with \'{Shared.Vars.prefix}\'', 'for you', 'you', 'for commands', f"{len(self.bot.guilds)} servers", "the turkey cook", "presents being opened ❄️", "snow ❄️"]
        while not Shared.Vars.Stopping and not Shared.Vars.presence_overridden:
            await asyncio.sleep(Shared.Vars.Settings['Bot_Settings']['Rand_Presence']['Presence_Update_Tick'] / 1000)
            if datetime.month == 12:
                if datetime.day == 25:
                    await self.bot.change_presence(activity=discord.Activity(name=Christmas_rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
            elif not Shared.Vars.Stopping and not Shared.Vars.presence_overridden:
                await self.bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)

    @commands.command()
    async def status(self, ctx, time, Type, *, Name):
        if str(ctx.message.author.id) == Shared.Vars.devs:
            Shared.Vars.presence_overridden == True
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
            Output(f"presance updated to: {str(Type)} {Name} ({time}s)")
            try:
                await ctx.message.delete()
            except:
                Output(Type="Error", Msg="Was not able to delete status command.")
            try:
                time = int(time)
                await asyncio.sleep(time)
                await self.bot.change_presence(activity=discord.Activity(name="for " + Shared.Vars.prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
                Shared.Vars.presence_overridden = False
                await randomPresanceChange()
            except:
                Shared.Vars.presence_overridden = False
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