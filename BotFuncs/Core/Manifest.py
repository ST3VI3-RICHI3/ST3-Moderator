from BotFuncs.Core.Print import prt
import time

def Generate(fname: str, Data: list, extention: str = "ST3MDat", T_ENCODE: str = "cp037", Quiet=False, Debug = False):
    IND = 1
    with open(f"{fname}.{extention}", "wb") as MFile:
        MFile.write(bytes("ST3MDAT  ", T_ENCODE))
        if Debug:
            prt(f"Manifest file \"{fname}\": Write identifier successful", type="debug")
        MFile.write(bytes(len(Data)))
        if Debug:
            prt(f"Manifest file \"{fname}\": Write entries successful", type="debug")
        MFile.write(bytes("  ", T_ENCODE))
        if Debug:
            prt(f"Manifest file \"{fname}\": Write blanking bytes successful", type="debug")
        MFile.write(bytes(8))
        if Debug:
            prt(f"Manifest file \"{fname}\": Write header end successful", type="debug")
        for SF in Data:
            MFile.write(bytes("\n", T_ENCODE))
            MFile.write(bytes(str(IND), T_ENCODE))
            MFile.write(bytes(f"[\"{SF}\"]", T_ENCODE))
            IND += 1
            if Debug:
                prt(f"Manifest file \"{fname}\": Write data (Index: {IND}) {SF} successful", type="debug")
        MFile.write(bytes("\n", T_ENCODE))
        MFile.write(bytes("END", T_ENCODE))
        if Debug:
            prt(f"Manifest file \"{fname}\": Write manifest end successful", type="debug")
        MFile.close()
        if Debug:
          prt(f"Manifest file \"{fname}\": Write of manifest complete.", type="debug")  
    return Data

def Read(fname: str, extention: str = "ST3MDat", T_ENCODE: str = "cp037", Quiet=False, Debug = False):
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
            if Debug:
                prt(f"Manifest file \"{fname}\": Ident pass, start header read.", type="debug")
            prt_nchr = upd_prt(prt_nchr)
            fc = 0
            while str(MFile.read(1)) == "b'\\x00'":
                fc+=1
            MFile.read(2)#Skip forward 2 bytes, blanking text
            prt_nchr = upd_prt(prt_nchr)
            if str(MFile.read(8)) == "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00%'": #Check for header ending
                if Debug:
                    prt(f"Manifest file \"{fname}\": Header read successful.", type="debug")
                for iter in bytes.decode(MFile.read(), encoding=T_ENCODE).split("\n"):
                    prt_nchr = upd_prt(prt_nchr)
                    if Debug:
                        prt(f"Manifest file \"{fname}\": Data read \"{iter}\"", type="debug")
                    if iter != "END":
                        SetFiles.append(iter[3:-2])
            else:
                print("ERR: Byte read of manifest failed, expected header ending at: LN 1, COL 14 > LN 1 COL 22.")
                MFile.close()
    return SetFiles