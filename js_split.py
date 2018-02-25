import sys
import json
import os
import time
from operator import itemgetter

_low = lambda x: x.replace("İ", "i").replace("I", "ı").lower()

if len(sys.argv) < 3:
    print("Usage: python3", sys.argv[0], "<json_file> <write_dir> [--sorted]")
    sys.exit(1)

json_file = sys.argv[1]
write_dir = sys.argv[2]
do_sort = "--sorted" in sys.argv

print("[+] Loading records ... ", end="")

with open(json_file, "r") as jf:
    jd = json.load(jf)

print("DONE\n[+] Analyzing regs ", end="")

reg_sv = dict()

for reg in jd:
    sname_pre = _low(reg["isim"].split(" ")[-1][0])

    if sname_pre not in reg_sv:
        reg_sv[sname_pre] = list()

    reg_sv[sname_pre].append(reg)

    print(".", end="", flush=True)
    time.sleep(0.002)

if do_sort:
    print("\n[+] Sorting ", end="")
    for pre in reg_sv:
        reg_sv[pre] = sorted(reg_sv[pre], key = lambda x: itemgetter("isim")(x).split(" ")[-1])
        print(".", end="")
        time.sleep(0.001)
    print(" DONE.")

print("DONE\n[+] Saving regs ...")

for pre in reg_sv:
    print("  =>", pre + ".json", "... ", end="")
    with open(os.path.join(write_dir, pre + ".json"), "w") as wf:
        json.dump(reg_sv[pre], wf)
    print("DONE")

print("\n[i] We're done here!\n")
