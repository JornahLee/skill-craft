#!/usr/bin/env python3
"""交互式安装当前仓库中的 Codex skills。"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def discover_skills(repo_root: Path) -> list[Path]:
    """查找仓库一级目录中包含 SKILL.md 的 skill。"""
    return sorted(
        (
            path
            for path in repo_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        ),
        key=lambda path: path.name,
    )


def codex_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return base / "skills"


def project_root(start: Path) -> Path:
    """返回 start 所在的 Git 仓库根目录，不在仓库中时返回 start。"""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def project_skills_dir() -> Path:
    return project_root(Path.cwd()) / ".agents" / "skills"


def choose_destination() -> Path:
    project_destination = project_skills_dir()
    print(f"当前项目安装目录：{project_destination}")
    try:
        answer = input("是否安装到当前项目？[y/N] ").strip().lower()
    except EOFError:
        answer = ""
    if answer in {"y", "yes"}:
        return project_destination
    return codex_skills_dir()


def print_skills(skills: list[Path], destination_root: Path) -> None:
    print("当前仓库中的 skills：")
    for index, skill in enumerate(skills, start=1):
        status = "（已安装）" if (destination_root / skill.name).exists() else ""
        print(f"  {index}. {skill.name}{status}")


def parse_selection(value: str, skills: list[Path]) -> list[Path]:
    """解析 all、名称、序号和序号区间组成的多选输入。"""
    value = value.strip()
    if value.lower() in {"all", "a"} or value == "全部":
        return skills.copy()
    if value in {"0", "q", "quit", "退出"}:
        return []

    name_to_index = {skill.name: index for index, skill in enumerate(skills)}
    selected_indexes: set[int] = set()
    tokens = re.split(r"[,，\s]+", value)

    for token in filter(None, tokens):
        if token in name_to_index:
            selected_indexes.add(name_to_index[token])
            continue

        if token.isdigit():
            index = int(token) - 1
            if not 0 <= index < len(skills):
                raise ValueError(f"序号超出范围：{token}")
            selected_indexes.add(index)
            continue

        match = re.fullmatch(r"(\d+)-(\d+)", token)
        if match:
            start, end = (int(number) for number in match.groups())
            if start > end:
                start, end = end, start
            if start < 1 or end > len(skills):
                raise ValueError(f"区间超出范围：{token}")
            selected_indexes.update(range(start - 1, end))
            continue

        raise ValueError(f"无法识别：{token}")

    return [skill for index, skill in enumerate(skills) if index in selected_indexes]


def choose_skills(skills: list[Path], destination_root: Path) -> list[Path]:
    print_skills(skills, destination_root)
    print("\n输入序号、名称或区间，可用逗号分隔；输入 all 选择全部，输入 0 退出。")

    while True:
        try:
            value = input("请选择要安装的 skills：")
            selected = parse_selection(value, skills)
        except EOFError:
            print("\n未读取到选择，已取消。")
            return []
        except ValueError as error:
            print(f"选择无效：{error}，请重新输入。")
            continue

        if not selected:
            print("未选择 skill，已取消。")
        return selected


def confirm_overwrite(selected: list[Path], destination_root: Path) -> set[str]:
    existing = [skill.name for skill in selected if (destination_root / skill.name).exists()]
    if not existing:
        return set()

    print("\n以下 skills 已安装：" + "、".join(existing))
    try:
        answer = input("是否覆盖这些 skills？[y/N] ").strip().lower()
    except EOFError:
        answer = ""
    return set(existing) if answer not in {"y", "yes"} else set()


def install_skill(source: Path, destination_root: Path) -> Path:
    """先暂存完整副本，再替换目标目录。"""
    destination = destination_root / source.name
    if source.resolve() == destination.resolve():
        raise ValueError("源目录已经位于 Codex skills 安装目录中")

    destination_root.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=f".{source.name}-install-", dir=destination_root)
    )
    staged = temporary_root / source.name
    backup = temporary_root / "previous"

    try:
        shutil.copytree(
            source,
            staged,
            symlinks=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        if destination.exists() or destination.is_symlink():
            destination.rename(backup)
        try:
            staged.rename(destination)
        except BaseException:
            if backup.exists() and not destination.exists():
                backup.rename(destination)
            raise
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)

    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="安装当前仓库中的 Codex skills；不指定 skill 时进入交互式多选。"
    )
    parser.add_argument("skills", nargs="*", help="要安装的 skill 名称")
    parser.add_argument("--all", action="store_true", help="选择仓库中的全部 skills")
    parser.add_argument("--list", action="store_true", help="仅列出可安装的 skills")
    parser.add_argument("--force", action="store_true", help="覆盖已安装项，不再询问")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument(
        "--project", action="store_true", help="安装到当前项目的 .agents/skills"
    )
    destination.add_argument(
        "--user", action="store_true", help="安装到用户级 Codex skills 目录"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    skills = discover_skills(REPO_ROOT)
    interactive = not args.all and not args.skills and not args.list

    if args.project:
        destination_root = project_skills_dir()
    elif args.user or not interactive:
        destination_root = codex_skills_dir()
    else:
        destination_root = choose_destination()

    if not skills:
        print("当前仓库未发现包含 SKILL.md 的一级目录。", file=sys.stderr)
        return 1

    if args.list:
        print_skills(skills, destination_root)
        return 0

    if args.all and args.skills:
        print("--all 不能与 skill 名称同时使用。", file=sys.stderr)
        return 2

    if args.all:
        selected = skills
    elif args.skills:
        try:
            selected = parse_selection(" ".join(args.skills), skills)
        except ValueError as error:
            print(f"选择无效：{error}", file=sys.stderr)
            return 2
    else:
        selected = choose_skills(skills, destination_root)

    if not selected:
        return 0

    print(f"\n安装位置：{destination_root}")
    skipped = set() if args.force else confirm_overwrite(selected, destination_root)
    failures = 0
    installed = 0
    for skill in selected:
        if skill.name in skipped:
            print(f"跳过：{skill.name}")
            continue
        try:
            destination = install_skill(skill, destination_root)
        except (OSError, ValueError) as error:
            failures += 1
            print(f"安装失败：{skill.name}（{error}）", file=sys.stderr)
        else:
            installed += 1
            print(f"已安装：{skill.name} -> {destination}")

    print(f"\n完成：安装 {installed} 个，跳过 {len(skipped)} 个，失败 {failures} 个。")
    if installed:
        print("新安装的 skills 将在 Codex 的下一轮对话中可用。")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
