# 以原文为骨架的轻量精读架构（v1.2.1）

```text
实际论文原文（正文、关键图/式/表及必要附录）
    ↓
reader.roadmap（主要原文章节的编号、论证作用、关键证据）
reader.argument_route（开篇一个自然段的作者论证路线）
sections[].source_sections（正文与原文章节的对应）
    ↓
report.md / report.html（按原章序逐节解释，必要处补数学/原图）
    ↓
一次交付检查（主要章序/关键科学事实/产物一致性）
```

默认 `schema_version=1.3`、`reader.organization="paper-order"`；`source_sections` 的覆盖和相对顺序仍由程序检查，解释者新增评价放在原文论证之后。原文顺序确实需要改变时使用 `restructured` 与明确的 `departure_reason`，并保留原文覆盖。

**精简点**：`reader.throughline` 和 `reader.connections` 仅在有复杂依赖时填写；不会因为没有这些内部草稿而拒绝 schema 1.3 深读报告。既有 schema 1.2 仍保留历史验收合同。详细原文索引和证据账本按需随 `analysis-notes.md` 自动生成，不额外手工编写重复记录。

**读者评测是可选扩展**：`validation/reader-review.json` 与 `prepare_reader_review.py`、`--require-reader-review` 保留供明确要求的教学效果评估使用，日常报告构建不调用。`pytest`、界面与发布检查只在 Skill 开发时运行。程序不能识别 roadmap 漏记了真正的原文章节，也无法替代对关键科学事实的核对。

原有离线 HTML/MathML、静态图与选择性交互、微透镜继承模块及对 schema 1.0–1.2 的兼容性均保留。
