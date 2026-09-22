# Skill Craft

本仓库包含一组可供 Codex 和 DSH 使用的 skills。

## 安装

无需克隆仓库，在终端中执行：

```bash
curl -fsSL https://raw.githubusercontent.com/JornahLee/skill-craft/main/install.sh | bash
```

支持 macOS、Linux 和 WSL，需要 Bash、curl、tar 和 Python 3.9+。
每次运行会下载 main 分支的最新快照，在临时目录中运行安装程序，结束后清理。
更新 skills 也使用同一条命令，已有项会询问是否覆盖。

运行安装脚本后，可先选择 Codex 或 DSH，再选择安装到当前项目或用户目录，最后
按序号、名称或区间选择一个或多个 skill。项目目录以执行命令时所在的位置为准。
示例选择：`1,3-5`、`doc-gov proj-exp` 或 `all`。

远程入口也支持透传参数：

```bash
# 安装全部 skills 到用户目录，覆盖已有项
curl -fsSL https://raw.githubusercontent.com/JornahLee/skill-craft/main/install.sh | bash -s -- --all --user --force

# 安装指定 skills 到当前项目
curl -fsSL https://raw.githubusercontent.com/JornahLee/skill-craft/main/install.sh | bash -s -- doc-gov proj-exp --project
```

无参数安装需要可交互的终端。自动化环境请明确指定 skills 或 `--all`、安装位置，
并在需要覆盖时传入 `--force`。

如果已经克隆仓库，也可以直接运行本地安装脚本：

```bash
python3 install_skills.py
```

也可以直接使用命令行选项：

```bash
# 查看仓库中的 skills 及安装状态
python3 install_skills.py --list

# 安装全部 skills
python3 install_skills.py --all --user

# 将全部 skills 安装到 DSH 用户目录
python3 install_skills.py --all --user --platform dsh

# 将指定 skills 安装到当前项目的 .agents/skills
python3 install_skills.py doc-gov proj-exp --project

# 覆盖已安装项且不再询问
python3 install_skills.py --all --user --force
```

脚本只依赖 Python 标准库。直接运行时会先询问目标平台，再询问是否安装到当前 Git
仓库根目录的 `.agents/skills`。选择用户级安装时，Codex 使用
`~/.codex/skills`（如果设置了 `CODEX_HOME`，则使用 `$CODEX_HOME/skills`），
DSH 使用 `~/.dsh/skills`。带参数调用默认选择 Codex 和用户级安装，也可以用
`--platform`、`--project` 或 `--user` 明确指定。已安装项默认会先询问是否覆盖。
