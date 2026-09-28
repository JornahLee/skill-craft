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

进入项目安装流程后，无论选择哪个 skill，脚本都会将独立模板
`prompt/AGENTS.feedback.fragment.md` 中的协作规则同步到项目根目录的 `AGENTS.md`，
文件不存在时创建。每次安装流程只同步一次，即使所有 skill 都被跳过或安装失败，
仍会同步规则。交互式选择项目安装与 `--project` 行为相同。
用户级安装、仅列出 skills、无效参数或取消选择时不写入规则。

脚本通过固定标记和内容校验值维护规则段落：缺失时添加，相同时跳过，版本变化时
只更新该段，保留其他内容。若该段被手动修改、标记损坏或重复，则保留原文件，
提示检查差异并返回非零退出码；skill 安装结果仍保留。`--force` 只覆盖 skill，
不会绕过规则段落的手动修改保护。同步只发生在安装时，日常使用 skill 不检查配置。
旧版 `design-dialogue` 规则段落会在校验通过后迁移为独立标记，不重复追加。
