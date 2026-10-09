# RoboTwin Reproduction

RoboTwin 双臂堆叠任务的复现与实验分析：从专家数据采集、ACT 实现修复和策略训练，到 ACT 与 Diffusion Policy 对照、RGB-D 纠偏及组件消融。

## 技术报告

**推荐先阅读 [复现技术报告初稿](docx/robotwin-reproduction-report.md)**：系统梳理项目目标、数据采集、ACT 实现修复、RGB-D 纠偏方法、ACT 与 DP 配对实验、释放分支消融及误差分析，并说明结论边界与后续工作。

报告中的 19/20 成功率属于 **ACT 加外部 RGB-D 纠偏的组合系统**；纯 ACT 为 3/20。报告区分实测结果与待验证解释，未将系统效果归为纯策略性能或算法总体排名。

查阅具体证据可继续进入 [项目材料总索引](PROJECT_MATERIALS.md) 和 [最终实验材料](experiments/2026-10-08-policy-comparison/README.md)。

## 当前结果

50 条演示，固定 40 条训练、10 条验证，ACT 与 DP 各完成 2000 轮、80000 次更新。以下使用同一批 20 个场景，每场最多 800 个动作步：

| 方案 | 成功数 | 范围 |
| --- | --- | --- |
| 纯 ACT | 3/20（15%） | 正式配对评测 |
| 纯 DP | 0/20（0%） | 正式配对评测 |
| ACT 加 RGB-D 纠偏 | 19/20（95%） | 正式配对评测 |
| DP 加 RGB-D 纠偏 | 3/20（15%） | 正式配对评测 |
| ACT 加仅抓取纠偏 | 14/20（70%） | 同场景事后消融 |

95% 属于 ACT 与外部几何纠偏的组合系统。策略网络只接收 RGB 与关节；外部控制器另使用深度、相机标定和已知方块颜色/尺寸。当前单训练种子、20 个场景及不同策略执行周期，不能支持总体算法排名或广泛泛化结论。

释放分支在保留抓取纠偏时额外挽回 5 场，无反向退化；首次释放介入前动作完全一致。DP 诊断在 550 个专家观测上检查预测、夹爪时序与输入对齐，并记录单场执行响应。详见 [四组比较](experiments/2026-10-08-policy-comparison/FOUR_WAY_COMPARISON.md)、[DP 诊断](experiments/2026-10-08-policy-comparison/DP_FAILURE_DIAGNOSIS.md)和 [ACT 消融](experiments/2026-10-08-policy-comparison/ACT_ABLATION.md)。

## 材料导航

| 材料 | 入口 |
| --- | --- |
| 复现全过程与技术分析 | [技术报告初稿](docx/robotwin-reproduction-report.md) |
| 项目流程与证据关系 | [PROJECT_MATERIALS.md](PROJECT_MATERIALS.md) |
| 当前结果、配置和原始评分 | [最终材料目录](experiments/2026-10-08-policy-comparison/README.md) |
| 代码恢复与运行入口 | [复现说明](docs/materials-reproduction.md) |
| 权重、数据与完整日志位置 | [ARTIFACTS.md](ARTIFACTS.md) |
| 展示视频与来源 | [展示材料](results/short_videos/README.md) |
| 各轮结果汇总 | [summary.csv](results/summary.csv) |

## 历史实验

- [2026-09-30 首次闭环](experiments/2026-09-30-act-stack-blocks/README.md)：小样本 ACT 训练与评估。
- [2026-10-06 ACT 排查](experiments/2026-10-06-act-diagnostics/README.md)：失败行为及实现检查。
- [2026-10-07 RGB-D 阶段成果](experiments/2026-10-07-stack-blocks-rgbd/README.md)：修复 ACT 和历史新场景 19/20。
- [2026-10-08 对照与消融](experiments/2026-10-08-policy-comparison/README.md)：另一批配对场景及最终证据。

历史与本轮 19/20 使用不同种子，分别保留；失败尝试不抹去，也不混入有效测试分母。

## 基线与验证

RoboTwin `30954692d06ba7e89f7a6b76064f4062c488fa81`，XPolicyLab `a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5`。锁定记录见 [upstream.lock.yml](upstream.lock.yml)。各轮完整补丁从干净基线应用，勿重复叠加。

公开材料可通过标准库离线核验：

```bash
python scripts/verify_materials.py
```

恢复工具已在干净锁定基线上检查四份补丁和 24 个源码快照。当前 ACT 20 项、DP 输入契约 5 项、纠偏初始化回归 1 项、消融契约 2 项测试全部通过。本次只整理材料，没有重训或重新运行正式评测。

## 大文件与交付范围

Git 保存轻量代码、配置、结果和明确标注来源的展示媒体。原始演示、处理数据、模型权重和完整历史日志/视频仍在本地，尚无公开下载地址，因此当前是可检查的实验归档，完整重跑仍需准备环境与大文件。

技术报告初稿已整理为 [Markdown 文档](docx/robotwin-reproduction-report.md)，位于 `docx/` 目录。当前结果仅覆盖仿真中的已知方块任务，未验证真实机器人、多任务泛化和长期释放稳定性。
