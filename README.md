# CV Paper Reading

面向有 CV 与机器学习基础、尚未读过原文的研究生，先讲清研究问题、瓶颈、贡献、主要结果和原文论证地图，再深入决定理解的机制。

本项目以已验收的 [Astro Paper Reading](https://github.com/Ray8mu34/astro-paper-reading/tree/889b44e8983584aa7e8fb3b4c59f4592ada4f014) 为蓝本，继承其 schema 1.1、报告构建、离线 MathML、排版、manifest 图形嵌入和读者/内部记录分层。CV 版本为 **1.0.0**，核心改动在内容选择与证据分析，继承范围见 [适配说明](docs/CV-ADAPTATION.md)。

## CV 版本重点

- 定位贡献在表示、目标、数据、训练、推断、评估、理论还是系统，选择真正值得深讲的问题。
- 将主要主张与证据逐项对应，区分配置表现、机制归因、泛化、稳定性和效率。
- 按问题核对预训练、监督、模型、预算、分辨率及评估协议，保留条件相异的系统结果。
- 分析消融能支持多强的结论；定性图、注意力与特征可视化各有其证据范围。
- 按分类表征、检测分割、生成、视觉语言、三维几何等任务加载约定，不给所有论文套训练/消融模板。

正文保持连贯，关键推导充分展开；原文 § 导览便于回到 PDF。执行记录、来源全集与复现状态独立保存。图形按理解需要选择，不设数量目标。

## 使用

本目录是一个完整 Skill。安装时将整个 `cv-paper-reading/` 放到 `~/.codex/skills/`，或把 `dist/cv-paper-reading-v1.0.skill.zip` 解压到该目录，确保入口为 `~/.codex/skills/cv-paper-reading/SKILL.md`。保留相邻 assets、schemas 与 Python 代码。

在新聊天中调用：

```text
使用 $cv-paper-reading 深入解读这篇 CV 论文：<论文链接或PDF>。
读者具备 CV 基础但尚未看过原文。先讲研究问题、贡献、结果和原文结构，
再深入关键机制，按比较协议与证据强度解释实验，输出离线 HTML。
```

也可在当前工作区明确指定本目录的 SKILL.md。模式沿用 `quick`、`deep-md`、`interactive-html`、`critical-review`，见 [输出模式](references/output-modes.md)。读取与填写由 Agent 完成，CLI 不会独立分析论文或调用模型。

Python ≥3.10，使用项目环境或用户的 Conda 环境，例如：

```powershell
conda run -n dl_env python scripts/validate_skill.py
conda run -n dl_env python scripts/new_analysis.py '<论文链接或PDF>' --mode interactive-html --out reading-work
```

若当前环境缺构建依赖，先检查环境，再用该环境安装 `python -m pip install -e .`。与天文版共享 NumPy、SciPy、Mistune、PyYAML、jsonschema、latex2mathml；阅读和构建无需新装 PyTorch、下载权重或训练模型。

Agent 完成 schema 1.1 的 overview、roadmap、focus、sections、claims、来源与图形选择，置 `status=ready` 后构建：

```powershell
conda run -n dl_env python scripts/build_report.py --analysis reading-work/analysis.json
conda run -n dl_env python scripts/validate_skill.py --analysis reading-work/analysis.json --require-artifacts
```

生成 `report.md`、离线 `report.html` 与独立 `analysis-notes.md`；仅 Markdown 加 `--md-only`。HTML 可直接在现代浏览器打开，阅读与内嵌控件不需要服务器或网络。

## 示例与验证

[CV 比较协议示例](examples/protocol-reading/README.md) 使用明确标注的合成材料，展示相异 recipe、匹配对照与百分点/显著性的区别。表格和解释已经足够，本例没有交互。它验证运行管线和设计意图，真实论文的科学解读仍需实际阅读评估。

```powershell
conda run -n dl_env python scripts/build_report.py --analysis examples/protocol-reading/analysis.json
conda run -n dl_env python scripts/validate_skill.py --analysis examples/protocol-reading/analysis.json --require-artifacts
conda run -n dl_env python -m pytest -q
conda run -n dl_env python scripts/package_skill.py
conda run -n dl_env python scripts/check_release.py dist/cv-paper-reading-v1.0.skill.zip
```

测试依赖沿用基线的 `.[test]`。本地检查记录存入 validation，不进入文章。`astro_xray` 的包名、lensing 模块、single/binary-lens 资产及 OGLE 夹具保留作继承兼容性与回归资源，CV 任务不加载它们；已有的 lensing browser/numerics 命令仍只验证这些继承组件。新 CV 图通过现有 manifest 接入，没有另建训练或可视化框架。

## 关键参考

- [CV 内容选择](references/cv-content-selection.md)
- [CV 证据分析](references/cv-evidence.md)
- [CV 任务约定](references/cv-task-conventions.md)
- [评估、不确定性与效率](references/statistics.md)
- [可视化选择](references/visualization.md)
- [共同组件契约](references/component-contract.md)

## 来源与许可

沿用 [MIT License](LICENSE)，保留 Astro Paper Reading 与 [Paper X-Ray](https://github.com/Wang-auspicious/paper-xray) 的来源、版权和设计参考。论文、原图和第三方数据各遵循自己的授权。CV 规则、代码回归和合成运行示例的检查分别记录，不把结构测试等同于科学论断被验证。
