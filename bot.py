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
from discord.ext import commands
import os
import ST3MOD
from ST3MOD.Core.Print import prt
from ST3MOD.Core import Settings
from ST3MOD.Vars import VDict

prt("Bot loading...")

Settings.Load()
print(VDict)

bot = commands.Bot(command_prefix=VDict["Prefix"])# This sets the prefix that the bot will use.
bot.remove_command('help') #Removes the default discord help command

if os.path.isdir("./Cogs"):
    prt(f"Loading cogs [0/{len(os.listdir('./Cogs'))}]", type="Cog")

    for cog in os.listdir("./Cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"Cogs.{cog[:-3]}")
            except Exception as e:
                print(f"Failed loading extention \"Cogs/{cog[:-3]}\". Error, {e}")
else:
    prt("Cog directory not found, skipping cogs.")
prt("Bot readying...", end="\r")


@bot.event
async def on_ready():
    prt("Bot ready.     ")

#--COG COMMANDS--#

@bot.command()
async def cl(ctx, cog):
    if ctx.author.id in VDict["Perms"]["devs"]:
        try:
            bot.load_extension(cog)
            await ctx.send("Cog loaded.")
        except Exception as e:
            await ctx.send(f"Failed loading extention \"{cog}\". Error: `{e}`")

@bot.command()
async def crl(ctx, cog):
    if ctx.author.id in VDict["Perms"]["devs"]:
        try:
            bot.unload_extension(cog)
            bot.load_extension(cog)
            await ctx.send("Cog reloaded.")
        except Exception as e:
            await ctx.send(f"Failed reloading extention \"{cog}\". Error: `{e}`")

@bot.command()
async def cul(ctx, cog):
    if ctx.author.id in VDict["Perms"]["devs"]:
        try:
            bot.unload_extension(cog)
            await ctx.send("Cog unloaded.")
        except Exception as e:
            await ctx.send(f"Failed unloading extention \"{cog}\". Error: `{e}`")

#----------------#


bot.run(ST3MOD.Vars.__TOKEN)