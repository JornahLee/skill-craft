---
name: doc-gov
description: 治理软件项目的文档导航、业务设计、技术设计、代码映射和 ADR，并处理实施对当前设计的文档影响。仅在用户显式调用或要求建立、评估、启用项目目录导航或设计文档治理，或者项目根 AGENTS.md 已声明采用且任务涉及维护项目导航、创建、拆分、更新或审查设计文档、维护文档关系与权威来源、定位代码改动的文档影响或执行文档漂移审计时使用。
---

# 治理项目文档

按本次任务读取最小充分规则，不因项目采用某种治理类型就加载整套治理知识。

## 开始任务

1. 读取用户请求和当前范围适用的 `AGENTS.md`。
2. 若其中已经声明治理类型和实际入口，直接采用，不重新推断。
3. 若治理类型未知且本次确实需要确定类型，只读取 [governance-selection.md](references/governance-selection.md)。
4. 从下表选择本次任务需要的最少 reference。不要预读其他文件；复合任务只叠加直接涉及的任务包。
5. 从声明的地图或导航入口渐进定位项目文档。只沿明确关系或代码证据扩大范围。

## 按任务读取

| 当前任务 | 读取 |
| --- | --- |
| 建立、维护项目目录导航，或判断是否需要升级导航型治理 | [navigation.md](references/navigation.md) |
| 局部创建、修改、拆分或审查业务设计和技术设计 | [design-change.md](references/design-change.md) |
| 从文档定位代码，或判断代码变更的文档影响 | [impact-tracing.md](references/impact-tracing.md) |
| 建立或重构完整设计文档体系、地图和基础文档 | [design-system.md](references/design-system.md) |
| 表达已确认但尚未生效的目标设计，或在实施结束时收敛设计 | [design-state.md](references/design-state.md) |
| 创建、更新或取代 ADR | [adr.md](references/adr.md) |
| 启用治理、切换治理类型或更新常驻 `AGENTS.md` 声明 | [resident-config.md](references/resident-config.md) |
| 检查全局文档结构或语义漂移 | [audit.md](references/audit.md) |

仅实施契约的计划、阶段、进度、验收和偏差处理使用 `$impl-gov`。只有任务同时涉及当前设计、文档影响或设计收敛时，才叠加读取上表对应规则。

## 全局约束

- 默认局部定位并渐进读取；不得为求稳妥扫描全部文档或代码。
- 同一事实只保留一个权威定义；摘要和实现投影必须可追溯到权威来源。
- 发现多个权威来源、语义冲突或代码越过声明边界时，列出证据和待决定问题，不静默选择版本或扩大范围。
- 未经用户要求，不修改常驻指令、切换治理类型或执行全局审计。
- 只把本次任务直接需要的 reference 读入上下文；项目治理类型不是完整加载某组 reference 的理由。
