import json

def Read(setfile: str):
    with open(setfile, "r") as sf:
        S = json.load(sf)
        sf.close()
    return s