import discord
import os
import json
import asyncio
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        if os.path.isfile("Settings.json"):
            devs = "169501254899335168"
            with open("Settings.json") as FSettings:
                Settings = json.load(FSettings)
                FSettings.close()
            Info = Settings['Info']
            SavedData = Settings['Saved_Data']
            SV = Info['Settings_Version']
            if SV == "0.0.5":
                if SavedData['Token'] != None:
                    _TOKEN = SavedData['Token']
                elif os.path.isfile("TOKEN"):
                    with open("TOKEN", "r") as f:
                        _TOKEN = f.read()
        DM = False
        embed=discord.Embed(title="Help", description="This is a list of commands for ST3-M0D3RAT0R, all commands are used with the prefix '{}', this list only applies to the server you sent the help command in and the roles you have in said server.".format(ctx.prefix), color=0x8080ff)
        embed.add_field(name="Help", value="The generic help command, it brings this up.", inline=False)
        #embed.add_field(name="Info", value="Shows the version and changes.", inline=False)
        try:
            if ctx.message.author.guild_permissions.administrator:
                embed.add_field(name="Whois", value="Gets information about a specific user.", inline=False)
                embed.add_field(name="role", value="Used for role managment. " + ctx.prefix + "role {Add / Remove} @User @Role", inline=False)
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

def setup(bot):
    bot.add_cog(Help(bot))
