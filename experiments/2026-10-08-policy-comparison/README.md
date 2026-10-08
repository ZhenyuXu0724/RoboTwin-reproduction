# RoboTwin 策略对照与消融材料

本目录归档双臂堆叠项目的最终实验材料，连接训练配置、同场景评测、DP 失败诊断和 ACT 释放纠偏消融。技术报告另行撰写；这里提供材料索引、既有实验记录和可核查证据。

## 最终结果

50 条演示按固定 40/10 划分，ACT 与 DP 各训练 2000 轮、80000 次更新。四组正式评测使用同一批 20 个场景，种子 2700000 至 4600000、间隔 100000，初始位置逐场一致，每场最多 800 个动作步。

| 方案 | 成功数 | 实验范围 |
| --- | --- | --- |
| 纯 ACT | 3/20 | 正式配对评测 |
| 纯 DP | 0/20 | 正式配对评测 |
| ACT 加完整 RGB-D 纠偏 | 19/20 | 正式配对评测 |
| DP 加完整 RGB-D 纠偏 | 3/20 | 正式配对评测 |
| ACT 加仅抓取纠偏 | 14/20 | 同场景事后组件消融 |

95% 是组合系统成绩。网络只接收三路 RGB 和关节；深度、标定、已知颜色及 5 cm 方块尺寸用于外部控制器。方块真值只用于评分。ACT 和 DP 保留不同的动作块、观测历史、损失与精度，本轮不构成只改变架构的严格消融，也不支持总体算法排名。

## 阅读顺序

1. [项目材料总索引](../../PROJECT_MATERIALS.md)：从任务目标到结果归因的材料关系。
2. [四组比较](FOUR_WAY_COMPARISON.md)及 [80 场正式结果](four-way-results.json)：同场景配对效果。
3. [DP 失败诊断](DP_FAILURE_DIAGNOSIS.md)：550 个专家观测、数据对齐和冻结权重执行响应。
4. [ACT 释放分支消融](ACT_ABLATION.md)及 [消融结果](ablation-results.json)：完整组额外挽回 5 场，无反向退化。
5. [复现入口与依赖](../../docs/materials-reproduction.md)：恢复代码、准备数据和权重、检查证据。

## 配置与数据

| 文件 | 内容 |
| --- | --- |
| [camera-and-task.yml](camera-and-task.yml) | 任务、相机安装及采集设置 |
| [split-40-10.json](split-40-10.json) | 固定训练与验证轨迹编号 |
| [dataset-audit.json](dataset-audit.json) | 轨迹 SHA-256、动作对齐、图像与视频检查 |
| [collection-manifest.json](collection-manifest.json) | 采集来源和过程记录 |
| [dp-config.json](dp-config.json)、[dp-experiment.json](dp-experiment.json) | DP 参数、数据和冻结指纹 |
| [dp-training-metrics.jsonl](dp-training-metrics.jsonl) | 2000 轮训练指标 |
| [dp-training-completion.json](dp-training-completion.json)、[dp-preflight.json](dp-preflight.json) | 完成状态与训练前检查 |
| [weights-registry.json](weights-registry.json) | ACT、归一化统计及 DP EMA 权重位置、大小、SHA-256 |

ACT 训练参数和实现修复见上一轮的 [训练与控制器快照](../2026-10-07-stack-blocks-rgbd/README.md)。DP 权重含原模型与 EMA，本轮评测使用 EMA。

## 逐场结果与诊断证据

[paired-results.csv](paired-results.csv) 包含四组正式评测和新增消融共 100 场，按种子与方案排列；其中 20 场消融复用此前正式评测作为基线，不能当成新增独立测试场景。

DP 诊断包括 [观测索引](dp-expert-points.jsonl)、[预测数组](dp-expert-predictions.npz)、[分阶段结果](dp-expert-prediction-results.json)、[分析](dp-diagnosis-analysis.json)、[输入审计](dp-data-audit.json)和 [核验](dp-diagnosis-verification.json)。[单场响应](dp-execution-response.jsonl)、[动作轨迹](dp-diagnostic-trace.jsonl)及 [结果](dp-diagnostic-rollout.json)属于诊断重放，不并入成功率分母。

消融的 [预先声明协议](ablation-protocol.json)、[完成状态](ablation-completion.json)与结果分别保留。冻结 manifest 的状态记录可能仍为 running/evaluating，它表示建立或更新该快照时的阶段；最终完成以独立 completion 文件及结果文件为准，历史 manifest 不回写。

## 代码和校验

[dp-workflow.patch](dp-workflow.patch) 恢复 `scripts/dp_comparison/` 的 24 个脚本，包括训练、评测、输入契约测试、纠偏缺陷回归、失败诊断和消融。它依赖上一轮的 RoboTwin、ACT 和历史训练依赖补丁，应用顺序见复现说明。

[source-snapshot.json](source-snapshot.json) 校验本次归档的源码；正式实验的冻结源码哈希保留在原实验与协议中。公开 JSON 的机器路径已替换为 `${ROBOTWIN_ROOT}`，因此公开副本的文件哈希与原始文件哈希不同。[publication-manifest.json](publication-manifest.json) 校验公开文件，[export-verification.json](export-verification.json)记录本次归档的结果、配对、原冻结源码和权重核验。

[local-artifact-inventory.json](local-artifact-inventory.json) 登记 704 个本地文件及大小，轻量证据另附 SHA-256。大文件仍在原工作区，不复制或公开上传；这份清单是路径模板，不是下载地址。大型处理数据没有在此次整理中重新逐字节哈希，其来源和对齐检查见数据审计。

## 结论范围

本项目完成单任务采集、训练、部署、比较、故障诊断与组件归因。只有一个训练种子；20 个正式测试场景不代表广泛泛化。释放消融在已看过的场景上进行，隔离的是整个释放分支，不能分解分支内部各机制。持续抬升仅为代理指标，官方成功未额外检查长期释放稳定性。纠偏识别是针对已知颜色与尺寸的几何估计，不是通用目标检测器。

原始数据、权重和完整历史视频尚无公开下载地址。材料支持检查证据和恢复代码；新环境完整重跑仍需准备仿真资源、环境与大文件。
