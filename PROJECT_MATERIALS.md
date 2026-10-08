# RoboTwin 项目材料总索引

项目目标是在 RoboTwin 的 `stack_blocks_two` 任务上完成双臂操作策略的完整生命周期，并解释学习策略与几何纠偏各自的效果。当前已完成数据采集、ACT 与 DP 训练、同场景比较、DP 失败诊断以及 ACT 释放分支消融。

本页作为项目入口和证据导航。技术报告将在后续单独撰写。

## 从任务到结论

| 环节 | 回答的问题 | 材料 |
| --- | --- | --- |
| 任务和环境 | 机器人、观测、动作与成功条件是什么 | [环境记录](docs/environment.md)、[任务与相机配置](experiments/2026-10-08-policy-comparison/camera-and-task.yml) |
| 专家数据 | 训练目标是否正确，图像是否可用 | [采集说明](docs/data-collection.md)、[数据审计](experiments/2026-10-08-policy-comparison/dataset-audit.json)、[固定划分](experiments/2026-10-08-policy-comparison/split-40-10.json) |
| ACT 修复 | 为什么旧训练未达到预期，怎样验证实现问题 | [早期诊断](experiments/2026-10-06-act-diagnostics/README.md)、[ACT 修复与训练](experiments/2026-10-07-stack-blocks-rgbd/README.md) |
| 策略对照 | 相同数据和更新预算下，两套方案表现怎样 | [最终四组比较](experiments/2026-10-08-policy-comparison/FOUR_WAY_COMPARISON.md)、[逐场 CSV](experiments/2026-10-08-policy-comparison/paired-results.csv) |
| DP 失败诊断 | 失败是否仅由闭环偏移或标签错位造成 | [诊断记录](experiments/2026-10-08-policy-comparison/DP_FAILURE_DIAGNOSIS.md)、[550 点预测证据](experiments/2026-10-08-policy-comparison/dp-expert-prediction-results.json) |
| 组件消融 | 保留抓取纠偏后，释放分支是否仍有贡献 | [消融记录](experiments/2026-10-08-policy-comparison/ACT_ABLATION.md)、[协议](experiments/2026-10-08-policy-comparison/ablation-protocol.json) |
| 复现与展示 | 代码、权重、原始结果和视频如何找到 | [复现入口](docs/materials-reproduction.md)、[大文件登记](ARTIFACTS.md)、[展示材料](results/short_videos/README.md) |

## 可以直接使用的结果

同一批 20 个正式场景：纯 ACT 3/20、纯 DP 0/20、ACT 加 RGB-D 19/20、DP 加 RGB-D 3/20。网络输入均为 RGB 与关节，深度只进入外部控制器。这些是当前方案的实测结果，不是总体算法排名。

同场景事后消融：仅抓取纠偏 14/20，完整纠偏 19/20。完整释放分支挽回 5 场，没有反向退化；首次释放介入前两组动作完全一致。贡献属于整个释放分支，不是网络训练修复的贡献。

DP 在专家训练观测上已存在动作预测与夹爪时序误差，标签和转换检查未发现统一错位。此证据支持继续分析条件动作拟合、采样与执行周期，尚不能把其中一项认定为唯一失败原因。

## 历史与最终材料的关系

- [首次闭环](experiments/2026-09-30-act-stack-blocks/README.md)：小样本采集、训练和评估入口。
- [ACT 排查](experiments/2026-10-06-act-diagnostics/README.md)：抓取、相机和训练实现问题的过程证据。
- [RGB-D 阶段成果](experiments/2026-10-07-stack-blocks-rgbd/README.md)：修复 ACT 和另一批 20 场的历史 19/20。
- [最终对照与消融材料](experiments/2026-10-08-policy-comparison/README.md)：当前主结论、完整配对记录与证据。

两批 19/20 来自不同种子范围，分别保留，不合并为一个配对实验。失败的训练尝试与控制器初始化修复前结果保存在本地清单中，未混入正式分母。

## 交付范围

公开内容包括代码补丁、参数、指标、预测诊断数组、已有实验记录和展示视频。原始轨迹、处理数据、权重、完整日志与历史视频保存在本地，文件登记见各轮清单。面向老师展示时，建议先阅读本页和最终比较，再检查消融证据及失败案例。

独立技术报告、通用物体检测成果、多训练种子统计、长期稳定性与真实机器人验证不在本次材料交付范围内。
