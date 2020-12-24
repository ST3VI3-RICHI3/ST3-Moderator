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
import Shared
import os
import BotFuncs
from BotFuncs import Core
from BotFuncs.Core import Manifest
from BotFuncs.Core import Settings
from BotFuncs.Core.Print import prt
import time

__DBG = True #Debug mode

prt("Checking for manifest file (\"SETTINGS_MANIFEST.ST3MDat\")... |", end="\r")

if not os.path.isfile("SETTINGS_MANIFEST.ST3MDat"):
    prt("Checking for manifest file (\"SETTINGS_MANIFEST.ST3MDat\")... Failed (Missing files)")
    prt("Generating manifest file... |", end="\r")
    SetFiles = Manifest.Generate("SETTINGS_MANIFEST", ["SETTINGS_BASE.json", "USER_SETTINGS.json"], Debug=__DBG)
    prt("Generating manifest file... Done!")
else:
    prt("Checking for manifest file (\"SETTINGS_MANIFEST.ST3MDat\")... Passed!")
    prt("Reading manifest file... /", end="\r")
    SetFiles = Manifest.Read("SETTINGS_MANIFEST", Debug=__DBG)
    prt("Reading manifest file... Done!")


__Settings = {}
for Sfile in SetFiles:
    blank_length = len(Sfile) + 5
    prt(f"Reading settings file (\"{Sfile}\") |", end="\r")
    __Settings = Settings.Read(Sfile)
    print(__Settings)
    time.sleep(10)
    i = 0
    blank_str = ""
    while i!= blank_length:
        blank_str = f"{blank_str} "
        i += 1
    prt(f"Reading settings file (\"{blank_str}", end="\r")
prt(f"Reading settings files... Done!", end="\r")


bot = commands.Bot(command_prefix="//")# This sets the prefix that the bot will use.
bot.remove_command('help') #Removes the default discord help command

prt("Checking for manifest file (\"SETTINGS_MANIFEST.ST3MDat\")... |", end="\r")

@bot.event
async def on_ready():
	Shared.Cog.SendMessage(None, "READY0", "00000000", "*")

#bot.run(None)