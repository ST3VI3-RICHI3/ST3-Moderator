import json

def Read(setfile: str):
    if setfile != "SETTINGS_BASE.json":
        with open(setfile, "r") as sf:
            S = json.load(sf)
            sf.close()
    else:
        S = {}
        S["META"] = {}
        S["META"]["SVER"] = "2020.RW0001"
        S["META"]["BVER"] = "2020.RW0001"
        S["$UNIVERSAL"] = {}
        S["$UNIVERSAL"]["_DEBUG"] = False
        S["$UNIVERSAL"]["OS"] = 0
        S["$UNIVERSAL"]["Prefix"] = "!"
    return S