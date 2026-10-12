# CV 第一手定义与来源入口

具体结果、方法和机制首先引用当前论文、相关原论文及作者版本化代码。以下是核对评估和运行定义的入口，不是预先取得了所有实现或测试过这些库。

|来源|用途|
|---|---|
|[COCO 官方 cocoeval.py](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)|检测/分割/关键点评估，阈值、面积、最大候选与 ignore 的实际定义；记录使用的 revision|
|[Detectron2 evaluation 文档](https://github.com/facebookresearch/detectron2/blob/main/docs/tutorials/evaluation.md)|区分数据集 evaluator 与模型推断输出，确认任务协议|
|[PyTorch 随机性文档](https://docs.pytorch.org/docs/stable/notes/randomness.html)|运行环境、随机源与确定性设置的定义；具体版本按论文或实际环境核对|
|[Astro Paper Reading](https://github.com/Ray8mu34/astro-paper-reading/tree/889b44e8983584aa7e8fb3b4c59f4592ada4f014)|本 Skill 继承的 schema 1.1、阅读分层、离线构建与测试基线|
|[Paper X-Ray](https://github.com/Wang-auspicious/paper-xray)|原始阅读与视觉设计参考，许可证和版本记录位于 upstream|

链接是按需核对的入口，不将当前默认值反套到旧论文。主文、附录、模型卡、数据卡、仓库配置与实际执行分别记录来源；无法获得的信息标 unknown。来源清单属于独立记录，正文引用放在具体论断附近。
