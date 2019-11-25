#M0DB0T by ST3VI3 RICHI3#5015
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import json
import os

bot = commands.Bot(command_prefix='!')#sets the prefix for the bot.
client = bot
bot.remove_command('help')
Version = "DEV-0.1.15"
authusrs = "ST3VI3 RICHI3#5015" or "Bobby696969#8204" or "Soldier_engie-demo#3115"
Testers = "ST3VI3 RICHI3#5015" or "Bobby696969#8204" or "AnimeDevotee#3847" or "isidore#0075" or "Sparrow#6309" or "Soldier_engie-demo#3115"
devs = "ST3VI3 RICHI3#5015"
Owner = "ST3VI3 RICHI3#5015"
@bot.event
async def on_ready():
	print("Loading...")
	print("Done!")
	await bot.change_presence(game=discord.Game(name="!help"), status=discord.Status("online"), afk=False)
	print("M0DB0T by ST3VI3 RICHI3#5015")
	print("M0DB0T running on user name: " + bot.user.name + " and on the ID: " + bot.user.id)
	
@bot.command(pass_context=True)
async def help(ctx):
	msg = await bot.get_message(ctx.message.channel, ctx.message.id)
	await bot.delete_message(msg)
	embed=discord.Embed(title="Help", description="This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '!', this list only applies to the server you sent the help command in and the roles you have in said server.", color=0x8080ff)
	embed.add_field(name="help", value="The generic help command, it brings this up.", inline=False)
	embed.add_field(name="ver", value="Shows the version and changes.", inline=False)
	if ctx.message.author.server_permissions.administrator:
		embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
		embed.add_field(name="addrole", value="Adds a specific role to a given user.", inline=False)
		embed.add_field(name="removerole", value="Removes a specific role from a given user.", inline=False)
	if str(ctx.message.author) == Testers:
		embed.add_field(name="test", value="This tests if the bot is running & responsive.", inline=False)
	if ctx.message.author.server_permissions.administrator:
		embed.add_field(name="C_Announce", value="Announces supplied text to the channel the command was used in, text must be in quotes.", inline=False)
		embed.add_field(name="kick", value="kicks a specific user.", inline=False)
		embed.add_field(name="ban", value="bans a specific user.", inline=False)
	if str(ctx.message.author) == devs:
		embed.add_field(name="update", value="updates the bot to newer code.", inline=False)
		embed.add_field(name="restart", value="restarts the bot, this can also be used to update the bot.", inline=False)
	await client.send_message(ctx.message.author, embed=embed)

@bot.command(pass_context=True)#test command
async def test(ctx):
	author = ctx.message.author
	if str(author)==Testers:
		await bot.say("This is a test!")
		await bot.say("bot running version " + Version)
		print("Test command sent.")

@bot.command(pass_context=True)#test command v2
async def bucket(ctx):
	await bot.say("This is a bucket.")

@bot.command(pass_context=True)
async def whois(ctx, user: discord.Member):
	author = ctx.message.author
	if ctx.message.author.server_permissions.administrator:
		embed = discord.Embed(title="{}'s info".format(user.name), description=" ", color=0x00ff00)
		embed.add_field(name="Name", value=user.name, inline=True)
		embed.add_field(name="ID", value=user.id, inline=True)
		embed.add_field(name="Status", value=user.status, inline=True)
		embed.add_field(name="Highest role", value=user.top_role)
		embed.add_field(name="Joined", value=user.joined_at)
		embed.set_thumbnail(url=user.avatar_url)
		await bot.say(embed=embed)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))

@bot.command(pass_context = True)
async def ver(ctx):
	embed = discord.Embed(title="Version", description=" ")
	embed.add_field(name="Bot version", value=Version, inline=False)
	embed.add_field(name="Changes", value="Fixed !addrole, Fixed !removerole, Updated !ver", inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def C_Announce(ctx, message = ""):
	author = ctx.message.author
	if ctx.message.author.server_permissions.administrator:
		if message == "":
			await bot.say(":x:Error: Empty message.")
		else:
			msg = await bot.get_message(ctx.message.channel, ctx.message.id)
			await bot.delete_message(msg)
			await bot.say("@everyone Channel announcement: {}".format(message))
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))
		
@bot.command(pass_context=True)
async def iwantmod(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.server.roles, name="Requesting mod")
    await bot.add_roles(member, role)
    msg = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(msg)

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member, message = "No reason specified"):
	if ctx.message.author.server_permissions.kick_members:
		await bot.say("{} just got the boot for {}".format(user.name, message))
		bot.kick(user)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))

@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
	if ctx.message.author.server_permissions.ban:
		await bot.say("{} just got the ban hammer!".format(user.name))
		bot.ban(user)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))

@bot.command(pass_context=True)
async def modcancel(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.server.roles, name="Requesting mod")
    await bot.remove_roles(member, role)
    msg = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(msg)

@bot.command(pass_context=True)
async def addrole(ctx, member: discord.Member, message):
	if ctx.message.author.server_permissions.administrator:
		role = discord.utils.get(member.server.roles, name=message)
		await bot.add_roles(member, role)
		msg = await bot.get_message(ctx.message.channel, ctx.message.id)
		await bot.delete_message(msg)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))
		print("{} has used a restricted command without sufficient permissions".format(ctx.message.author))

@bot.command(pass_context=True)
async def removerole(ctx, member: discord.Member, message):
	if ctx.message.author.server_permissions.administrator:
		role = discord.utils.get(member.server.roles, name=message)
		await bot.remove_roles(member, role)
		msg = await bot.get_message(ctx.message.channel, ctx.message.id)
		await bot.delete_message(msg)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))
		print("{} has used a restricted command without sufficient permissions".format(ctx.message.author))

@bot.command(pass_context=True)
async def update(ctx):
	author = ctx.message.author
	if str(author) == devs:
		msg = await bot.get_message(ctx.message.channel, ctx.message.id)
		await bot.delete_message(msg)
		await bot.change_presence(game=discord.Game(name="Updating..."), status=discord.Status("dnd"), afk=False)
		exit(0)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))
		print("{} has used a restricted command without sufficient permissions".format(ctx.message.author))

@bot.command(pass_context=True)
async def restart(ctx):
	author = ctx.message.author
	if str(author) == devs:
		msg = await bot.get_message(ctx.message.channel, ctx.message.id)
		await bot.delete_message(msg)
		await bot.change_presence(game=discord.Game(name="Restarting..."), status=discord.Status("dnd"), afk=False)
		exit(0)
	else:
		await bot.say(":warning:WARNING:warning: @{} has invalid permissions.".format(ctx.message.author))
		print("{} has used a restricted command without sufficient permissions".format(ctx.message.author))

bot.run("{Redacted}")
