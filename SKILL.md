---
name: cv-paper-reading
description: 面向具备计算机视觉与机器学习基础、尚未读过论文的研究生，默认按论文原有章节与论证顺序逐节讲清研究问题、动机、方法、关键数学、实验和局限；在相应章节加深技术解释，并区分作者结论与独立评价。支持 Markdown 与离线交互 HTML，保留科学核查、原图及证据分析。
license: MIT
metadata:
  version: "1.2.1"
  base-skill: "Ray8mu34/astro-paper-reading"
  base-ref: "889b44e8983584aa7e8fb3b4c59f4592ada4f014"
  framework-version: "1.3"
---

# CV Paper Reading

默认任务是**忠实而深入地带读原论文**。把论文章节及其论证顺序视为应当解释的研究成果：作者怎样提出问题、比较已有方案、引出方法、形成证据并收束结论，就按这条路线带读。模型的增值在于讲清每一步的缘由、机制和推导、读懂原图与实验，而不是优先发明另一套故事。读者有 CV/ML 基础但尚未读过这篇论文；可以深入，不为了简短跳过关键论证。不要推测作者未记录的心理历程或失败试验。

## 资料与必读规则

先固定论文版本，阅读正文、图表、图注与有关附录；核对原文的真实目录、图表和关键公式。全文不可得时如实降级为 quick/partial，不凭摘要补完章节。外部代码只作带版本的资料，运行前审查权限与依赖。

默认阅读 [原文顺序工作流](references/narrative-workflow.md)、[正文与内部记录分层](references/reader-experience.md)、[科学完整性](references/scientific-integrity.md)，交付前用 [轻量质量检查](references/quality-gates.md) 核对一次。其余参考按任务需要查阅：[阅读方法](references/reading-method.md)、[CV 内容选择](references/cv-content-selection.md)、[实验与证据分析](references/cv-evidence.md)、[论文类型](references/paper-types.md)、[任务约定](references/cv-task-conventions.md)、[统计与效率](references/statistics.md)、[溯源](references/provenance.md)。HTML 有需要时查看 [图形选择](references/visualization.md) 与 [组件契约](references/component-contract.md)；[输出模式](references/output-modes.md) 与 [扩展](references/extensions.md) 按需查看。勿为完成所有参考文件或检查表而额外增加阅读轮次。

## 默认以原文结构为骨架

**先还原，后解释，再评价**，步骤不可倒置：

1. 从论文的实际目录建立 `reader.roadmap`：按原文顺序逐项记录原章节编号、标题、该节要回答的问题/论证职责、主要图表与页码。以主文的主要章节为完整覆盖单位；附录按理解和证据需要单独交代。不得以模型自己归纳的五段式替代原文内容。
2. 顺着目录直接写 `reader.argument_route`：用一个自然段点明作者怎样从研究背景、问题/挑战走到技术选择、方法与证据，放在正文之前。只有原文论证特别复杂、确实需要整理时，再额外写内部 `reader.throughline`；不要重复造第二份相同的章节计划。概览与路线不提前详解公式和审查。
3. 正文 `sections` **默认保持原文主要章节的相对次序**。允许将相邻的较短原文章节合并为一节，或把一个核心原文章节拆为多个相邻的精讲节；但须保留每节对整体论证的作用、关键结论和必要证据。每个正文节填写 `source_sections`，明确对应原文 § 编号；只有当前后节关系确实复杂时，才在可选 `reader.connections` 中记录额外说明，不做逐节重复笔记。
4. 在原文相应位置逐节展开：为什么要做、作者提出了什么、方案怎样工作、公式如何得到与使用、结果究竟检验哪项主张。若原文先讲 Motivation/Challenges 再推公式，就先解释动机及技术选择；数学、实验配置和独立质疑不得无故提前打断作者的论证。
5. 完整重建作者的主要论证后，集中给出**独立评价**（关键协议、归因、未验证的替代解释、值得检验的问题）。科学条件若直接改变当前结果的解释，在结果旁自然说明一次；次要审计、工作日志和逐条免责声明不占据正文主线。

默认 `reader.organization="paper-order"`，使用 schema **1.3** 的章节映射和顺序校验。只有用户明确要求重组，或原文顺序确实无法支撑基本理解时，才能选择 `"restructured"` 并在 `reader.departure_reason` 说明具体例外；仍须保存完整原文地图与覆盖映射，不得以“更流畅”作空泛理由。章节内部可以补短暂的前置定义或直观例子；优先增加必要桥梁而不是调整整篇顺序。模型改写的标题可更清楚，但要保留显眼的原文 § 对应，不能暗中把作者论证替换为模型推断。

