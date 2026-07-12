import json
import os
from get_process import get_all_processes


def generate_whitelist(process_names: list[str], output_path) -> int:
    with open(output_path, "w") as f:
        json.dump(process_names, f, indent=2, ensure_ascii=False)


def main() -> None:

    system_process_names = get_all_processes()
    generate_whitelist(system_process_names, "whitelist-system.json")

    print("已经保存系统进程和已经启动的用户级进程")
    input("现在启动用户级进程，随后按回车键继续...")

    all_process_names = get_all_processes()
    user_process_names = list(set(all_process_names) - set(system_process_names))

    generate_whitelist(user_process_names, "whitelist-user.json")
    print("白名单已保存")
    print("请编辑文件删除不需要保留的进程名")


if __name__ == "__main__":
    main()
