# Changelog

## v1.2.1 — 日常流程轻量化（2026-10-22，本地修订）

- 删除普通论文精读中的强制前四分之一理解测试、逐章无提示复述、独立模拟读者及 `reader-review.json` 记录；这些仅在明确要求的读者研究中使用。
- 默认只做一次联合检查（真实原文目录与映射、关键公式和证据、产物构建），有问题才重查对应部分。`pytest` / UI / 发布校验仅在 Skill 开发时运行。
- schema 1.3 的 `reader.throughline`、`reader.connections` 由必填分析计划改为按需补充，减少与章节地图重复的写作；原文章序与章节覆盖检查保持严格，历史 schema 1.2 保持原合同。
- 同步修改中文 Skill 主指令、英文简述、README、工作流与质量验收；保留选择性的完整读者评估脚本和已有兼容资源。

## v1.2.0 — 原文章序优先（2026-10-22，本地修订）

**核心变更**：从“模型自拟最短完整主线并重排文章”，转向“还原原文论证，按章序逐节解释，再嵌入技术深度和独立评价”。

- 重写 `SKILL.md`、`references/narrative-workflow.md`、`reader-experience.md`、`quality-gates.md` 等，明确作者章节顺序优先、不可省略方法选择动机、关键数学与原图在原文所在节深入讲解；独立评价集中放在作者论证之后；减少重复免责语。
- 新分析 schema 1.3 增加 `reader.argument_route`、`reader.organization/departure_reason` 和 `sections[].source_sections`；旧 schema 1.0–1.2 不变且可构建。
- 构建器在概览后加简短的“论文论证路线”，末尾保留详细原文结构导览；内部 notes 记录章节对应与重排原因。
- deep/review 模式新增映射覆盖和默认章序校验；对明确声明的 `restructured` 例外保留完整覆盖检查。程序无法从 PDF 自动发现被遗漏的目录章节，人工目录审查仍为必需。
- 新增 `tests/test_source_order_v13.py` 的覆盖、倒序、独立评价和 legacy 检验；新增明确标注为**合成教学材料**的 `examples/original-order-v13` Markdown 端到端示例。
- 保留原始 `astro_xray` 数值和 UI 组件兼容资源；没有把 Skill 改写成独立 PDF 阅读器或训练框架。

## v1.1.2 — 来源 ZIP 基线

作者自查单轮流程、schema 1.2 的 throughline/connections 组织与后置原文结构导览；深度方法解释与证据核查。v1.2.0 以此包为基础，保留旧模式的数据和代码兼容性。
