import json
import subprocess
import time
from pathlib import Path

from whitelist_killer.get_process import get_all_processes

CONFIG_DIR = Path.home() / ".config" / "white-list-killer"
SYSTEM_WHITELIST = CONFIG_DIR / "whitelist-system.json"
USER_WHITELIST = CONFIG_DIR / "whitelist-user.json"


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_kill_process():
    white_list = []

    with open(SYSTEM_WHITELIST, "r") as f:
        white_list.extend(json.load(f))
    with open(USER_WHITELIST, "r") as f:
        white_list.extend(json.load(f))

    with open("/proc/self/comm", "r") as f:
        white_list.append(f.read().strip())

    kill_process = get_all_processes()
    kill_process = list(set(kill_process) - set(white_list))
    return kill_process


def generate_whitelist(process_names: list[str], output_path: Path) -> int:
    with open(output_path, "w") as f:
        json.dump(process_names, f, indent=2, ensure_ascii=False)


def cmd_init():
    ensure_config_dir()
    system_process_names = get_all_processes()
    generate_whitelist(system_process_names, SYSTEM_WHITELIST)

    print("已经保存系统进程和已经启动的用户级进程")
    input("现在启动用户级进程，随后按回车键继续...")

    all_process_names = get_all_processes()
    user_process_names = list(set(all_process_names) - set(system_process_names))

    generate_whitelist(user_process_names, USER_WHITELIST)
    print("白名单已保存")
    print(f"配置文件位于: {CONFIG_DIR}")
    print("请编辑文件删除不需要保留的进程名")


def cmd_clean(loop: bool = False):
    while True:
        kill_process_list = get_kill_process()
        for i in kill_process_list:
            subprocess.run(["pkill", "-f", i])
        if not loop:
            break
        time.sleep(1)


def main(loop: bool = False):
    cmd_clean(loop=loop)