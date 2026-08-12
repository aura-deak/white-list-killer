#!/usr/bin/env python3
"""white-list-killer 命令行接口"""

import argparse

from whitelist_killer.killer import cmd_clean, cmd_init


def run_init() -> None:
    """运行初始化配置向导"""
    cmd_init()


def run_clean(loop: bool) -> None:
    """执行进程清理"""
    cmd_clean(loop=loop)


def cli() -> None:
    """命令行接口主函数"""
    parser = argparse.ArgumentParser(
        prog='white-list-killer',
        description='基于白名单的 Linux 进程清理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''示例用法:
  white-list-killer              执行进程清理（单次）
  white-list-killer clean        执行进程清理（单次）
  white-list-killer clean --loop 循环清理进程
  white-list-killer init         初始化白名单配置
  white-list-killer -h           显示帮助信息'''
    )

    subparsers = parser.add_subparsers(dest='command', help='可用子命令')

    parser_init = subparsers.add_parser('init', help='初始化白名单配置')
    parser_init.set_defaults(func=lambda args: run_init())

    parser_clean = subparsers.add_parser('clean', help='执行进程清理')
    parser_clean.add_argument(
        '--loop', action='store_true', help='循环清理模式'
    )
    parser_clean.set_defaults(func=run_clean)

    args = parser.parse_args()

    if args.command is None or args.command == 'clean':
        run_clean(getattr(args, 'loop', False))
    elif args.command == 'init':
        run_init()


if __name__ == "__main__":
    cli()