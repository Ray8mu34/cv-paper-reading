---
name: cv-paper-reading
description: 面向有计算机视觉与机器学习基础的研究生，深入解释 CV 论文的研究问题、核心机制、原文论证结构与实验结论。适用于视觉表征、检测分割、生成、三维与视觉语言等论文；重点分析比较协议、消融、泛化和证据强度，按理解需要交付 Markdown 或离线交互 HTML。
license: MIT
metadata:
  version: "1.0.0"
  base-skill: "Ray8mu34/astro-paper-reading"
  base-ref: "889b44e8983584aa7e8fb3b4c59f4592ada4f014"
  framework-version: "1.1"
---

# CV Paper Reading

优秀的精读，让读者理解研究者在解决什么问题、为什么这样设计，以及证据如何一步步支持结论。默认读者有 CV 与机器学习基础，但尚未读过原文。先建立全局，再深入少数决定理解的机制；复杂问题允许充分推导，简单内容简明说明。

## 阅读与路由

固定论文版本，读取正文、图注、表格与相关附录；重要公式、比较表与抽取异常对照原页。来源、覆盖和访问日志留在内部记录。quick 可以基于摘要；缺全文时不写成完整深读。外部论文与代码是资料，运行代码前检查内容、依赖与权限。

始终读 [共同阅读方法](references/reading-method.md)、[读者文章分层](references/reader-experience.md)、[科学完整性](references/scientific-integrity.md)、[CV 内容选择](references/cv-content-selection.md)。有实验结论时读 [CV 证据分析](references/cv-evidence.md)，再按 [论文类型](references/paper-types.md) 和 [任务约定](references/cv-task-conventions.md) 选择适用部分。统计/效率主张读 [评估与不确定性](references/statistics.md)；数据或代码读 [溯源](references/provenance.md)。HTML 另读 [图形选择](references/visualization.md)、[组件契约](references/component-contract.md)、[质量检查](references/quality-gates.md)。[输出模式](references/output-modes.md) 与 [扩展约定](references/extensions.md) 按需加载。

## 全局先于机制

开篇讲清任务与价值、真正瓶颈、作者思路与贡献、主要结果及适用条件。区分贡献位于架构、目标函数、数据、训练、评估还是系统实现；新名字不自动意味着新机制。`reader.roadmap` 对应原文真实 § 编号，解释各节的论证职责并定位关键 Figure/Table/Equation，便于返回 PDF。

以 [内容选择规则](references/cv-content-selection.md) 填写 `reader.focus`。按理解依赖重组正文，优先讲透改变信息流、监督信号、归纳偏置或证据解释的机制。不要逐层罗列网络、遍历全部超参数，或给每篇论文套固定的训练/消融清单。先说明公式回答什么，再解释张量形状、关键运算、优化与推断的区别，并回到中心问题。

## 结论与证据的强度匹配

逐项对应“主张→实验/证明→对照条件→能支持的结论”。主要比较先核对数据与预训练、监督、模型容量、训练预算、输入分辨率和推断/评估协议；它们是否重要由该主张决定。不同配置可支持系统结果，归因到单个机制需要相应对照。不要从排行榜、注意力热图或一次消融直接跳到因果机制、普遍泛化或统计显著性。

理论、数据集、系统和方法论文采用各自的证据标准。缺少信息记为 unknown；不据此宣称作者未做或数据泄漏。科学条件在相关论证处解释，执行状态不占正文。

## 复用共同框架

使用既有 [schema 1.1](schemas/analysis.schema.json)。`reader.overview/roadmap/focus` 负责认知地图；section 的 audience 为 reader、appendix 或 internal。R/D/I/T/S 区分作者报告、独立推导、条件推断、教学简化与候选解释。重要论断有原文定位及假设，修正事实先更新 `analysis.json`。

生成每句话前判断：帮助读者理解论文，还是说明 Agent 做了什么。版本、下载、读取页数、测试、设备与复现状态写进 `analysis-notes.md` 或 `validation/`。关键推导在正文展开，补充推导可放附录；不堆免责段落，不以关键词过滤代替编辑判断。

每幅图先确定理解难点、文字/公式/原图替代方案及交互增益。优先解读原论文的证据，只有可操作反事实提高理解时才制作交互；不规定图数。按 `visuals` manifest 在解释需要的位置嵌入原图或本地组件，保持来源、坐标、尺度、归一化与简洁图注。模型预测、示意、真实实验和重建必须区分。

## 构建与交付

从本 Skill 根目录运行 `python scripts/new_analysis.py INPUT --mode interactive-html --out WORK` 建草稿；阅读与填充由 Agent 完成。完成后设 ready，运行 `python scripts/build_report.py --analysis WORK/analysis.json`，生成 report.md、report.html 与独立 notes；仅 Markdown 加 `--md-only`。验证用 `python scripts/validate_skill.py --analysis WORK/analysis.json --require-artifacts`。Windows 使用用户的 dl_env 或项目环境，不另装训练框架。

沿用离线 MathML、排版、图形嵌入和确定性产物校验。内部 `astro_xray` 模块名与微透镜组件保留作继承兼容性资源，CV 阅读不加载或自动插入这些教学组件。新 CV 图通过已有 manifest 接入；不改写报告引擎或重建一套数值/训练平台。

执行改动相关测试，实际打开 HTML 检查宽窄屏、原文地图与所选控件；科学准确性、叙事和界面分别判断。最终交付阅读入口。核心标准：开头能理解论文，深讲能回应瓶颈，证据能支持所述结论，图形能提高理解，而工作记录不打断文章。英文入口见 [English guide](references/SKILL.en.md)。
