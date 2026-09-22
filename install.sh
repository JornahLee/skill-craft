#!/usr/bin/env bash
# 远程安装入口；安装逻辑与交互仍由同一份快照中的 Python 脚本负责。
main() {
    set -euo pipefail

    local dependency temporary_root
    for dependency in curl python3 tar mktemp; do
        if ! command -v "$dependency" >/dev/null 2>&1; then
            echo "缺少依赖：$dependency，请安装后重试。" >&2
            return 1
        fi
    done
    if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
        echo "需要 Python 3.9 或更新版本，请安装后重试。" >&2
        return 1
    fi

    # Bash 的标准输入可能是脚本管道，交互输入必须单独连接终端。
    if { exec 3</dev/tty; } 2>/dev/null; then
        :
    elif [ "$#" -eq 0 ]; then
        echo "未找到可用终端。请在终端中运行，或传入 --all --user --force 等非交互参数。" >&2
        return 1
    else
        exec 3</dev/null
    fi

    temporary_root=$(mktemp -d "${TMPDIR:-/tmp}/skill-craft.XXXXXXXX")
    trap 'rm -rf -- "$temporary_root"' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM

    echo "正在下载最新 skills…"
    if ! curl -fsSL --connect-timeout 20 --max-time 180 \
        https://github.com/JornahLee/skill-craft/archive/refs/heads/main.tar.gz \
        -o "$temporary_root/source.tar.gz"; then
        echo "下载失败，请检查网络后重试。" >&2
        exit 1
    fi
    if ! tar -xzf "$temporary_root/source.tar.gz" -C "$temporary_root"; then
        echo "仓库快照解压失败，请重试。" >&2
        exit 1
    fi
    if [ ! -f "$temporary_root/skill-craft-main/install_skills.py" ]; then
        echo "仓库快照缺少 install_skills.py，无法继续安装。" >&2
        exit 1
    fi

    # 不切换工作目录，确保 --project 始终指向用户运行命令时的项目。
    local result=0
    python3 "$temporary_root/skill-craft-main/install_skills.py" "$@" <&3 || result=$?
    exit "$result"
}

main "$@"
