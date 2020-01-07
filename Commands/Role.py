import discord
import asyncio
from discord.ext import commands

class Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, func = None, User: discord.Member = None, role = None):
        if ctx.message.author.guild_permissions.administrator:
            if User != None:
                if Role != None:
                    if func == "add":
                        try:
                            await User.add_roles(role)
                            msg = await ctx.send(":thumbsup: added role!")
                            asyncio.sleep(5)
                            await msg.delete()
                            try:
                                await ctx.message.delete()
                            except:
                                pass
                        except:
                            await ctx.send("There was an error doing that.")
                    elif func == "remove":
                        try:
                            await User.remove_roles(role)
                            msg = await ctx.send(":thumbsup: removed role!")
                            asyncio.sleep(5)
                            await msg.delete()
                            try:
                                await ctx.message.delete()
                            except:
                                pass
                        except:
                            await ctx.send("There was an error doing that.")
                else:
                    await ctx.send("Missing or invalid arguement, `func` (Function). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
            else:
                await ctx.send("Missing or invalid arguement, `role` (@Role_To_Act_On). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
        else:
            await ctx.send("Missing or invalid arguement, `User` (@User_Mention). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")

def setup(bot):
    print("[Info] Role commands successfully loaded.")
    bot.add_cog(Role(bot))
