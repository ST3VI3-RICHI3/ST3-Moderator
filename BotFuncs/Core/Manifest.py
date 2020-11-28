from BotFuncs.Core.Print import prt
import time

def Generate(fname: str, Data: list, extention: str = "ST3MDat", T_ENCODE: str = "cp037", Quiet=False):
    IND = 1
    with open(f"{fname}.{extention}", "wb") as MFile:
        MFile.write(bytes("ST3MDAT  ", T_ENCODE))
        MFile.write(bytes(len(Data)))
        MFile.write(bytes("  ", T_ENCODE))
        MFile.write(bytes(8))
        for SF in Data:
            MFile.write(bytes("\n", T_ENCODE))
            MFile.write(bytes(str(IND), T_ENCODE))
            MFile.write(bytes(f"[\"{SF}\"]", T_ENCODE))
            IND += 1
        MFile.write(bytes("\n", T_ENCODE))
        MFile.write(bytes("END", T_ENCODE))
        MFile.close()
    return Data

def Read(fname: str, extention: str = "ST3MDat", T_ENCODE: str = "cp037", Quiet=False):
    prt_nchr = "/"
    def upd_prt(prt_nchr):
        prt(f"Reading manifest file... {prt_nchr}", end="\r")
        if prt_nchr == "|":
            prt_nchr = "/"
        elif prt_nchr == "/":
            prt_nchr = "-"
        elif prt_nchr == "-":
            prt_nchr = "\\"
        elif prt_nchr == "\\":
            prt_nchr = "|"
        return prt_nchr
    SetFiles = []
    with open(f"{fname}.{extention}", "rb") as MFile:
        if bytes.decode(MFile.read(len(bytes("ST3MDAT  ", T_ENCODE))), encoding=T_ENCODE) == "ST3MDAT  ":
            prt_nchr = upd_prt(prt_nchr)
            fc = 0
            while str(MFile.read(1)) == "b'\\x00'":
                fc+=1
            MFile.read(2)#Skip forward 2 bytes, blanking text
            prt_nchr = upd_prt(prt_nchr)
            if str(MFile.read(8)) == "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00%'": #Check for header ending
                for iter in bytes.decode(MFile.read(), encoding=T_ENCODE).split("\n"):
                    prt_nchr = upd_prt(prt_nchr)
                    if iter != "END":
                        SetFiles.append(iter[3:-2])
            else:
                print("ERR: Byte read of manifest failed, expected header ending at: LN 1, COL 14 > LN 1 COL 22.")
                MFile.close()
    return SetFiles