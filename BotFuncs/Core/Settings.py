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
import json

def Read(setfile: str):
    if setfile != "SETTINGS_BASE.json":
        with open(setfile, "r") as sf:
            S = json.load(sf)
            sf.close()
    else:
        S = {}
        S["META"] = {}
        S["META"]["SVER"] = "1"
        S["META"]["BVER"] = "1"
        S["$UNIVERSAL"] = {}
        S["$UNIVERSAL"]["_DEBUG"] = False
        S["$UNIVERSAL"]["OS"] = 0
        S["$UNIVERSAL"]["Prefix"] = "!"
    return S