#ST3-Moderator by ST3VI3 RICHI3#5015

from __future__ import print_function
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import time
import random

#--Funcs--#
"""
def DBUpdate(Database): #Not currently used with any bot features.
	with open("DB.json", "w") as f:
		json.dump(Database, f, indent = 4)
"""
#---------#

print("[Info] Bot loading  [0%]")

#--Vars--#

stopping = False	#Used when shutdown and restart are called.

presance_overridden = False

devs = "169501254899335168"

IsLinux = True

global _TOKEN

global Settings

global prefix
prefix = "//"

global Version

#--------#

#--Init--#

#Settings load

if os.path.isfile("Settings.json"):
	print("[Info] Loading bot settings")
	with open("Settings.json") as FSettings:
		Settings = json.load(FSettings)
		FSettings.close()
	Info = Settings['Info']
	SavedData = Settings['Saved_Data']
	SV = Info['Settings_Version']
	Bot_Settings = Settings['Bot_Settings']
	Version = Info["Bot_Version"]
	if SV == "0.0.5":
		if SavedData['Token'] != None:
			_TOKEN = SavedData['Token']
		elif os.path.isfile("TOKEN"):
			with open("TOKEN", "r") as f:
				_TOKEN = f.read()
				print("[Info] Token overriden via file \"TOKEN\".")
		else:
			print("Error.\nToken is null.")
			_TOKEN = input("Please enter the bot token: ")
			SavedData['Token'] = _TOKEN
			with open("Settings.json", "w") as f:
				json.dump(Settings, f, indent = 4)
		NoCommandSettings = Bot_Settings['No_Command']
		if os.path.isfile("Prefix_Override.txt"):
			with open("Prefix_Override.txt", "r") as f:
				prefix = f.read()
				print(f"[Info] Prefix overiden to \"{prefix}\" via file \"Prefix_Override.txt\".")
				f.close()
		elif NoCommandSettings["Prefix"] != None:
			prefix = NoCommandSettings["Prefix"] #This allows custom prefixes.
	else:
		print("Error.\nSettings are outdated, please make sure you have the newest version before running.")
		print("For the newest version of the Settings file please check github or contact the developer ( \"ST3VI3 RICHI3#5015\" )")
		print("Press Enter / Return to exit.")
		input()
		exit(0)
else:
	print("[Warn] Settings.json not found. Creating file...")
	Settings_Prefab = """
	{
		"Saved_Data": {
			"Token": null
		},
		"Bot_Settings": {
			"No_Command": {
				"Prefix": "//"
			},
			"Help": {
				"Send_To_DM": true
			}
		},
		"Info": {
			"Settings_Version": "0.0.5",
			"Bot_Version": "DEV-REWRITE-0005"
		}
	}"""
	with open("Settings.json", "w") as f:
		json.dump(Settings_Prefab, f, indent = 4)

bot = commands.Bot(command_prefix=prefix)
client = bot

#Database (Not currently used)
"""
if os.path.isfile("DB.json"):
	with open("DB.json", "r") as DBFile:
		Database = json.load(DBFile)
else:
	Database = {}
	with open("DB.json", "w") as f:
		json.dump(Database, f, indent = 4)

if os.path.isfile("DB.json"):
	with open("DB.json", "r") as DBFile:
		Database = json.load(DBFile)
else:
	Database = {}
	with open("DB.json", "w") as f:
		json.dump(Database, f, indent = 4)
"""
#--------#

print("\r[Info] Bot loading [50%]")

bot = commands.Bot(command_prefix=prefix)# This sets the prefix that the bot will use.
client = bot

bot.remove_command('help') #Removes the default discord help command

#--Cogs--#

print("[Info] Gathering cogs", end="")
Cog_Count = 0
for file in os.listdir("./Commands"):
	if file.endswith(".py"):
		Cog_Count += 1
		print("\r[Info] Gathering cogs: " + str(Cog_Count), end="")
		time.sleep(0.050)
