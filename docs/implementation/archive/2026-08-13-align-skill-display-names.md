# 统一 Skill 显示名称

- **预期结果**：治理 Skill 的目录名、`SKILL.md.name` 和 `interface.display_name` 完全一致。
- **范围**：`impl-gov`、`doc-gov` 的界面元数据，以及根 `AGENTS.md` 的 skill 命名约束。
- **非目标**：不调整 skill 的职责、触发条件或正文流程。
- **设计依据**：名称保持简短一致，便于用户主动识别和调用。
- **最小充分验证**：解析 YAML，核对三个名称字段，并检查 Git 差异。
- **重新讨论条件**：发现 Codex 界面对 `display_name` 有不同的强制格式要求。

## 实施结果

- `impl-gov` 与 `doc-gov` 的 `interface.display_name` 已改为与目录名和 `SKILL.md.name` 完全一致。
- 根 `AGENTS.md` 已规定三处名称必须完全一致，并强调名称应简短、方便主动调用。
- YAML 解析、三处名称一致性、默认提示引用和 `git diff --check` 均通过。
- 未运行全量测试：本次仅涉及两项 YAML 字符串与一条仓库指令，定向结构检查已覆盖风险。

结论：完成。
