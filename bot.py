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

def DBUpdate(Database):
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

bot = commands.Bot(command_prefix=prefix)
client = bot

#--------#

#--Init--#

if os.path.isfile("Settings.json"):
	with open("Settings.json") as FSettings:
		Settings = json.load(FSettings)
		FSettings.close()
	Info = Settings['Info']
	SavedData = Settings['Saved_Data']
	SV = Info['Settings_Version']
	Version = Info["Bot_Version"]
	if SV == "0.0.4":
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
			"Help": {
				"Send_To_DM": true
			}
		},
		"Info": {
			"Settings_Version": "0.0.4",
			"Bot_Version": "0.0.1"
		}
	}"""
	with open("Settings.json", "w") as f:
		json.dump(Settings_Prefab, f, indent = 4)

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

rand_watching = ['for' + prefix, 'Dead By Daylight', 'the server', 'YouTube', 'Dark Souls Remastered', 'for //help', 'commands', 'for messages starting with \'//\'']

async def randomPresanceChange():
	global presance_overridden
	global stopping
	await asyncio.sleep(60)
	if not stopping and not presance_overridden:
		await bot.change_presence(activity=discord.Activity(name=rand_watching[random.randint(0, len(rand_watching)-1)], type=discord.ActivityType.watching), status=discord.Status.online, afk=False)
		await randomPresanceChange()

@bot.command()
async def help(ctx):
	DM = False
	embed=discord.Embed(title="Help", description="This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '!', this list only applies to the server you sent the help command in and the roles you have in said server.", color=0x8080ff)
	embed.add_field(name="Help", value="The generic help command, it brings this up.", inline=False)
	embed.add_field(name="Info", value="Shows the version and changes.", inline=False)
	try:
		if ctx.message.author.guild_permissions.administrator:
			embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
			embed.add_field(name="addrole", value="Adds a specific role to a given user.", inline=False)
			embed.add_field(name="removerole", value="Removes a specific role from a given user.", inline=False)
			embed.add_field(name="C_Announce", value="Announces supplied text to the channel the command was used in, text must be in quotes.", inline=False)
			embed.add_field(name="kick", value="kicks a specific user.", inline=False)
			embed.add_field(name="ban", value="bans a specific user.", inline=False)
	except:
		DM = True
	if str(ctx.message.author.id) == devs:
		embed.add_field(name="test", value="This tests if the bot is running & responsive.", inline=False)
		embed.add_field(name="update", value="updates the bot to newer code hosted on GutHub.", inline=False)
		embed.add_field(name="restart", value="restarts the bot, this can also be used to update the bot.", inline=False)
	await ctx.author.send(embed=embed)
	if not DM:
		msg = await ctx.send(":ok_hand: Check your DMs!")
		await asyncio.sleep(5)
		try:
			await ctx.message.delete()
		except:
			DM = True
		await msg.delete()

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
			null = None
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
async def restart(ctx):
	global stopping
	if str(ctx.message.author.id) == devs:
		stopping = True
		print("Restarting")
		await bot.change_presence(activity=discord.Activity(name="bot restarting...", type=discord.ActivityType.streaming), status=discord.Status.do_not_disturb, afk=False)
		try:
			await ctx.message.delete()
		except:
			null = None
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
		print("performing update procedure...")
		try:
			await ctx.message.delete()
		except:
			null = None
		os.system("git pull")
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
		print("shutting down")
		try:
			await ctx.message.delete()
		except:
			null = None
		exit(0)
	else:
		msg = ctx.send(":x: You do not have the required permissions to run this command.")
		await asyncio.sleep(5)
		await msg.delete()

bot.run(_TOKEN)