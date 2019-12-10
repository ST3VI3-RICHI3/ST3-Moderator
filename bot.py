#ST3-Moderator by ST3VI3 RICHI3#5015

from __future__ import print_function
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import random

#--Funcs--#

def DBUpdate(Database): #Not currently used with any bot features.
	with open("DB.json", "w") as f:
		json.dump(Database, f, indent = 4)

#---------#

print("Bot loading  [0%]", end = "")

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

if os.path.isfile("Settings.json"):
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
		else:
			print("Error.\nToken is null.")
			_TOKEN = input("Please enter the bot token: ")
			SavedData['Token'] = _TOKEN
			with open("Settings.json", "w") as f:
				json.dump(Settings, f, indent = 4)
		NoCommandSettings = Bot_Settings['No_Command']
		if NoCommandSettings["Prefix"] != None:
			prefix = NoCommandSettings["Prefix"] #This allows custom prefixes.
	else:
		print("Error.\nSettings are outdated, please make sure you have the newest version before running.")
		print("For the newest version of the Settings file please contact the developer ( \"ST3VI3 RICHI3#5015\" )")
		print("Press Enter / Return to exit.")
		input()
		exit(0)
else:
	print("Settings.json not found. Creating file...")
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
			"Bot_Version": "DEV-REWRITE-0004"
		}
	}"""
	with open("Settings.json", "w") as f:
		json.dump(Settings_Prefab, f, indent = 4)

bot = commands.Bot(command_prefix=prefix)
client = bot

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

#--------#

print("\rBot loading [50%]", end = "")

bot = commands.Bot(command_prefix=prefix)# This sets the prefix that the bot will use.
client = bot

bot.remove_command('help') #Removes the default discord help command

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(name="for " + prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
	print("\rBot loaded [100%]", end = "\n")
	print("Bot running.")
	await randomPresanceChange()

rand_watching = ['for {}'.format(prefix), 'Dead By Daylight', 'the server', 'YouTube', 'Dark Souls Remastered', 'for {}help'.format(prefix), 'commands', 'for messages starting with \'{}\''.format(prefix), 'for urban', 'for you']

async def randomPresanceChange():
	global presance_overridden
	global stopping
	while not stopping and not presance_overridden:
		await asyncio.sleep(60)
		if not stopping and not presance_overridden:
			await bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)

@client.event
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
async def help(ctx):
	DM = False
	embed=discord.Embed(title="Help", description="This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '{}', this list only applies to the server you sent the help command in and the roles you have in said server.".format(prefix), color=0x8080ff)
	embed.add_field(name="Help", value="The generic help command, it brings this up.", inline=False)
	#embed.add_field(name="Info", value="Shows the version and changes.", inline=False)
	try:
		if ctx.message.author.guild_permissions.administrator:
			embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
			#embed.add_field(name="addrole", value="Adds a specific role to a given user.", inline=False)
			#embed.add_field(name="removerole", value="Removes a specific role from a given user.", inline=False)
			embed.add_field(name="C_Announce", value="Announces supplied text to the channel the command was used in. Caution: Uses @everyone", inline=False)
			embed.add_field(name="kick", value="kicks a specific user.", inline=False)
			embed.add_field(name="ban", value="bans a specific user.", inline=False)
	except:
		DM = True
	if str(ctx.message.author.id) == devs:
		embed.add_field(name="test", value="This tests if the bot is running & responsive.", inline=False)
		embed.add_field(name="status", value="Sets the bot's playing / watching / listening to status.", inline=False)
		embed.add_field(name="config", value="Sets provided property / setting for the bot.", inline=False)
		embed.add_field(name="update", value="updates the bot to newer code hosted on GutHub.", inline=False)
		embed.add_field(name="restart", value="restarts the bot, this can also be used to update the bot.", inline=False)
		embed.add_field(name="shutdown", value="causes the bot's script to exit.", inline=False)

	Bot_Settings = Settings['Bot_Settings']
	HelpSettings = Bot_Settings['Help']
	if HelpSettings['Send_To_DM']:
		await ctx.author.send(embed=embed)
		if not DM:
			msg = await ctx.send(":ok_hand: Check your DMs!")
			await asyncio.sleep(5)
			try:
				await ctx.message.delete()
			except:
				DM = True
			await msg.delete()
	else:
		await ctx.send(embed=embed)
		try:
			await ctx.message.delete()
		except:
			DM = True


@bot.command()
async def whois(ctx, member: discord.Member = None):
	if ctx.message.author.guild_permissions.administrator or member == None or ctx.message.author.id == member.id:
		if member == None:
			member = ctx.message.author
		embed=discord.Embed(title="Whois", description="Details of: {} ({})".format(member.name, member.id), color=0x00ff00)
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name="Username", value=str(member.name), inline=True)
		embed.add_field(name="ID", value=str(member.id), inline=True)
		if member.nick != None:
			embed.add_field(name="Nickname", value=str(member.nick), inline=True)
		embed.add_field(name="Status", value=str(member.status), inline=True)
		embed.add_field(name="Joined server at", value=str(member.joined_at), inline=True)
		embed.add_field(name="Joined discord at", value=str(member.created_at), inline=True)
		embed.add_field(name="Highest role", value=str(member.top_role), inline=True)
		await ctx.send(embed=embed)
	else:
		ctx.send(":x: {} You lack the required permissions to run this command".format(ctx.message.author.id))

	

@bot.command()
async def C_Announce(ctx, *, message = ""):
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

@bot.command()
async def kick(ctx, user: discord.Member = None, *, Reason: str = "No reason provided"):
	if ctx.message.author.guild_permissions.administrator:
		if user == None:
			msg = await ctx.send(":x: Missing arg: `User`")
			await asyncio.sleep(5)
			await msg.delete()
			await ctx.message.delete()
		else:
			msg = await ctx.send(":ballot_box_with_check:<@{}> was kicked for: {}".format(user.id, Reason))
			await user.kick(reason=Reason)
			await asyncio.sleep(5)
			await msg.delete()
			await ctx.message.delete()

@bot.command()
async def ban(ctx, user: discord.Member = None, *, Reason: str = "No reason provided"):
	if ctx.message.author.guild_permissions.administrator:
		if user == None:
			msg = await ctx.send(":x: Missing arg: `User`")
			await asyncio.sleep(5)
			await msg.delete()
			await ctx.message.delete()
		else:
			msg = await ctx.send(":ballot_box_with_check:<@{}> was banned for: {}".format(user.id, Reason))
			await user.ban(reason=Reason)
			await asyncio.sleep(5)
			await msg.delete()
			await ctx.message.delete()

@bot.command()
async def status(ctx, time, Type, *, Name):
	if str(ctx.message.author.id) == devs:
		global presance_overridden
		presance_overridden = True
		if Type == "playing":
			Type = discord.ActivityType.playing
		elif Type == "watching":
			Type = discord.ActivityType.watching
		elif Type == "listening":
			Type =discord.ActivityType.listening
		elif tpye == "streaming":
			tpye = discord.ActivityType.streaming
		elif Type == "unknown":
			Type = discord.ActivityType.unknown
		else:
			Type = discord.ActivityType.playing
		await bot.change_presence(activity=discord.Activity(name=Name, type=Type), status=discord.Status.online, afk=False)
		print("presance updated to: " + str(Type) + " " + Name + " (" + time + "s)")
		try:
			await ctx.message.delete()
		except:
			print("Was not able to delete status command.")
		try:
			time = int(time)
			await asyncio.sleep(time)
			await bot.change_presence(activity=discord.Activity(name="for " + prefix, type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
			presance_overridden = False
			await randomPresanceChange()
		except:
			presance_overridden = False
			await randomPresanceChange()
			msg = ctx.send(":x: Invalid arg given: time.")
			await asyncio.sleep(5)
			await msg.delete()
	else:
		msg = ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

@bot.command()
async def test(ctx):
	if str(ctx.message.author.id) in devs:
		msg = await ctx.send(":ok_hand: I am working!")
		await asyncio.sleep(5)
		await ctx.message.delete()
		await msg.delete()

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

@bot.command()
async def restart(ctx):
	global stopping
	if str(ctx.message.author.id) == devs:
		stopping = True
		print("Restarting")
		await bot.change_presence(activity=discord.Activity(name="bot restarting...", type=discord.ActivityType.playing), status=discord.Status.do_not_disturb, afk=False)
		try:
			await ctx.message.delete()
		except:
			print("Unable to delete restart command.")
		os.system("bot.py")
		exit(0)
	else:
		msg = ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

@bot.command()
async def update(ctx):
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
		print("Update complete, restarting.")
		os.system("bot.py")
		exit(0)
	else:
		msg = ctx.send(":x: You do not have the required permissions to run this command.")
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
		msg = ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

bot.run(_TOKEN)
