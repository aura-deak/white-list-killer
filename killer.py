import subprocess
import sys
import json
from get_process import get_all_processes

def get_kill_process():
    white_list = []
    with open("whitelist-system.json", "r") as f:
        white_list.extend(json.load(f))
    with open("whitelist-user.json", "r") as f:
        white_list.extend(json.load(f))
    kill_process = get_all_processes()
    kill_process = list(set(kill_process) - set(white_list))
    return kill_process

loop = sys.argv[1]=="loop"
kill_process_list = get_kill_process()

while True:
    for i in kill_process_list:
        subprocess.run(["pkill", "-f", i])
    if not loop:
        break