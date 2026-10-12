# CV 协议与证据分层运行夹具

`source.md` 是显式标注的合成教学材料；`analysis.json` 是其 schema 1.1 解读状态。四组固定数值用于检查比较条件、百分点、条件推断与正文/内部分层，不代表真实论文或模型实验。

从 Skill 根目录运行：

```text
python scripts/build_report.py --analysis examples/protocol-reading/analysis.json
python scripts/validate_skill.py --analysis examples/protocol-reading/analysis.json --require-artifacts
```

打开本地 `report.html`。表格与文字已足够解释本例，因此没有交互。此例是运行与设计检查，不代替使用真实 CV 论文的独立 Agent 试读。
