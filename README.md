# White List Killer

一个基于白名单的 Linux 进程清理工具。通过记录系统启动时的进程快照，区分系统进程与用户进程，最终杀死不在白名单中的所有进程。

## 安装

使用 `uv tool install` 安装（推荐）：

```bash
uv tool install --python-preference only-system .
```

安装后即可使用 `white-list-killer` 命令。

## 工作原理

1. **生成系统进程白名单** — 扫描 `/proc` 获取当前所有运行中的进程名称，保存为 `whitelist-system.json`
2. **生成用户进程白名单** — 用户启动所需的应用后，再次扫描进程，将新增进程保存为 `whitelist-user.json`
3. **清理进程** — 读取两份白名单，杀死所有不在白名单中的进程

配置文件存放于 `~/.config/white-list-killer/` 目录。

## 使用方法

### 1. 生成白名单

```bash
white-list-killer init
```

脚本会：
1. 扫描当前所有进程，保存为 `whitelist-system.json`
2. 提示你启动需要保留的用户级应用（如浏览器、编辑器等）
3. 按回车后再次扫描，将新增进程保存为 `whitelist-user.json`

### 2. 编辑白名单

根据需要手动编辑 `~/.config/white-list-killer/` 下的两个 JSON 文件，删除不需要保留的进程名。

### 3. 执行进程清理

```bash
# 单次清理
white-list-killer
# 或
white-list-killer clean

# 循环清理
white-list-killer clean --loop
```

> [!NOTE]
> 推荐配合 [aura-deak/Curfew](https://github.com/aura-deak/Curfew) 使用，
> 将 Curfew 的关机命令配置成 `white-list-killer clean --loop`（绝对路径），
> 可实现定时白名单效果。

> **警告**: `loop` 模式会持续运行并不断杀死不在白名单中的进程，请确保白名单配置正确后再使用。

## 配置文件

| 文件 | 说明 |
|------|------|
| `~/.config/white-list-killer/whitelist-system.json` | 系统启动时的进程白名单 |
| `~/.config/white-list-killer/whitelist-user.json` | 用户级进程白名单 |