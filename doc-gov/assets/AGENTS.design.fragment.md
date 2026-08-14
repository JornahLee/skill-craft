## 文档治理

本项目采用 `$doc-gov` 文档治理体系。

- 治理类型：设计型

### 文档入口

- 业务地图：`{{BUSINESS_MAP_PATH}}`
- 技术地图：`{{TECHNICAL_MAP_PATH}}`
- ADR：`{{ADR_DIRECTORY}}`
- 活动实施契约：`{{ACTIVE_IMPLEMENTATION_DIRECTORY}}`
- 归档实施契约：`{{ARCHIVED_IMPLEMENTATION_DIRECTORY}}`

- 涉及业务设计、技术设计、架构决策、文档关系与权威来源，或定位代码变更的设计影响时，使用 `$doc-gov`，从上述入口渐进定位。
- 仅涉及实施计划、阶段、进度、验收或偏差时使用 `$impl-gov`；同时涉及当前设计、文档影响或设计收敛时再叠加 `$doc-gov`。
