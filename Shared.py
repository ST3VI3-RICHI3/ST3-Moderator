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
from __future__ import print_function
import os
import json
from datetime import datetime
import platform

def __init__():
	Vars.Settings = SetLoad()
	Vars.DBData = Database.Load()

def Output(Msg: str, Type="Info", Premsg="", End="\n"):
	print(f"{Premsg}[{str(datetime.now())[:19]} | {Type}] {Msg}", end=End)
	try:
		with open("Logs/Latest.log", "a") as Log:
			Log.write(f"[{str(datetime.now())[:19]} | {Type}] {Msg}\n")
	except:
		if not os.path.isfile("Logs"):
			os.popen("mkdir Logs")

def BIn(Msg: str, Type="Input", Premsg=""):
	Msg = input(f"{Premsg}[{str(datetime.now())[:19]} | {Type}] {Msg}")
	try:
		with open("Logs/Latest.log", "a") as Log:
			Log.write(f"[{str(datetime.now())[:19]} | {Type}] {Msg}\n")
	except:
		if not os.path.isfile("Logs"):
			os.popen("mkdir Logs")
			with open("Logs/Latest.log", "w") as Log:
				Log.wriFalseettings.json") as FSettings:
			Settings = json.load(FSettings)
			FSettings.close()
		Info = Settings['Info']
		SavedData = Settings['Saved_Data']
		SV = Info['Settings_Version']
		Bot_Settings = Settings['Bot_Settings']
		Vars.Version = Info["Bot_Version"]
		if SV == "0.0.5":
			if SavedData['Token'] != None:
				Vars.Token = SavedData['Token']
			elif os.path.isfile("TOKEN"):
				with open("TOKEN", "r") as f:
					Vars.Token = f.read()
					Output("Token overriden via file \"TOKEN\".")
			else:
				Output(Type="Error", Msg="Token is null.")
				Vars.Token = input("Please enter the bot token: ")
				SavedData['Token'] = Vars.Token
				with open("Settings.json", "w") as f:
					json.dump(Settings, f, indent = 4)
			NoCommandSettings = Bot_Settings['No_Command']
			if os.path.isfile("Prefix_Override.txt"):
				with open("Prefix_Override.txt", "r") as f:
					Vars.prefix = f.read()
					Output(f"Prefix overiden to \"{Vars.prefix}\" via file \"Prefix_Override.txt\".")
					f.close()
			elif NoCommandSettings["Prefix"] != None:
				Vars.prefix = NoCommandSettings["Prefix"] #This allows custom prefixes.
			return Settings
		else:
			Output(Type="Error", Msg="Settings are outdated, please make sure you have the newest version before running. For the newest version of the Settings file please check github or contact the developer ( \"ST3VI3 RICHI3#5015\"). Press Enter / Return to exit.")
			input()
			exit(0)
	else:
		Output(Type="Warning", Msg="Settings.json not found. Creating file...")
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
				"Bot_Version": "DEV-REWRITE-0005"
			}
		}"""
		with open("Settings.json", "w") as f:
			json.dump(Settings_Prefab, f, indent = 4)

class Database:

	Datafile = "DB.json"

	def Load(file=Datafile):
		with open(file, "r") as DBFile:
			DBData = json.load(DBFile)
			DBFile.close()
		return DBData
	
	def Refresh(file=Datafile):
		with open(file, "r") as DBFile:
			DBData = json.load(DBFile)
			DBFile.close()
		return DBData

	def dump(file=Datafile, data=None):
		if data == None:
			data = Vars.DBData
		with open(file, "w") as f:
			json.dump(data, f, indent = 4)
			f.close()

class API:
	def GatherCogs(Search_In=["Commands", "Modules"], verbose=False):
		Cogs = []
		for _dir in Search_In:
			Cog_Count = 0
			if verbose: Output(f"Searching folder \"{_dir}\"")
			for file in os.listdir(f"./{_dir}"):
				if file.endswith(".py"):
					Cog_Count += 1
					if verbose: Output(Premsg="\r", Msg=f"Gathering cogs: {str(Cog_Count)}", End="")
					Cogs.append(f"{_dir}.{str(file)[:-3]}")
			if verbose: Output(Premsg="\r", Msg=f"Gathering cogs: {str(Cog_Count)}")
		return Cogs
				


if platform.system().lower() == "windows":
	Vars.IsWindows = True

class Vars:
	# IsWindows = False
	IsLinux = False
	Settings = {}
	Token = ""
	Stopping = False
	presence_overridden = False
	devs = ["169501254899335168", "287190213451710464"]
	prefix = "//"
	Version = ""
	DBData = {}
	Debug = False