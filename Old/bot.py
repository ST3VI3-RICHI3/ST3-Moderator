#ST3-Moderator by ST3VI3 RICHI3#5015

from __future__ import print_function
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import os

devs = "169501254899335168"
Version = "DEV-0004"

print("Bot loading token from file TOKEN [0%]", end = "\r")

def Setup():
	print("Loading failed, file does not exist.   ")
	TOKEN = input("Please enter the bot token. ")
	with open("TOKEN", "w") as Writer:
		Writer.write(TOKEN)
		Writer.close()
		print("Token saved, if your bot is on GitHub, it is strongly advised to add \"TOKEN\" to your gitnore. This will reduce the pssibility of your bot being hijacked / stolen.")
		safegitnore = False	
		if os.path.isfile(".gitignore"):
			with open(".gitignore", "r") as f:
				if "TOKEN" in f.read():
					print("TOKEN is already in gitnore, continuing without prompt.")
					safegitnore = True
				f.close()
			if input("Add to gitnore? [Y/N] ") == "y" or "Y" and safegitnore == False:
				with open(".gitignore", "a") as f:
						f.write("\n" + "TOKEN")
						f.close()
			else:
				print("Response was not equal to \"y\" or \"Y\". Assuming no and continuing without adding to gitnore file.")
		else:
			print("No gitnore file found, you may have to manually add \"TOKEN\" to your gitnore should one exist.")
	return TOKEN

prefix = "//"

if os.path.isfile("TOKEN"): 
	TOKEN = open(str("TOKEN"), "r")
	print("Bot loading token from file TOKEN [50%]", end = "\r")
	TOKEN = str(TOKEN.readline())
	print("Bot loaded token from file TOKEN [100%]", end = "\n")
else:
	TOKEN = Setup()

print("Bot loading  [0%]", end = "\r")
Sudo_owner = "169501254899335168"
Owners = ["169501254899335168"]
with open("Owners.txt", "r") as f:
	for line in f:
		Owners.append(line)
	f.close()

print("Bot loading [50%]", end = "\r")
bot = commands.Bot(command_prefix=prefix)# This sets the prefix that the bot will use.
client = bot
bot.remove_command('help') #Removes the default discord help command
@bot.event
async def on_ready():
	await bot.change_presence(game=discord.Game(name= str(prefix) + "help"), status=discord.Status("online"), afk=False)
	print("Bot loaded [100%]")
	print("Bot running.")

@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.command(pass_context = True)
async def help(ctx):
	DM = False
	msg = await bot.get_message(ctx.message.channel, ctx.message.id)
	try:
		await bot.delete_message(msg)
	except:
		DM = True
	embed=discord.Embed(title="Help", description="This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '!', this list only applies to the server you sent the help command in and the roles you have in said server.", color=0x8080ff)
	embed.add_field(name="Help", value="The generic help command, it brings this up.", inline=False)
	embed.add_field(name="Info", value="Shows the version and changes.", inline=False)
	try:
		if ctx.message.author.server_permissions.administrator:
			embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
			embed.add_field(name="addrole", value="Adds a specific role to a given user.", inline=False)
			embed.add_field(name="removerole", value="Removes a specific role from a given user.", inline=False)
			embed.add_field(name="C_Announce", value="Announces supplied text to the channel the command was used in, text must be in quotes.", inline=False)
			embed.add_field(name="kick", value="kicks a specific user.", inline=False)
			embed.add_field(name="ban", value="bans a specific user.", inline=False)
	except:
		DM = True
	if str(ctx.message.author.id) in Owners:
		embed.add_field(name="test", value="This tests if the bot is running & responsive.", inline=False)
	if str(ctx.message.author.id) == devs:
		embed.add_field(name="update", value="updates the bot to newer code hosted on GutHub.", inline=False)
		embed.add_field(name="restart", value="restarts the bot, this can also be used to update the bot.", inline=False)
	await client.send_message(ctx.message.author, embed=embed)
	if not DM:
		msg = await bot.say(":ok_hand: Check your DMs!")
		await asyncio.sleep(5)
		await bot.delete_message(msg)



@bot.command(pass_context = True)
async def info(ctx):
	embed = discord.Embed(title="Version", description=" ")
	embed.add_field(name="Bot version", value=Version, inline=False)
	embed.add_field(name="Changes", value="Fixed !addrole, Fixed !removerole, Updated !ver", inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context = True)
async def Config(ctx, File: str, Property: str, Value: str):
	if str(ctx.message.author) == Sudo_owner:
		with open(File, "r+") as f:
			i = 0
			while i != len(f.readlines()):
				f.seek(i)
				if str(f.read())[len(Property)] == Property:
					await bot.say("Debug: pos = " + str(i))
				i += 1
		await bot.say("Not implemented.")
	else:
		await bot.say(":warning: Warning: <@" + ctx.message.author.id + "> has insufficient permissions to configure the bot. :warning:")

@bot.command(pass_context = True)
async def AddOwner(ctx, user: discord.Member):
	if str(ctx.message.author) == Sudo_owner:
		if str(user) != Sudo_owner and Owners:
			with open("Owners.txt", "a") as f:
				f.write(str(user) + "\n")
				f.close()
			print("Added " + str(user) + " to the owners list.")
			Owners.append(str(user))
			await bot.say(":ballot_box_with_check: Succsessfully added <@" + str(user.id) + "> to the owners list!")
		else:
			await bot.say(":x: Error: user is already an owner.")
		
	else:
		await bot.say(":warning: Warning: <@" + ctx.message.author.id + "> has insufficient permissions to add owners to the bot. :warning:")

@bot.command(pass_context = True)
async def restart(ctx):
	if str(ctx.message.author.id) == devs:
		try:
			msg = await bot.get_message(ctx.message.channel, ctx.message.id)
			await bot.delete_message(msg)
		except:
			null = None
		await bot.change_presence(game=discord.Game(name="Restarting..."), status=discord.Status("dnd"), afk=False)
		print("Restarting...")
		os.system("start bot.py")
		exit(0)
	else:
		await bot.say(":warning: Warning: <@" + ctx.message.author.id + "> has insufficient permissions to restart the bot. :warning:")
@bot.command(pass_context = True)
async def update(ctx):
	if str(ctx.message.author.id) == devs:
		try:
			msg = await bot.get_message(ctx.message.channel, ctx.message.id)
			await bot.delete_message(msg)
		except:
			null = None
		await bot.change_presence(game=discord.Game(name="Updating..."), status=discord.Status("dnd"), afk=False)
		print("Downloading update from git...")
		os.system("cd C:/Users/%username%/Documents/GitHub/ST3-Moderator/ | git pull | echo.")
		os.system("start bot.py")
		exit(0)
	else:
		await bot.say(":warning: Warning: <@" + ctx.message.author.id + "> has insufficient permissions to update the bot. :warning:")

bot.run(TOKEN)
