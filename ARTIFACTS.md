# Artifact Registry

大文件不进入 Git。每次上传数据、权重或完整视频后，在此补充稳定下载地址和校验值。

| 名称 | 类型 | 位置 | SHA-256 | 状态 |
| --- | --- | --- | --- | --- |
| `demo_smoke/stack_blocks_two` | 采集数据 | 本地 RoboTwin 工作区 | 待计算 | 未公开 |
| `demo_train20/stack_blocks_two` | 采集数据 | 本地 RoboTwin 工作区 | 待计算 | 未公开 |
| ACT smoke checkpoint | 模型权重 | 本地 checkpoint 目录 | 待登记 | 未公开 |
| ACT 评测视频 | 视频 | 本地 `eval_result/` | 待登记 | 未公开 |
| `demo_train50_wrist_v2/stack_blocks_two` | 50 条采集数据 | 本地 RoboTwin 工作区 | 各轨迹校验值见本轮 `evidence.json` 的 collection manifest | 未公开 |
| repaired ACT / 2000 epoch | 模型权重 | 本地 `repaired_train2000_20261006_191143` | `e242a25826d8ace1d41999c6bf04b695e9a60027a31d6fbbdde897a6dd662542` | 未公开 |
| repaired ACT dataset stats | 归一化统计 | 同一训练目录 | `de075b0ec6f54051b9060f774f41c2f23d655500fb62bee089a60859fc102995` | 未公开 |
| visual_guard_v2 / test20 | 完整评测视频 | 本地 `visual_guard_test20_20261006_231054` | 待登记 | 未公开 |

本轮代码补丁、配置、逐场景结果及证据已归档至 [2026-10-07 实验记录](experiments/2026-10-07-stack-blocks-rgbd/README.md)。公开仓库不包含数据或权重，尚不能直接下载后复现训练与评测。

## 登记要求

每个可下载 artifact 至少记录：

- 稳定 URL 或数据集/模型仓库 ID
- 文件或目录大小
- SHA-256（目录可使用 manifest）
- 生成它的实验目录
- 许可证或访问限制

## 最终对照与消融材料

当前大文件的路径、字节大小和权重 SHA-256 见 [权重登记](experiments/2026-10-08-policy-comparison/weights-registry.json)。[本地材料清单](experiments/2026-10-08-policy-comparison/local-artifact-inventory.json) 登记 704 个文件，`${ROBOTWIN_ROOT}` 表示运行工作区，不是公开下载地址。

| 材料 | 位置或证据 | 公开状态 |
| --- | --- | --- |
| 50 条演示与 50 个专家视频 | `data/demo_train50_wrist_v2/stack_blocks_two/aloha_agilex/`；[原始审计](experiments/2026-10-08-policy-comparison/dataset-audit.json) | 大文件本地保存 |
| ACT 处理数据 | `XPolicyLab/policy/ACT/processed_data/demo_train50_wrist_v2/stack_blocks_two/aloha_agilex-joint/` | 本地保存；本次未重算全部大型文件哈希 |
| ACT 权重和归一化统计 | [weights-registry.json](experiments/2026-10-08-policy-comparison/weights-registry.json) | SHA-256 已复核，本地保存 |
| DP 2000 轮模型与 EMA | `data/dp_compare_20261007/run2000_v2/training/2000.pt`；同上权重登记 | SHA-256 已复核，本地保存 |
| 正式四组及新增消融 | [配对结果](experiments/2026-10-08-policy-comparison/paired-results.csv) | 100 场评分公开；完整轨迹和日志本地保存 |
| DP 550 个专家观测预测 | [诊断材料](experiments/2026-10-08-policy-comparison/README.md) | 观测索引、预测数组与诊断结果公开；图像来自本地数据 |
| 专家与历史 ACT RGB-D 展示视频 | [来源与说明](results/short_videos/README.md) | 两个轻量转码副本公开 |

当前四组与消融评测目录没有独立 MP4 输出；其行为证据为逐步动作轨迹、日志和评分。公开成功视频来自历史 seed 700000，不冒充最新配对场景的录像。

本次清单对轻量证据、日志和视频计算 SHA-256；大型数据/模型记录大小并引用已有审计或独立权重登记。没有为未逐字节复核的文件声明新的内容校验值。
