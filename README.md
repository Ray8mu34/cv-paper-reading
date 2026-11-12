# CV Paper Reading v1.2.1（轻量化修订）

面向有 CV/ML 基础、尚未读过论文的研究生。默认**沿论文作者的章节和论证顺序**解释研究动机、方案选择、关键机制与数学、主要原图和实验证据，最后再作独立评价。保留技术深度，不用额外验收流程填充工作量。

## v1.2.1 改动

- **保留** v1.2.0 的原文 `reader.roadmap`、正文 `source_sections` 章节映射及覆盖/顺序校验；保留公式、关键图表与科学证据核查。
- **取消日常强制**：前四分之一阅读理解检验、逐章无提示复述、`reader-review.json` 人工验收记录、额外读者调用和多轮自查。
- **省去重复计划**：schema 1.3 的 `reader.throughline`、`reader.connections` 改为可选工作笔记；真正复杂的论文仍可填写。历史 schema 1.2 的合同保持不变。
- **每篇论文只做一次必要检查**：原文章序与覆盖、核心公式/图表/结论、构建产物。发现具体错误才针对性重查。
- **保留可选高级能力**：独立读者评测及相关脚本、`critical-review`、HTML 交互、复现与软件开发测试；不默认执行。

## 安装

从 [GitHub Releases](https://github.com/Ray8mu34/cv-paper-reading/releases/latest) 下载 Skill ZIP，解压后将其中 `cv-paper-reading/` 放在 `~/.codex/skills/cv-paper-reading/`；Windows PowerShell 常见路径是 `$env:USERPROFILE\.codex\skills\cv-paper-reading\`。该目录下应直接看到 `SKILL.md`，不要出现嵌套的两个 `cv-paper-reading/`。

也可以在目标目录尚不存在时，从仓库安装当前版本：

```powershell
git clone --branch v1.2.1 https://github.com/Ray8mu34/cv-paper-reading.git "$env:USERPROFILE/.codex/skills/cv-paper-reading"
```

新的 Codex 会话直接调用：

```text
请使用 $cv-paper-reading 精读这篇论文：<PDF或链接>。
按原文主要章节及论证顺序解释研究动机、方法选择、关键公式与实验原图，生成离线 HTML 报告。
```

## 日常使用（无需开发测试）

需要 Python 3.10+ 和 [pyproject.toml](pyproject.toml) 列出的运行依赖；不需要 PyTorch、模型权重或浏览器回归。Agent 阅读原文后填写 `analysis.json`，设置 `status=ready`。从 Skill 根目录执行：

```sh
python scripts/new_analysis.py INPUT --mode interactive-html --out WORK
# 填写 WORK/analysis.json 后：
python scripts/build_report.py --analysis WORK/analysis.json
python scripts/validate_skill.py --analysis WORK/analysis.json --require-artifacts
```

Markdown-only 时，在最后两条命令中添加 `--md-only`。验证脚本只检验结构与产物一致性，不会自己判断内容是否易懂。日常不调用 `prepare_reader_review.py`、不填写 `validation/reader-review.json`、不跑 pytest 或全量浏览器检查。用户明确要求评估首次阅读体验时，才启用保留的读者评测脚本及 `--require-reader-review`。

## 能力与边界

`quick`、`deep-md`、`interactive-html`、`critical-review` 均保留。对于深度报告，仍应对照**真实 PDF 目录**检查是否漏掉关键章节；程序只验证已经登记在 roadmap 中的章节。复杂公式和原图仍应讲透，但不会因为篇幅或内部检查配额而添加无关细节。所有来源与许可、离线 HTML/MathML、证据账本以及继承的数值/前端组件保留。旧版 schema 1.0–1.2 的报告仍然兼容。

[SKILL 主指令](SKILL.md) · [原文优先工作流](references/narrative-workflow.md) · [质量检查](references/quality-gates.md) · [Changelog](CHANGELOG.md)

## 仅开发 Skill 时运行

```sh
python -m pytest -q
python scripts/validate_skill.py
python scripts/package_skill.py --out dist/cv-paper-reading-v1.2.1.skill.zip
python scripts/check_release.py dist/cv-paper-reading-v1.2.1.skill.zip
```

这些程序测试**不会**在每篇论文阅读时触发。源码与安装包均在本仓库发布；安装包见 [v1.2.1 Release](https://github.com/Ray8mu34/cv-paper-reading/releases/tag/v1.2.1)。
