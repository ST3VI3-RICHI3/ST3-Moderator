import discord
import asyncio
import Shared
from Shared import Output
from discord.ext import commands

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, user: discord.Member = None):
        MRole: discord.role = None
        Guilds = Shared.Database.Load("Guilds.json")
        if str(ctx.message.guild.id) in Guilds:
            MRole = Guilds[str(ctx.message.guild.id)]["Mute_Role"]
            MRole = ctx.message.guild.get_role(MRole)
        else:
            for r in ctx.message.guild.roles:
                if str(r).lower() == "muted":
                    MRole = ctx.message.guild.get_role(r.id)
            if MRole == None:
                msg = await ctx.send(":x: Cannot find muted role for this guild.")
                await asyncio.sleep(5)
                await msg.delete()
                return
        if ctx.message.author.guild_permissions.administrator:
            if str(user.id) in str(Shared.Vars.DBData):
                if str(ctx.message.guild.id) in str(Shared.Vars.DBData[str(user.id)]):
                    if "Muted" in str(Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)]):
                        if Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)][0]["Muted"]:
                            msg = await ctx.send("User is already muted in this server.")
                            await asyncio.sleep(5)
                            await msg.delete()
                            await ctx.message.delete()
                        else:
                            Shared.Vars.DBData[str(user.id)] = {}
                            Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)] = []
                            Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)].append({
                                'Muted': True
                            })
                            Shared.Database.dump()
                            await user.add_roles(MRole)
                            msg = await ctx.send(f"Muted <@{str(user.id)}>")
                            await asyncio.sleep(5)
                            await msg.delete()
                            await ctx.message.delete()
                else:
                    Shared.Vars.DBData[str(user.id)] = {}
                    Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)] = []
                    Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)].append({
                        'Muted': True
                    })
                    Shared.Database.dump()
                    await user.add_roles(MRole)
                    msg = await ctx.send(f"Muted <@{str(user.id)}>")
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
            else:
                Shared.Vars.DBData[str(user.id)] = {}
                Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)] = []
                Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)].append({
                    'Muted': True
                })
                Shared.Database.dump()
                await user.add_roles(MRole)
                msg = await ctx.send(f"Muted <@{str(user.id)}>")
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()

    @commands.command()
    async def setmute(self, ctx, role: discord.Role = None):
        if ctx.message.author.guild_permissions.administrator:
            Guilds = Shared.Database.Load("Guilds.json")
            Guilds[str(ctx.message.guild.id)] = {}
            Guilds[str(ctx.message.guild.id)]["Mute_Role"] = role.id
            Shared.Database.dump("Guilds.json", Guilds)
            msg = await ctx.send(f":thumbsup: Set muted role to {role.id}")
            await asyncio.sleep(10)
            await msg.delete()
            await ctx.message.delete()

    @commands.command()
    async def unmute(self, ctx, user: discord.Member = None):
        if ctx.message.author.guild_permissions.administrator:
            MRole: discord.role = None
            Guilds = Shared.Database.Load("Guilds.json")
            if str(ctx.message.guild.id) in Guilds:
                MRole = Guilds[str(ctx.message.guild.id)]["Mute_Role"]
                MRole = ctx.message.guild.get_role(MRole)
            else:
                for r in ctx.message.guild.roles:
                    if str(r).lower() == "muted":
                        MRole = ctx.message.guild.get_role(r.id)
                if MRole == None:
                    msg = await ctx.send(":x: Cannot find muted role for this guild.")
                    await asyncio.sleep(5)
                    await msg.delete()
                    return
            if str(user.id) in str(Shared.Vars.DBData):
                if str(ctx.message.guild.id) in str(Shared.Vars.DBData[str(user.id)]):
                    if "Muted" in str(Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)]):
                        if Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)][0]["Muted"]:
                            Shared.Vars.DBData[str(user.id)][str(ctx.message.guild.id)][0]["Muted"] = False
                            Shared.Database.dump()
                            await user.remove_roles(MRole)
                            msg = await ctx.send(f"Unmuted <@{user.id}>")
                            await asyncio.sleep(5)
                            await msg.delete()
                            await ctx.message.delete()
def setup(bot):
    bot.add_cog(Mute(bot))