import os
def get_all_processes() -> list[str]:
    """读取系统中所有进程名称"""
    process_names: set[str] = set()
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/comm", "r") as f:
                name = f.read().strip()
            if name:
                process_names.add(name)
        except (FileNotFoundError, PermissionError):
            continue
    return sorted(process_names)