`reader.focus` 控制**精讲的深度**，不控制颠倒章序。方法、理论、基准、经验与系统论文按各自真实证据结构解读；不强制每篇都有挑战三分法、消融、网络结构或训练流水线。详见 [原文顺序工作流](references/narrative-workflow.md)。

## 技术讲解与证据

首次遇到术语时解释它在当前问题中的作用；重要机制处再详细引入输入输出、索引/张量形状、操作、优化/推断差异与必要推导。公式出现前先解释**作者为什么需要这个公式**，而不是先给联合损失再补动机。区分论文原有的决策依据、教学举例与模型新增的推断；不能编造作者的尝试顺序。复杂机制允许长讲，不按每个 loss 或超参数平均分配篇幅。

实验章节按原文的实验逻辑解释：实验要检验什么→数据、基线、指标、关键控制→图表里看到什么→该结果回答了什么。优先在**作者使用该图的位置**嵌入原文总体框架图和关键结果图，解释图的结构、轴、比较对象与最有信息量的差异。不可把一组重要原图无理由变成数字流水账；无原图时注明不可获取，不伪造。交互只在反事实操作实际改善理解时增加。

结论逐项核对“作者主张→原文证据→必要条件→可支持的范围”。对训练预算、额外数据、监督、模型容量、推断协议等只检查与本结论有关的条件，区分性能与机制归因。作者报告、独立推导、条件推断、教学简化、候选解释分别按 R/D/I/T/S 记录。重要缺口按原文位置核对，unknown 不等于作者未做。

**编辑纪律**：不要在每段后附加“不能证明……”“不代表……”“需要注意……”来展示审慎；只在相关证据旁交代会改变理解的真实条件一次。独立审查放在作者论证讲完之后集中讨论。既不能删掉改变结论的关键限制，也不能在开篇列出一长串未来才需用到的免责条件。写作以解释为主，资料取得/核查/运行状态进内部记录。

## 状态、构建、验收与交付

新任务继续使用 [schema 1.3](schemas/analysis.schema.json)：`reader.overview` 是简短概览，`argument_route` 是前置原文论证路线，`roadmap` 是文后真实章节索引，`organization/departure_reason` 控制必要的顺序例外，`sections[].source_sections` 建立章节对应。**`throughline` 和 `connections` 是按需使用的工作笔记，schema 1.3 不再强制填写**；没有复杂结构断点就留空。旧 schema 1.0–1.2 的生成与验证规则保持兼容。已有的科学证据、覆盖和必要参数记录仍保留在 `analysis-notes.md`，不要为普通精读额外建立多份审读日志。`audience=appendix` 只能容纳补充科学内容，不能藏核心方法。

在 Skill 根目录：

```sh
python scripts/new_analysis.py INPUT --mode interactive-html --out WORK
# Agent 读原文并填写 analysis.json；完成后置 status=ready
python scripts/build_report.py --analysis WORK/analysis.json
python scripts/validate_skill.py --analysis WORK/analysis.json --require-artifacts
```

仅 Markdown 构建/检查加 `--md-only`。**普通论文精读只需一次合并式交付检查**：对照原文目录确认主要章序与覆盖；抽查关键公式、核心实验图表和重要结论是否准确；确认正文连贯、文件成功生成。只修正实际发现的问题。**不强制**前四分之一理解测试、逐章无提示复述、第二次模拟读者、`reader-review.json` 或多轮评审；不要仅为了验证而另起模型调用。有人明确要求教学效果评测时，才可额外运行 `prepare_reader_review.py` 并使用 `--require-reader-review`；这些工具保留为可选能力，不参与日常流程。

校验脚本检查已登记章节的覆盖映射、相对顺序、状态及产物一致性；**不能自动判断解释是否准确好懂**。普通阅读不运行 pytest、浏览器/UI 回归、数值基准、训练复现或发布检查；这些只在相应代码变更或用户明确要求时运行。保留离线 MathML、确定性 HTML、图片 manifest 与继承组件，CV 报告不会自动使用微透镜演示。交付 Markdown/HTML 阅读入口。英文指引见 [English guide](references/SKILL.en.md)。