print("\n[Info] Loading cogs")
print("[Info] Number of possible cogs found: " + str(Cog_Count))
percentinc = 25 / Cog_Count
Percent = 50
for file in os.listdir("./Commands"):
	if file.endswith(".py"):
		try:
			bot.load_extension(f"Commands.{file[:-3]}")
		except:
			print(f"\r[Error] Failed to load cog \"Commands.{file[:-3]}\"                         \r[Error] Failed to load cog \"Commands.{file[:-3]}\"")
		Percent += percentinc
		print(f"\r[Info] Bot loaded [{Percent}%]                         \r[Info] Bot loaded [{Percent}%]", end="")
		time.sleep(0.050)
print("\r[Info] Bot loaded [75%]                         \r[Info] Bot loaded [75%]", end = "")

#--------#

@bot.event
async def on_command_error(ctx, error):
	Sverity = "Undetermined"
	Class = "Unknown"
	if isinstance(error, commands.MissingRequiredArgument): Sverity = "Unimportant"; Class = "User invoked"
	if isinstance(error, commands.BadArgument): Sverity = "Unimportant"; Class = "User invoked"
	if isinstance(error, commands.CommandNotFound): Sverity = "Unimportant"; Class = "User invoked"
	if isinstance(error, commands.CommandInvokeError): Sverity = "Medium"; Class = "Code error"

	print("\n--ST3-MODERATOR ERROR HANDLER--")
	print(f"  Command: {ctx.command}")
	print(f"  Error: {error}")
	print(f"  Error type: {str(type(error))[8:-2]}")
	print(f"  Error class: {Class}")
	print(f"  Sverity: {Sverity}")
	print("-------------------------------\n")

@bot.event
async def on_message(message):
	if message.author.id != bot.user.id:
		if len(message.content) >= 6:
			if message.content.lower()[0:5] == "urban":
				query = "https://www.urbandictionary.com/define.php?term="
				for char in message.content[6:len(message.content)]:
					if char == " ":
						query = query + "+"
					else:
						query = query + char
				await message.channel.send(query)
	await bot.process_commands(message)

@bot.command()
async def config(ctx, module: str = None, property: str = None, value = None, file: str = "Settings.json"):
	if str(ctx.message.author.id) in devs:
		global Settings
		BotSettings = Settings['Bot_Settings']
		if module == "*":
			Keys = ""
			for key in dict(Settings['Bot_Settings']).keys():
				skey = str(key) + "\n"
				Keys = Keys + str(skey)
			await ctx.send("```-----Module list-----\n" + Keys + "```")
		elif module == None:
			await ctx.send("<@" + str(ctx.message.author.id) + "> :regional_indicator_x: Missing value `module` (arg1).")
		elif module in BotSettings.keys():
			BSettings = Settings['Bot_Settings']
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
							if "true" or "false" in value.lower():
								if "false" in value.lower():
									value = False
								else:
									value = True
							else:
								try:
									value = int(value)
								except ValueError:
									try:
										value = float(value)
									except:
										pass
						if type(Module[property]) == type(value):
							Module[property] = value
							BSettings[module] = Module
							Settings['Bot_Settings'] = BSettings
							with open("Settings.json", "w") as f:
								json.dump(Settings, f, indent=4)
							await ctx.send("Property updated to \"" + str(value) + "\".")
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
	if str(ctx.message.author.id) == devs:
		if cog == "*":
			for file in os.listdir("./Commands"):
				print("[Info] Loading all cogs.")
				if file.endswith(".py"):
					try:
						print(f"[Info] loading cog \"Commands.{file[:-3]}\".")
						bot.load_extension(f"Commands.{file[:-3]}")
					except:
						print(f"[Error] Failed to load cog \"Commands.{file[:-3]}\"")
		else:
			try:
				print(f"[Info] loading cog \"{cog}\".")
				bot.load_extension(cog)
				print(f"[Info] loaded cog \"{cog}\".")
				await ctx.message.delete()
				msg = await ctx.send("Loaded cog successfully!")
				await asyncio.sleep(5)
				await msg.delete()
			except:
				await ctx.message.delete()
				msg = await ctx.send("There was an error loading that cog, please make sure the location and file is correct (eg: \"Commands.Help\")")
				await asyncio.sleep(5)
				await msg.delete()

