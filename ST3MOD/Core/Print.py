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

def prt(msg:str, type="inf", start="", end="\n", log=True):
    ostr = msg
    if type.lower() == "inf":
        ostr = f"{start}[Info] {msg}"
    elif type.lower() == "err":
        ostr = f"{start}[Error] {msg}"
    else:
        ostr = f"{start}[{type}] {msg}"
    print(ostr, end=end)