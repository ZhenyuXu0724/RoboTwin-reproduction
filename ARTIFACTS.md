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
