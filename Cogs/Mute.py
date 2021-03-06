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
from typing import Set
import discord
import asyncio
import ST3MOD
import os
from ST3MOD.Core import JsonFiles
from ST3MOD.Vars import VDict
from discord.ext import commands
from ST3MOD.Core import Settings

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(sef):
        if not os.path.isfile("MuteDB.json"):
            with open("MuteDB.json", "w") as dbf:
                dbf.write("{\n    \"UserDB\": {}\n}")
                dbf.close()
            Settings.Load("MuteDB.json")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if str(member.id) in str(VDict["UserDB"]):
            if str(member.guild.id) in str(VDict["UserDB"][str(member.id)]):
                if "Muted" in str(VDict["UserDB"][str(member.id)][str(member.guild.id)]):
                    if VDict["UserDB"][str(member.id)][str(member.guild.id)][0]["Muted"]:
                        Guilds = JsonFiles.Read("MuteDB.json")
                        if str(member.guild.id) in Guilds:
                            if Guilds[str(member.guild.id)]["Mute_Ban_On_Leave"]:
                                embed=discord.Embed(title="Ban", description=f"Ban from: {member.guild.name}", color=0xff0000)
                                embed.add_field(name="Reason", value=f"You have been banned from {member.guild.name} for LTAP (Leaving to avoid punishment).", inline=False)
                                try:
                                    await member.send(embed=embed)
                                except:
                                    pass
                                Reason = "LTAP (Leaving To Avoid Punishment)."
                                await member.ban(reason=Reason, delete_message_days=0)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        MRole: discord.role = None
        Guilds = JsonFiles.Read("MuteDB.json")
        if str(member.guild.id) in Guilds:
            if Guilds[str(member.guild.id)]["Mute_Role"] != None:
                MRole = Guilds[str(member.guild.id)]["Mute_Role"]
                MRole = member.guild.get_role(MRole)
            else:
                for r in member.guild.roles:
                    if str(r).lower() == "muted":
                        MRole = member.guild.get_role(r.id)
                if MRole == None:
                    return
        else:
            for r in member.guild.roles:
                if str(r).lower() == "muted":
                    MRole = member.guild.get_role(r.id)
            if MRole == None:
                return
        if str(member.id) in str(VDict["UserDB"]):
            if str(member.guild.id) in str(VDict["UserDB"][str(member.id)]):
                if "Muted" in str(VDict["UserDB"][str(member.id)][str(member.guild.id)]):
                    if VDict["UserDB"][str(member.id)][str(member.guild.id)][0]["Muted"]:
                        for r in member.roles:
                            if "@everyone" not in str(r) and "Booster" not in str(r):
                                await member.remove_roles(r)
                        await member.add_roles(MRole)

    @commands.command()
    async def confmute(self, ctx, option = None, value = None):
        if ctx.message.author.guild_permissions.administrator:
            if option == None or value == None:
                if option == None:
                    msg = await ctx.send("Missing required argument `option`.")
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await msg.delete()
                elif value == None:
                    msg = await ctx.send("Missing required argument `value`.")
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await msg.delete()
            else:
                Guilds = VDict.Load("MuteDB.json")
                if str(ctx.message.guild.id) not in Guilds:
                    Guilds[str(ctx.message.guild.id)] = {}
                    Guilds[str(ctx.message.guild.id)]["Mute_Role"] = None
                    Guilds[str(ctx.message.guild.id)]["Mute_Ban_On_Leave"] = False
                if option.lower() == "ltap":
                    if value.lower() == "true":
                        Guilds[str(ctx.message.guild.id)]["Mute_Ban_On_Leave"] = True
                    if value.lower() == "false":
                        Guilds[str(ctx.message.guild.id)]["Mute_Ban_On_Leave"] = False
                JsonFiles.dump("MuteDB.json", Guilds)
                msg = await ctx.send(f"Updated `{option}` to `{value}`.")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await msg.delete()

    @commands.command()
    async def mute(self, ctx, user: discord.Member = None, time = 0):
        MRole: discord.role = None
        Guilds = JsonFiles.Read("MuteDB.json")
        if str(ctx.message.guild.id) in Guilds:
            if Guilds[str(ctx.message.guild.id)]["Mute_Role"] != None:
                MRole = Guilds[str(ctx.message.guild.id)]["Mute_Role"]
                MRole = ctx.message.guild.get_role(MRole)
            else:
                for r in ctx.message.guild.roles:
                    if str(r).lower() == "muted":
                        MRole = ctx.message.guild.get_role(r.id)
                if MRole == None:
                    msg = await ctx.send(f":x: I cannot find a role named `muted` for this guild. If your role is under a different name, turn on anyone can @ mention this role, then run `{VDict['prefix']}setmute @mtue_role`. Anyone can @ mention this role can then be turned off if need be.")
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await msg.delete()
                    return
        else:
            for r in ctx.message.guild.roles:
                if str(r).lower() == "muted":
                    MRole = ctx.message.guild.get_role(r.id)
            if MRole == None:
                msg = await ctx.send(f":x: I cannot find a role named `muted` for this guild. If your role is under a different name, turn on anyone can @ mention this role, then run `{VDict['prefix']}setmute @mtue_role`. Anyone can @ mention this role can then be turned off if need be.")
                await asyncio.sleep(30)
                await ctx.message.delete()
                await msg.delete()
                return
        if ctx.message.author.guild_permissions.administrator:
            async def TimeMute(usr = user, time = 0):
                if time != 0:
                    await asyncio.sleep(time)
                    asyncio.get_event_loop().create_task(Mute.unmute(self, ctx, usr, True))
            if str(user.id) in VDict["UserDB"]:
                if str(ctx.message.guild.id) in str(VDict["UserDB"][str(user.id)]):
                    if "Muted" in str(VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)]):
                        if VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)][0]["Muted"]:
                            msg = await ctx.send("User is already muted in this server.")
                            await asyncio.sleep(5)
                            await msg.delete()
                            await ctx.message.delete()
                        else:
                            VDict["UserDB"][str(user.id)] = {}
                            VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)] = []
                            MemRoles = []
                            for r in user.roles:
                                if "@everyone" not in str(r) and "Booster" not in str(r):
                                    MemRoles.append(r.id)
                            VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)].append({
                                'Muted': True,
                                'Old_Roles': MemRoles
                            })
                            JsonFiles.dump()
                            for r in user.roles:
                                if "@everyone" not in str(r) and "Booster" not in str(r):
                                    await user.remove_roles(r)
                            await user.add_roles(MRole)
                            msg = await ctx.send(f"Muted <@{str(user.id)}>")
                            await TimeMute(user, time)
                            await asyncio.sleep(5)
                            await msg.delete()
                            await ctx.message.delete()
                else:
                    VDict["UserDB"][str(user.id)] = {}
                    VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)] = []
                    MemRoles = []
                    for r in user.roles:
                        if "@everyone" not in str(r) and "Booster" not in str(r):
                            MemRoles.append(r.id)
                    VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)].append({
                        'Muted': True,
                        'Old_Roles': MemRoles
                    })
                    JsonFiles.dump()
                    for r in user.roles:
                        if "@everyone" not in str(r) and "Booster" not in str(r):
                            await user.remove_roles(r)
                    await user.add_roles(MRole)
                    msg = await ctx.send(f"Muted <@{str(user.id)}>")
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                    await TimeMute(user, time)
            else:
                VDict["UserDB"][str(user.id)] = {}
                VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)] = []
                MemRoles = []
                for r in user.roles:
                    if "@everyone" not in str(r) and "Booster" not in str(r):
                        MemRoles.append(r.id)
                VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)].append({
                    'Muted': True,
                    'Old_Roles': MemRoles
                })
                JsonFiles.dump()
                for r in user.roles:
                    if "@everyone" not in str(r) and "Booster" not in str(r):
                        await user.remove_roles(r)
                await user.add_roles(MRole)
                msg = await ctx.send(f"Muted <@{str(user.id)}>")
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()

    @commands.command()
    async def setmute(self, ctx, role: discord.Role = None):
        if ctx.message.author.guild_permissions.administrator:
            Guilds = VDict.Load("MuteDB.json")
            Guilds[str(ctx.message.guild.id)] = {}
            Guilds[str(ctx.message.guild.id)]["Mute_Role"] = role.id
            JsonFiles.dump("MuteDB.json", Guilds)
            msg = await ctx.send(f":thumbsup: Set muted role to {role.id}")
            await asyncio.sleep(10)
            await msg.delete()
            await ctx.message.delete()

    @commands.command()
    async def unmute(self, ctx, user: discord.Member = None, invoked = False):
        if ctx.message.author.guild_permissions.administrator or invoked:
            MRole: discord.role = None
            Guilds = VDict.Load("MuteDB.json")
            if str(ctx.message.guild.id) in Guilds:
                if Guilds[str(ctx.message.guild.id)]["Mute_Role"] != None:
                    MRole = Guilds[str(ctx.message.guild.id)]["Mute_Role"]
                    MRole = ctx.message.guild.get_role(MRole)
                else:
                    for r in ctx.message.guild.roles:
                        if str(r).lower() == "muted":
                            MRole = ctx.message.guild.get_role(r.id)
                    if MRole == None:
                        if not invoked:
                            msg = await ctx.send(f":x: I cannot find a role named `muted` for this guild. If your role is under a different name, turn on anyone can @ mention this role, then run `{VDict.prefix}setmute @mtue_role`. Anyone can @ mention this role can then be turned off if need be.")
                            await asyncio.sleep(30)
                            await ctx.message.delete()
                            await msg.delete()
                        return
            else:
                for r in ctx.message.guild.roles:
                    if str(r).lower() == "muted":
                        MRole = ctx.message.guild.get_role(r.id)
                if MRole == None:
                    msg = await ctx.send(f":x: I cannot find a role named `muted` for this guild. If your role is under a different name, turn on anyone can @ mention this role, then run `{VDict.prefix}setmute @mtue_role`. Anyone can @ mention this role can then be turned off if need be.")
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await msg.delete()
                    return
            if str(user.id) in str(VDict["UserDB"]):
                if str(ctx.message.guild.id) in str(VDict["UserDB"][str(user.id)]):
                    if "Muted" in str(VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)]):
                        if VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)][0]["Muted"]:
                            VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)][0]["Muted"] = False
                            JsonFiles.dump()
                            await user.remove_roles(MRole)
                            Roles: discord.Role = []
                            for r in VDict["UserDB"][str(user.id)][str(ctx.message.guild.id)][0]["Old_Roles"]:
                                Roles.append(ctx.message.guild.get_role(r))
                            await user.add_roles(*Roles)
                            if not invoked:
                                msg = await ctx.send(f"Unmuted <@{user.id}>")
                                await asyncio.sleep(5)
                                await msg.delete()
                                await ctx.message.delete()
def setup(bot):
    bot.add_cog(Mute(bot))