@bot.command()
async def Cog_Reload(ctx, cog):
	if str(ctx.message.author.id) == devs:
		if cog == "*":
			print("[Info] Reloading all cogs.")
			for file in os.listdir("./Commands"):
				if file.endswith(".py"):
					try:
						print(f"[Info] reloading cog \"Commands.{file[:-3]}\".")
						bot.reload_extension(f"Commands.{file[:-3]}")
						print(f"[Info] reload of \"Commands.{file[:-3]}\"")
					except:
						print(f"[Error] Failed to reload cog \"Commands.{file[:-3]}\"")
			await ctx.send("Reloaded all cogs!")
			print("[Info] Reload complete!")
		else:
			try:
				print(f"[Info] reloading cog \"{cog}\".")
				bot.reload_extension(cog)
				print(f"[Info] reloaded cog \"{cog}\".")
				await ctx.message.delete()
				msg = await ctx.send("Reloaded cog successfully!")
				await asyncio.sleep(5)
				await msg.delete()
			except:
				await ctx.message.delete()
				msg = await ctx.send("There was an error Reloading that cog, please make sure the location and file is correct (eg: \"Commands.Help\")")
				await asyncio.sleep(5)
				await msg.delete()

@bot.command()
async def Cog_Unload(ctx, cog):
	if str(ctx.message.author.id) == devs:
		if cog == "*":
			for file in os.listdir("./Commands"):
				print("[Info] Unloading all cogs.")
				if file.endswith(".py"):
					try:
						print(f"[Info] unloading cog \"Commands.{file[:-3]}\".")
						bot.unload_extension(f"Commands.{file[:-3]}")
					except:
						print(f"[Error] Failed to unload cog \"Commands.{file[:-3]}\"")
		else:
			try:
				print(f"[Info] Unloading cog \"{cog}\".")
				bot.unload_extension(cog)
				print(f"[Info] Unloaded cog \"{cog}\".")
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
	global stopping
	if str(ctx.message.author.id) == devs:
		stopping = True
		print("[Info] Restarting")
		await bot.change_presence(activity=discord.Activity(name="bot restarting...", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
		try:
			await ctx.message.delete()
		except:
			print("Unable to delete restart command.")
		os.system("bot.py")
		exit(0)
	else:
		msg = await ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

@bot.command()
async def update(ctx, *, args="None"):
	global stopping
	if str(ctx.message.author.id) == devs:
		stopping = True
		await bot.change_presence(activity=discord.Activity(name="bot updating...", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
		print("performing update procedure...")
		try:
			await ctx.message.delete()
		except:
			print("Unable to delete stop command.")
		os.system("git pull")
		if "--soft" in str(args).lower:
			print("Update complete.")
			msg = await ctx.send("Downloaded from git, a cog reload may be needed.")
			await bot.change_presence(activity=discord.Activity(name="for //", type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
			await asyncio.sleep(5)
			await msg.delete()
		else:
			print("Update complete, restarting.")
			os.system("bot.py")
			exit(0)
	else:
		msg = await ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

@bot.command()
async def shutdown(ctx):
	global stopping
	if str(ctx.message.author.id) == devs:
		stopping = True
		await bot.change_presence(activity=discord.Activity(name="Stopping.", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
		print("shutting down")
		try:
			await ctx.message.delete()
		except:
			print("Unable to delete shutdown command.")
		exit(0)
	else:
		msg = await ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

bot.run(_TOKEN)
