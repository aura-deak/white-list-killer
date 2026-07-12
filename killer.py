import subprocess
import sys
import json
import time
from pathlib import Path
from get_process import get_all_processes

# 脚本所在目录，用于解析同目录下的资源文件，避免依赖调用方的 cwd
_SCRIPT_DIR = Path(__file__).resolve().parent

def get_kill_process():
    white_list = []

    with open(_SCRIPT_DIR / "whitelist-system.json", "r") as f:
        white_list.extend(json.load(f))
    with open(_SCRIPT_DIR / "whitelist-user.json", "r") as f:
        white_list.extend(json.load(f))

    with open("/proc/self/comm", "r") as f:
        white_list.append(f.read().strip())# 程序自身加入白名单，避免loop失效

    kill_process = get_all_processes()
    kill_process = list(set(kill_process) - set(white_list))
    return kill_process

# 不建议使用内部循环。外部调用时，循环应由外部托管
loop = (len(sys.argv)>1 and sys.argv[1]=="loop")

while True:
    kill_process_list = get_kill_process()
    for i in kill_process_list:
        subprocess.run(["pkill", "-f", i])
    if not loop:
        break
    time.sleep(1)