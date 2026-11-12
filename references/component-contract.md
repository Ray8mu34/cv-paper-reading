# 共享状态、原文章序映射与离线资产

`analysis.json` 是唯一 authored 科学状态；`report.md`/`report.html` 为读者成果，科学证据与必要的内部记录进 `analysis-notes.md`；读者审读记录仅在专门开展读者评测时放入 `validation/`。新任务使用 schema **1.3**；旧 schema 1.0/1.1/1.2 继续按旧逻辑构建。

## schema 1.3 阅读结构

- `reader.overview`：简明研究概览；`reader.argument_route`：按原文实际章号书写的简短论证路线，构建器在概览后、正文前显示为「论文论证路线」。
- `reader.roadmap[]`：按真实 PDF 的**主要章序**填写 `section`（精确原文标识，如 `§3`）、`title`、`argument`（实际论证作用）、`focus`（重要图、式、表）、`source_id` 与 `page`。构建器将详细表放在正文和补充层后供回查；不能用该表替代逐节解读。
- `reader.organization`：新任务默认 `paper-order`。只有确实需要改变原文顺序才用 `restructured`，并填写非空 `departure_reason`，说明具体变动；该字段会保留在内部 notes，正文若改变章序应向读者简明说明。
- `sections[].source_sections`：每个 `audience=reader` 的正文节都必须有此数组，**元素必须与 roadmap 的 `section` 完全一致**。一个原文主要节可分成多个相邻公开正文节，相邻数节可合并；纯独立评价/补充局限节可填 `[]`，在原文讲完之后。`audience=appendix` 不强制映射，核心解释不能藏在附录。
- `reader.throughline` 和 `reader.connections[]`：**可选**。仅在多条论证线或复杂先修关系确实难以通过 roadmap 说明时，补充内部说明，不要求逐章独立写 `needs/adds`；`reader.focus` 按需选择精讲位置，不改变章序。

对 `paper-order`，构建前验证：主文必须覆盖 roadmap 中所有主要章节标识；映射序列不能倒退；纯独立评价不得插在尚未完成的原文论证前。`restructured` 仍必须覆盖原文地图，但允许顺序差异。程序只能比较作者填写的地图，不能保证 roadmap 没漏掉真实 PDF 的关键章节；必须人工核对原文目录和事实。

**新任务 JSON 最小结构示意**（非完整 analysis.json）：

```json
{
  "schema_version": "1.3",
  "reader": {
    "overview": "概览……",
    "argument_route": "§1 界定问题；§2 说明先前方案及挑战；§3 提出方法；§4 验证结果。",
    "organization": "paper-order",
    "departure_reason": "",
    "roadmap": [
      {"section":"§1", "title":"Introduction", "argument":"界定研究问题与既有方案不足", "focus":"Figure 1", "source_id":"paper", "page":1},
      {"section":"§2", "title":"Method", "argument":"说明方法与关键机制", "focus":"Figure 2", "source_id":"paper", "page":3}
    ],
    "focus": []
  },
  "sections": [
    {"id":"intro", "role":"background", "title":"§1 研究动机", "markdown":"……", "claim_ids":[], "source_sections":["§1"]},
    {"id":"method", "role":"method", "title":"§2 方法", "markdown":"……", "claim_ids":[], "source_sections":["§2"]}
  ]
}
```

## 文章与资产契约

公开正文 `sections[].markdown` 在详细原文索引之前；`audience=appendix` 用于进一步科学材料；`internal` 只写入 notes。`role=review` 的解释者新评价应放在完整原文之后，清楚区别作者主张与独立判断。新的 overview/argument_route 和早先的 throughline 不会自动替模型生成正文，schema 结构合格不保证章节解释到位。

`visuals` 用 `id/kind/section_id/placement/question/why/alternative/caption/basis` 等字段决定资源，interactive 还需 `interaction_gain`。include 在对应正文的 markdown 放一次 `<!-- astro-visual:ID -->`，image 必须是工作区内 PNG/JPEG/WebP，interactive 使用本地 fragment/styles/script/data。图形应放在原文用它提出机制或支持论证的位置，作者图/教学图标清真实来源和科学基础；omit 不加载。assets/路径必须受工作区限制，JSON 拒绝 NaN，复合产物含 SHA-256 和确定性资源验证。

从 Skill 根目录运行 `scripts/build_report.py --analysis WORK/analysis.json` 同时生成正文与 notes；`--md-only` 仅生成 MD 和 notes。常规只需运行 `scripts/validate_skill.py --analysis WORK/analysis.json --require-artifacts` 一次，按发现的真实问题修改后重建受影响的部分。`scripts/prepare_reader_review.py` 及 `--require-reader-review` 仅用于用户明确要求的独立读者评估。旧 single-lens/binary-lens module 为兼容资源，CV 不自动插入。
