import discord
import asyncio
from discord.ext import commands

class Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, func = None, User: discord.Member = None, role: discord.role = None):
	if ctx.message.author.guild_permissions.administrator:
		if User != None:
			if Role != None:
				if func == "add":
					User.add_roles(role)
				elif func == "remove":
					User.remove_roles(role)
				else:
					ctx.send("Missing or invalid arguement, `func` (Function). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
			else:
				ctx.send("Missing or invalid arguement, `role` (@Role_To_Act_On). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")
		else:
			ctx.send("Missing or invalid arguement, `User` (@User_Mention). Usage: " + str(self.bot.command_prefix) + "role {Add / Remove} @User @Role_Name")

def setup(bot):
    print("[Info] Role commands successfully loaded.")
    bot.add_cog(Role(bot))
