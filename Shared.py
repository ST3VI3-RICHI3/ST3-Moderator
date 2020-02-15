import os
import json
from datetime import datetime

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
				Log.write(f"[{str(datetime.now())[:19]} | {Type}] {Msg}\n")
	return Msg

def SetLoad():
	if os.path.isfile("Settings.json"):
		Output("Loading bot settings")
		with open("Settings.json") as FSettings:
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

	DatFile = "DB.json"

	def Load(file=DatFile):
		if file.endswith(".json"):
			with open(file, "r") as DBFile:
				DBData = json.load(DBFile)
				DBFile.close()
			return DBData
		else:
			Output(Type="Error", Msg="Cannot load database file, incorrect format.")
	
	def Refresh(file=DatFile):
		if file.endswith(".json"):
			with open(file, "r") as DBFile:
				DBData = json.load(DBFile)
				DBFile.close()
			return DBData
		else:
			Output(Type="Error", Msg="Cannot refresh database file, incorrect format.")

	def dump(file=DatFile, data=None):
		if data == None:
			data = Vars.DBData
		if file.endswith(".json"):
			with open(file, "w") as f:
				json.dump(data, f, indent = 4)
				f.close()

class Vars:
	IsLinux = False
	Settings = {}
	Token = ""
	Stopping = False
	presance_overridden = False
	devs = "169501254899335168"
	prefix = "//"
	Version = ""
	DBData = {}