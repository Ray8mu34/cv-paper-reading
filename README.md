# CV Paper Reading

让有计算机视觉与机器学习基础、尚未读过原文的研究生，先理解研究问题、核心贡献、主要结论与原文论证结构，再深入关键机制和决定性证据。支持离线 HTML、Markdown 精读和批判性阅读。

**正式版：1.0.0。** 基于已验收的 [Astro Paper Reading](https://github.com/Ray8mu34/astro-paper-reading/tree/889b44e8983584aa7e8fb3b4c59f4592ada4f014)，继承阅读框架、专业排版、离线公式和图形嵌入，重点适配 CV 的内容选择与证据分析。

## 安装

这是完整的 Codex Skill，安装整个目录，保留 `SKILL.md` 相邻的代码、参考文档和资产。默认位置为 `~/.codex/skills/cv-paper-reading/`；自定义了 `CODEX_HOME` 时，使用其 `skills/` 目录。

**方式一：让 Codex 安装。** 在聊天中请求：

```text
请使用 $skill-installer 从 https://github.com/Ray8mu34/cv-paper-reading 安装根目录的 Skill，名称为 cv-paper-reading，版本 v1.0.0。
```

**方式二：使用 Git。** 目标目录尚不存在时，Windows PowerShell：

```powershell
git clone --branch v1.0.0 https://github.com/Ray8mu34/cv-paper-reading.git "$env:USERPROFILE/.codex/skills/cv-paper-reading"
```

macOS / Linux：

```sh
git clone --branch v1.0.0 https://github.com/Ray8mu34/cv-paper-reading.git "$HOME/.codex/skills/cv-paper-reading"
```

**方式三：使用 ZIP。** 下载 [正式版安装包](https://github.com/Ray8mu34/cv-paper-reading/releases/latest)，将其中的 `cv-paper-reading/` 解压至上述 `skills/` 目录。确认入口为 `skills/cv-paper-reading/SKILL.md`，不要额外嵌套同名目录。

安装后开启新聊天，确认可以调用 `$cv-paper-reading`。已有安装时，先将旧目录备份到 `skills/` 之外，再安装指定版本；阅读产物保存在独立工作目录，方便更新。Git 安装可用 `git fetch --tags` 后 `git checkout <版本标签>` 切换版本；跟随开发分支可切换至 `main` 后使用 `git pull --ff-only`。

## 调用

```text
请使用 $cv-paper-reading 深度解读这篇论文：<论文链接或 PDF>。
按照 Skill 的默认方式生成完整的离线 HTML 报告。
```

默认先给研究概览和对应原文 § 编号的论证导览，再围绕重要、困难的机制深入解释。关键推导充分展开；可视化按理解增益选择，不设数量指标。执行记录与来源全集独立保存，正文聚焦科学问题。

模式包括 `quick`、`deep-md`、`interactive-html`、`critical-review`，见 [输出模式](references/output-modes.md)。常规产物为 `report.html`、`report.md`、`analysis-notes.md`。HTML 的公式与嵌入图形可离线阅读，无需服务器。

## CV 内容与证据规则

- 判断贡献在表示、目标、数据、训练、推断、评估、理论还是系统，选择值得深讲的问题。
- 将主张与证据对应，区分配置表现、机制归因、泛化、稳定性和效率。
- 核对预训练、监督、模型、预算、分辨率及评估协议，解释相异条件下的结果。
- 分析消融支持多强的结论；明确定性图、注意力与特征图的证据范围。
- 按表征、检测分割、生成、视觉语言、三维几何等任务选择相关约定。

详见 [内容选择](references/cv-content-selection.md)、[证据分析](references/cv-evidence.md)、[任务约定](references/cv-task-conventions.md)、[统计与效率](references/statistics.md)、[可视化选择](references/visualization.md)。

## 运行环境与开发

需要 Python **3.10 或以上**，依赖见 [pyproject.toml](pyproject.toml)。优先使用现有项目环境。阅读和报告构建无需 PyTorch、下载权重或训练模型。

以下命令在仓库根目录执行，使用现有 Conda 环境 `dl_env`；其他环境使用其对应 Python：

```powershell
conda run -n dl_env python -m pip install -e .
conda run -n dl_env python scripts/validate_skill.py
conda run -n dl_env python scripts/new_analysis.py '<论文链接或PDF>' --mode interactive-html --out reading-work
```

Agent 阅读论文并填写 schema 1.1 的概览、导览、重点、正文、主张、来源与图形选择，设置 `status=ready` 后构建。CLI 负责确定性构建与检查，不会自行调用模型分析论文：

```powershell
conda run -n dl_env python scripts/build_report.py --analysis reading-work/analysis.json
conda run -n dl_env python scripts/validate_skill.py --analysis reading-work/analysis.json --require-artifacts
```

仅构建 Markdown 可加 `--md-only`。工作目录应放在安装目录之外。

## 示例与验证

[CV 比较协议示例](examples/protocol-reading/README.md) 使用明确标注的合成材料，展示相异 recipe、匹配对照与百分点/显著性的区别；表格和文字足够时不添加交互。

本版本已用于六个独立 Agent 的试读：ConvNeXt、DINOv2、LoFTR（两次独立生成）、3D Gaussian Splatting，以及 *Do Vision Transformers See Like Convolutional Neural Networks?*。用户审阅后接受当前版本。试读产物独立于仓库保存，这次试读不提供自动评分或量化效果保证。

开发检查与打包：

```powershell
conda run -n dl_env python -m pip install -e '.[test]'
conda run -n dl_env python -m pytest -q
conda run -n dl_env python scripts/build_report.py --analysis examples/protocol-reading/analysis.json
conda run -n dl_env python scripts/validate_skill.py --analysis examples/protocol-reading/analysis.json --require-artifacts
conda run -n dl_env python scripts/package_skill.py
conda run -n dl_env python scripts/check_release.py dist/cv-paper-reading-v1.0.skill.zip
```

浏览器检查需要本机 Chromium。运行记录写入被 Git 忽略的 `validation/`，不进入文章。框架继承、适配范围与验证层级见 [适配说明](docs/CV-ADAPTATION.md)。

`astro_xray` 包名、微透镜模块和 OGLE 夹具保留作兼容性与回归资源，CV 阅读不加载这些教学模块。新 CV 图形通过现有 manifest 接入，未另建训练框架。

## 来源与许可

使用 [MIT License](LICENSE)，保留 Astro Paper Reading 与 [Paper X-Ray](https://github.com/Wang-auspicious/paper-xray) 的来源、版权和设计参考。论文、原图和第三方数据遵循各自授权；本仓库不随附下载的论文或私人阅读材料。
