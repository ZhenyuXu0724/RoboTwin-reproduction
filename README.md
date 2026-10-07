# RoboTwin Reproduction

这个仓库用于记录 RoboTwin 2.0 的复现过程、实验代码、配置、问题排查与结果。

当前主线是使用 **ACT** 在 `stack_blocks_two` 任务上完成从数据采集、训练、检查点验证到仿真评测的闭环。这里不会保存 RoboTwin 资源包、原始数据集或完整模型权重；大文件的位置与校验信息记录在 [`ARTIFACTS.md`](ARTIFACTS.md)。

## 当前状态

| 日期 | 任务 | 策略 | 数据 | 评测成功率 | 状态 |
| --- | --- | --- | --- | ---: | --- |
| 2026-09-30 | `stack_blocks_two` | ACT | `demo_smoke` | 0.0 | 已跑通评测，待排查策略行为 |
| 2026-09-30 | `stack_blocks_two` | ACT | `demo_train20` | 0.0 | 已跑通评测，待扩充数据与排查 |
| 2026-10-04 | `stack_blocks_two` | ExpertReplay | episode 0 | 1.0 | 单条专家轨迹回放通过 |
| 2026-10-05 | `stack_blocks_two` | ACT | `demo_train50` / 4000 epoch | 0/5 | checkpoint 验证通过；固定场景抓取仍失败 |
| 2026-10-05 | `stack_blocks_two` | ACT | 同模型执行 10 步 | 0/5 | 预测 chunk 50，单次配对诊断 |
| 2026-10-06 | `stack_blocks_two` | 修复 ACT | `demo_train50_wrist_v2` | 0/5 | 纯 ACT，五个固定开发场景 |
| 2026-10-06 | `stack_blocks_two` | 修复 ACT + RGB-D 校正 | `demo_train50_wrist_v2` | **19/20（95%）** | 冻结配置，20 个新种子，组合方案阶段成果 |

详见 [`experiments/2026-09-30-act-stack-blocks/`](experiments/2026-09-30-act-stack-blocks/README.md)。

最新阶段成果见 [`experiments/2026-10-07-stack-blocks-rgbd/`](experiments/2026-10-07-stack-blocks-rgbd/README.md)：修复 ACT、腕部相机配置和 RGB-D 校正代码，19/20 逐场景证据、失败分析与复现步骤。95% 是组合方案结果，额外使用深度、相机标定及已知颜色/尺寸，不能归因于纯 ACT。现有测试 20/20 通过。

此前排查记录见 [`experiments/2026-10-06-act-diagnostics/`](experiments/2026-10-06-act-diagnostics/README.md)。各轮完整补丁从锁定基线应用，勿重复叠加。

## 仓库内容

```text
configs/       可提交的任务和评测配置
docs/          环境、数据采集、训练和排错文档
experiments/   每次实验的完整记录
patches/       对上游 RoboTwin 的小范围修改
results/       汇总指标和适合公开的轻量结果
scripts/       可复用的辅助脚本
templates/     新实验模板
```

## 版本基线

- RoboTwin: `30954692d06ba7e89f7a6b76064f4062c488fa81`
- XPolicyLab: `a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5`
- 分支基线：RoboTwin `main`

完整记录见 [`upstream.lock.yml`](upstream.lock.yml)。复现实验前应先检出这些版本，再按需应用 [`patches/`](patches/README.md) 中的修改。

## 快速开始

1. 按 [`docs/environment.md`](docs/environment.md) 安装 RoboTwin 和 XPolicyLab。
2. 将 `configs/` 中的配置复制到 RoboTwin 的 `env_cfg/task_config/`。
3. 按 [`docs/data-collection.md`](docs/data-collection.md) 采集或准备数据。
4. 按 [`docs/act-training.md`](docs/act-training.md) 训练并评测 ACT。
5. 从 [`templates/experiment/`](templates/experiment/README.md) 复制一份目录，记录新的实验。

## 记录原则

每次实验必须记录上游 commit、配置文件、随机种子、数据规模、硬件与软件环境、运行命令、指标和失败现象。结果不理想也保留，避免重复踩坑。

## 大文件策略

Git 只保存代码、配置、文档、指标和少量展示媒体。以下内容不进入仓库：

- RoboTwin `assets/`
- 原始采集数据与训练数据
- 模型缓存和 checkpoint
- 完整评测视频与原始日志

公开时可把数据与权重放到 Hugging Face 或对象存储，并在 `ARTIFACTS.md` 中记录 URL、大小和 SHA-256。

## 发布状态

公开 GitHub 仓库已建立，初始记录已通过 PR #1 合并。最新 RGB-D 堆叠成果另行提交 PR 审阅。实验数据、权重和完整视频仍保存在本地，尚未提供公开下载地址。
