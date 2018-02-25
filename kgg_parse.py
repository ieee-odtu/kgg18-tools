import pandas as pd
import json
import sys
import re
import time

_clarify = lambda x: re.sub(' +',' ', x.replace(".", ". ").replace("-", " ")).strip()
_low = lambda x: x.replace("İ", "i").replace("I", "ı").lower()
_upp = lambda x: x.replace("i", "İ").replace("ı", "I").upper()
_tit = lambda x: " ".join([_upp(_x[0]) + _x[1:] for _x in _clarify(x).split(" ")])

data_file = sys.argv[1]
out_file = sys.argv[2]
no_wait = "--no-wait" in sys.argv[3:]

print("\n[+] Reading file", data_file, "... ", end="")

df = pd.read_csv(data_file)

print("DONE.")
print("  => Found", df.shape[0], "record(s)\n")
print("[+] Analyzing data ... ", end="")

df.columns = ["timestamp", "name", "school", "dept", "grade", "email"]
df["is_duplicated"] = df.duplicated(["email"])
data = df.loc[df["is_duplicated"] == False]

print("DONE.")
print("  => Found", df['is_duplicated'].sum(), "duplicate record(s)\n")
print("[+] Dumping parsed data to", out_file, end=" ")

records = list()

for row in data.iterrows():
    try:
        sch = row[1]["school"]
        dept = row[1]["dept"]
        grd = row[1].grade

        if sch != "-":
            sch = _tit(sch)
            if len(sch) <= 4:
                sch = _upp(sch)

        if dept != "-":
            dept = _tit(dept)
            if len(dept) <= 5:
                dept = _upp(dept)

        if grd != "-":
            grd = _tit(grd)

        records.append({
            "isim": _tit(row[1]["name"]),
            "kurum": sch,
            "bolum": dept,
            "sinif": grd,
            "email": _low(row[1]["email"])
        })
    except Exception as e:
        print("\n[ERR]", e)
        print("[DEBUG] name :", repr(row[1]["name"]), repr(_clarify(row[1]["name"])))
        print("[DEBUG] sch  :", repr(row[1]["school"]), repr(sch))
        print("[DEBUG] dept :", repr(row[1]["dept"]), repr(dept))
        print("[DEBUG] grade:", repr(row[1]["grade"]))
        print("[DEBUG] email:", repr(row[1]["email"]), repr(_low(row[1]["email"])))
        sys.exit(1)

    print(".", end="", flush=True)
    if not no_wait:
        time.sleep(0.002)

with open(out_file, "w") as regJ:
    json.dump(records, regJ)

print("\n\n[i] We're done here!\n")
sys.exit(0)
