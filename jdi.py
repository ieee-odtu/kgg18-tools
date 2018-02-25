import sys
import requests
import json
import time
import re

if len(sys.argv) != 4:
    print("Usage: python3", sys.argv[0] + "<json_file> <server_addr> <phpsessid>")
    sys.exit(1)

json_file = sys.argv[1]
webserver = sys.argv[2]
php_cookie = sys.argv[3]

print("[+] Reading records ... ", end="")

with open(json_file, "r") as jf:
    jd = json.load(jf)

print("DONE.")
print("  => Found", len(jd), "record(s)\n")

print("[+] Sending to server:", webserver, end=" ... ", flush=True)

for reg in jd:
    _ws = "http://" + webserver if not re.match("^https?://.*$", webserver) else webserver
    requests.post(_ws + "/kgg/do_stuff.php", data = reg, cookies = {"PHPSESSID": php_cookie})

print("DONE.")
time.sleep(0.5)
print("\n[i] We're all done here!\n")
