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
from __future__ import print_function

import asyncio
import json
import os
import os.path as path
from datetime import datetime
from time import sleep

import discord
from discord.ext import commands

import Shared
from Shared import Output

if path.isfile("Logs/Latest.log"):
	print("Preparing copy of \"latest.log\"")
	LogNo = 1
	while path.isfile(f"Logs/Log{LogNo}.log"):
		LogNo += 1
	print(f"Copying log to \"Log{LogNo}.log\"")
	if Shared.Vars.IsLinux:
		print(os.popen(f"cp Logs/Latest.log Logs/Log{LogNo}.log").read())
	else:
		print(os.popen(f"copy Logs\\Latest.log Logs\\Log{LogNo}.log").read())
	print("Clearing latest log...")
	os.remove("Logs/Latest.log")

if not path.isfile("DB.json"):
	DBfile = open("DB.json","w+")
	DBfile.write("{}")
	DBfile.close()

if not path.isfile("Guilds.json"):
	Gfile = open("Guilds.json","w+")
	Gfile.write("{}")
	Gfile.close()

while True:
	try:

		#Clear the screen, this is to reduce console clutter.
		if Shared.Vars.IsLinux:
			os.system("clear")
		else:
			os.system("cls")

		Output("ST3-MODERATOR by \"ST3VI3 RICHI3#5015\"")
		Output("\n\n    ST3-MODERATOR  Copyright (C) 2020  ST3VI3 RICHI3\n\n    This program comes with ABSOLUTELY NO WARRANTY.\n    This is free software, and you are welcome to redistribute it\n    under certain conditions.\n", Type="Copyright")
		Output("Checking for updates.")
		UpOut = os.popen("git pull").read()
		if "already up to date." in UpOut.lower():
			Output("No updates found.")
		else:
			Output("Update found, restarting.")
			os.system("bot.py")
			exit(0)
		Output("Bot loading  [0%]")

		#--Init--#

		Shared.__init__()

		Output(Premsg="\r", Msg="Bot loading [25%]")

		bot = commands.Bot(command_prefix=Shared.Vars.prefix)# This sets the prefix that the bot will use.
		client = bot

		bot.remove_command('help') #Removes the default discord help command

		Output(Premsg="\r", Msg="Bot loading [50%]")

		#--Cogs--#

		Output("Searching for and mounting cogs.")
		CogL = Shared.API.GatherCogs(verbose=True)
		percentinc = 25 / len(CogL)
		Percent = 50
		for Cog in CogL:
				try:
					bot.load_extension(Cog)
				except Exception as e:
					Output(Premsg="\n", Type="Error", Msg=f"Failed to mount cog \"{Cog}\", {e}")
				Percent += percentinc
				Output(Premsg="\r", Msg=f"Bot loaded [{int(Percent)}%]", End="")
		Output(Premsg="\r", Msg=f"Bot loaded [75%]", End="")

		#--------#

		@bot.event
		async def on_ready():
			Output(Premsg="\r", Msg="Bot loaded [100%]", End="\n")
			await bot.change_presence(activity=discord.Activity(name=f"for {bot.command_prefix}", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
			Output("Bot ready.")

		@bot.event
		async def on_command_error(ctx, error):

			if hasattr(ctx.command, "on_error"):
				return

			error = getattr(error, 'original', error)

			Sverity = "Undetermined"
			Class = "Unknown"
			if isinstance(error, commands.MissingRequiredArgument): Sverity = "Unimportant"; Class = "User invoked"
			if isinstance(error, commands.BadArgument): Sverity = "Unimportant"; Class = "User invoked"
			if isinstance(error, commands.CommandNotFound): Sverity = "Unimportant"; Class = "User invoked"
			if isinstance(error, commands.CommandInvokeError): Sverity = "Medium"; Class = "Code error"
			if isinstance(error, AttributeError): Severity = "Medium"; Class = "Code error / Var error"
			if isinstance(error, UnboundLocalError): Severity = "Critical"; Class = "Code error / Var error"

			Output(Type="Error", Msg=f"An error has occured: \n\n--ST3-MODERATOR ERROR HANDLER--\n  Command: {ctx.command}\n  Error: {str(error)}\n  Error type: {str(type(error))[8:-2]}\n  Error class: {Class}\n  Sverity: {Sverity}\n-------------------------------\n")

		@bot.event
		async def on_message(message):
			if message.author.id != bot.user.id:
				pass
			await bot.process_commands(message)

		@bot.command()
		async def config(ctx, module: str = None, property: str = None, value: str = None, file: str = "Settings.json"):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				BotSettings = Shared.Vars.Settings['Bot_Settings']
				if module == "*":
					Keys = ""
					for key in dict(Shared.Vars.Settings['Bot_Settings']).keys():
						skey = str(key) + "\n"
						Keys = Keys + str(skey)
					await ctx.send("```-----Module list-----\n" + Keys + "```")
				elif module == None:
					await ctx.send("<@" + str(ctx.message.author.id) + "> :regional_indicator_x: Missing value `module` (arg1).")
				elif module in BotSettings.keys():
					BSettings = Shared.Vars.Settings['Bot_Settings']
					Module = BSettings[module]
					if property == None:
						Keys = ""
						for key, value in Module.items():
							skey = str(key) + " = " + str(value) + "\n"
							Keys = Keys + str(skey)
						await ctx.send("```-----" + module.capitalize() + " variable list-----\n" + Keys + "```")
					else:
						if property in Module.keys():
							if value == None:
								await ctx.send("Property `" + property + "` is currently set to `" + str(Module[property]) + "`.")
							else:
								if type(Module[property]) != type(value):
									try:
										value = int(value)
									except ValueError:
										try:
											value = float(value)
										except:
											if "true" or "false" in value.lower():
												if "false" in value.lower():
													value = False
												else:
													value = True
											else:
												pass
								if type(Module[property]) == type(value):
									Module[property] = value
									BSettings[module] = Module
									Shared.Vars.Settings['Bot_Settings'] = BSettings
									with open("Settings.json", "w") as f:
										json.dump(Shared.Vars.Settings, f, indent=4)
									await ctx.send("Property updated to \"" + str(value) + "\".")
									Output(f"Property {property} in {module} updated to \"{str(value)}\".")
								else:
									await ctx.send(":x: Invalid type: `" + str(type(value)) + "`, should be: `" + str(type(Module[property])) + "`.")
						else:
							await ctx.send("Invalid property.")
				else:
					await ctx.send("<@" + str(ctx.message.author.id) + "> :regional_indicator_x: Invalid module.")
			else:
				await ctx.send(":warning:Warning: <@" + str(ctx.message.author.id) + "> has insuficiant permissions to run this command.")


		#--Cog related commands--#

		@bot.command()
		async def Cog_Load(ctx, cog):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				if cog == "*":
					Output("Loading all cogs.")
					for Cog in CogL:
						try:
							bot.load_extension(Cog)
						except Exception as e:
							Output(Premsg="\n", Type="Error", Msg=f"Failed to load cog \"{Cog}\", {e}")
				else:
					try:
						Output(f"loading cog \"{cog}\".")
						bot.load_extension(cog)
						Output(f"loaded cog \"{cog}\".")
						await ctx.message.delete()
						msg = await ctx.send("Loaded cog successfully!")
						await asyncio.sleep(5)
						await msg.delete()
					except:
						Output(Type="Error", Msg=f"Failed to load cog \"Commands.{cog[:-3]}\"")
						await ctx.message.delete()
						msg = await ctx.send("There was an error loading that cog, please make sure the location and file is correct (eg: \"Commands.Help\")")
						await asyncio.sleep(5)
						await msg.delete()

		@bot.command()
		async def Cog_Reload(ctx, cog):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				if cog == "*":
					Output("Reloading all cogs.")
					for Cog in Shared.API.GatherCogs():
						try:
							Output(f"reloading cog \"{Cog}\".")
							bot.reload_extension(Cog)
							Output(f"reloaded \"{Cog}\"")
						except:
							Output(Type="Error", Msg=f"Failed to reload cog \"{Cog}\"")
					await ctx.send("Reloaded all cogs!")
					Output("Reload complete!")
				else:
					try:
						Output(f"reloading cog \"{cog}\".")
						bot.reload_extension(cog)
						Output(f"reloaded cog \"{cog}\".")
						await ctx.message.delete()
						msg = await ctx.send("Reloaded cog successfully!")
						await asyncio.sleep(5)
						await msg.delete()
					except:
						await ctx.message.delete()
						msg = await ctx.send("There was an error Reloading that cog, please make sure the location and file is correct (eg: \"Commands.Help\")")
						Output(Type="Error", Msg=f"Failed to reload cog \"{cog}\".")
						await asyncio.sleep(5)
						await msg.delete()

		@bot.command()
		async def Cog_Unload(ctx, cog):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				if cog == "*":
					Output("Unloading all cogs.")
					for Cog in Shared.API.GatherCogs():
						try:
							Output(f"unloading cog \"{Cog}\".")
							bot.unload_extension(Cog)
						except:
							Output(f"Failed to unload cog \"{Cog}\"")
				else:
					try:
						Output(f"Unloading cog \"{cog}\".")
						bot.unload_extension(cog)
						Output(f"Unloaded cog \"{cog}\".")
						await ctx.message.delete()
						msg = await ctx.send("Unloaded cog successfully!")
						await asyncio.sleep(5)
						await msg.delete()
					except:
						await ctx.message.delete()
						msg = await ctx.send("There was an error unloading that cog, please make sure the location and file is correct (eg: \"Commands.Help\")")
						await asyncio.sleep(5)
						await msg.delete()

		#------------------------#

		@bot.command()
		async def restart(ctx):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				Shared.Vars.Stopping = True
				Output("Restarting")
				await bot.change_presence(activity=discord.Activity(name="bot restarting...", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
				Output("Unloading all cogs.")
				for Cog in Shared.API.GatherCogs():
					try:
						Output(f"unloading cog \"{Cog}\".")
						bot.unload_extension(Cog)
					except:
						Output(f"Failed to unload cog \"{Cog}\"")
				try:
					await ctx.message.delete()
				except:
					Output(Type="Error", Msg="Unable to delete restart command.")
				if Shared.Vars.IsLinux:
					os.system("python3 bot.py")
				else:
					os.system("bot.py")
				exit(0)
			else:
				msg = await ctx.send(":x: You do not have the required permissions to run this command.")
				await asyncio.sleep(5)
				await msg.delete()

		@bot.command()
		async def update(ctx, *, args: str="None"):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				Shared.Vars.Stopping = True
				Output("Attempting to perform update procedure.")
				await bot.change_presence(activity=discord.Activity(name="bot updating...", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
				try:
					await ctx.message.delete()
				except:
					Output(Type="Error", Msg="Unable to delete update command.")
				UpOut = os.popen("git pull").read()
				if "already up to date." in UpOut.lower():
					Output(Type="Error", Msg="Aborting update, bot is already up to date.")
					await bot.change_presence(activity=discord.Activity(name=f"for {Shared.Vars.prefix}", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
					Shared.Vars.Stopping = False
				elif "please commit your changes or stash them before you merge" in UpOut.lower():
					Output(Type="Error", Msg="Bot update faliled: bot has uncomitted changes.")
					await bot.change_presence(activity=discord.Activity(name=f"for {Shared.Vars.prefix}", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
					Shared.Vars.Stopping = False
				elif "aborting" in UpOut.lower():
					Output(Type="Error", Msg="Bot update failed: unknown error.")
					await bot.change_presence(activity=discord.Activity(name=f"for {Shared.Vars.prefix}", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
					Shared.Vars.Stopping = False
				else:
					if "--soft" in str(args).lower():
						Output("Update complete.")
						msg = await ctx.send("Downloaded update from git. Due to `--soft`, a cog reload or a bot restart may be needed to load / enable updated code. To do this, `//Cog_Reload *` will reload all cogs, `//restart` will restart the bot.")
						await bot.change_presence(activity=discord.Activity(name=f"for {Shared.Vars.prefix}", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
						Shared.Vars.Stopping = False
						await asyncio.sleep(10)
						await msg.delete()
					else:
						Output("Update complete, restarting.")
						Output("Unloading all cogs.")
						for Cog in Shared.API.GatherCogs():
							try:
								Output(f"unloading cog \"{Cog}\".")
								bot.unload_extension(Cog)
							except:
								Output(f"Failed to unload cog \"{Cog}\"")
						os.system("bot.py")
						exit(0)
			else:
				msg = await ctx.send(":x: You do not have the required permissions to run this command.")
				await asyncio.sleep(5)
				await msg.delete()

		@bot.command()
		async def shutdown(ctx):
			if str(ctx.message.author.id) in Shared.Vars.devs:
				Shared.Vars.Stopping = True
				await bot.change_presence(activity=discord.Activity(name="Stopping.", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
				Output("shutting down")
				Output("Unloading all cogs.")
				for Cog in Shared.API.GatherCogs():
						try:
							Output(f"unloading cog \"{Cog}\".")
							bot.unload_extension(Cog)
						except:
							Output(f"Failed to unload cog \"{Cog}\"")
				try:
					await ctx.message.delete()
				except:
					Output(Type="Error", Msg="Unable to delete shutdown command.")
				exit(0)
			else:
				msg = await ctx.send(":x: You do not have the required permissions to run this command.")
				await asyncio.sleep(5)
				await msg.delete()
		bot.run(Shared.Vars.Token)

	except Exception as e:
		Output(Type="Error", Msg=f"An error has occured ({str(e)}).")
		Shared.BIn("Press return to restart.")
