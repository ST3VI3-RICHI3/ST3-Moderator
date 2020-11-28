from __future__ import print_function

def prt(msg:str, type="info", end="\n", log=True):
    ostr = msg
    if type.lower() == "info":
        ostr = f"[i] {msg}"
    print(ostr, end=end)