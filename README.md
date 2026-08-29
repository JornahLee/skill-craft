# Skill Craft

本仓库包含一组 Codex skills。

## 安装

运行安装脚本后，可先选择安装到当前项目或用户目录，再按序号、名称或区间选择
一个或多个 skill：

```bash
python3 install_skills.py
```

示例选择：`1,3-5`、`doc-gov proj-exp` 或 `all`。

也可以直接使用命令行选项：

```bash
# 查看仓库中的 skills 及安装状态
python3 install_skills.py --list

# 安装全部 skills
python3 install_skills.py --all --user

# 将指定 skills 安装到当前项目的 .agents/skills
python3 install_skills.py doc-gov proj-exp --project

# 覆盖已安装项且不再询问
python3 install_skills.py --all --user --force
```

脚本只依赖 Python 标准库。裸运行时会询问是否安装到当前 Git 仓库根目录的
`.agents/skills`；选择否时安装到 `~/.codex/skills`，如果设置了 `CODEX_HOME`，
则安装到 `$CODEX_HOME/skills`。带参数调用默认保持用户级安装，也可以用
`--project` 或 `--user` 明确指定。已安装项默认会先询问是否覆盖。
