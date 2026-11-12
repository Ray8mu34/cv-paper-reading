# Schema 1.3：按原文顺序精读的合成示例

本示例**完全是合成教学材料，不是真实论文或模型实验**。源文档 `source.md` 自带 §1–§4，`analysis.json` 使用 v1.2.0 新版 schema 1.3 的 `reader.argument_route`、`source_sections` 和 `organization=paper-order`。公开主文章节逐节对应原文 §1、§2、§3、§3、§4；§3 被拆成数值证据与数学说明两个相邻部分，末尾另附技术延伸。

验证：在仓库根目录运行 `python scripts/build_report.py --analysis examples/original-order-v13/analysis.json --md-only`，再运行 `python scripts/validate_skill.py --analysis examples/original-order-v13/analysis.json --md-only --require-artifacts`。生成 `report.md`、`analysis-notes.md`。这只用于检查原文章序和构建链，不代表人类阅读测试或真实论文研究。
