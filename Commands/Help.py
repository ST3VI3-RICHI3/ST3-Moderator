import discord
import os
import json
import asyncio
import Shared
from Shared import Output
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        DM = False
        embed=discord.Embed(title="Help", description=f"This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '{Shared.Vars.prefix}', this list only applies to the server you sent the help command in and the roles you have in said server.", color=0x8080ff)
        embed.add_field(name="Help", value="The generic help command, it brings this up.", inline=False)
        #embed.add_field(name="Info", value="Shows the version and changes.", inline=False)
        try:
            if ctx.message.author.guild_permissions.administrator:
                embed.add_field(name="Role", value="Used for role managment. " + ctx.prefix + "role {Add / Remove} @User @Role", inline=False)
                embed.add_field(name="Kick", value="kicks a specific user.", inline=False)
                embed.add_field(name="Ban", value="bans a specific user.", inline=False)
                embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
                embed.add_field(name="C_Announce", value="Announces supplied text to the channel the command was used in. Caution: Uses @everyone", inline=False)
                embed.add_field(name="Purge", value="Deletes a given ammount of messages.", inline=False)
                embed.add_field(name="Mute", value="Mutes a given user.", inline=False)
                embed.add_field(name="Unmute", value="Unmutes a given user.", inline=False)
        except:
            DM = True
        if str(ctx.message.author.id) == Shared.Vars.devs:
            embed.add_field(name="test", value="This tests if the bot is running & responsive.", inline=False)
            embed.add_field(name="status", value="Sets the bot's playing / watching / listening to status.", inline=False)
            embed.add_field(name="config", value="Sets provided property / setting for the bot.", inline=False)
            embed.add_field(name="Cog_Load", value="Loads a given cog", inline=False)
            embed.add_field(name="Cog_Reload", value="Reloads a given cog.", inline=False)
            embed.add_field(name="Cog_Unload", value="Unloads a given cog.", inline=False)
            embed.add_field(name="update", value="updates the bot to newer code hosted on GutHub.", inline=False)
            embed.add_field(name="restart", value="restarts the bot, this can also be used to update the bot.", inline=False)
            embed.add_field(name="shutdown", value="causes the bot's script to exit.", inline=False)

        HelpSettings = Shared.Vars.Settings['Bot_Settings']['Help']
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

def setup(bot):
    bot.add_cog(Help(bot))
