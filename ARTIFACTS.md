# Artifact Registry

大文件不进入 Git。每次上传数据、权重或完整视频后，在此补充稳定下载地址和校验值。

| 名称 | 类型 | 位置 | SHA-256 | 状态 |
| --- | --- | --- | --- | --- |
| `demo_smoke/stack_blocks_two` | 采集数据 | 本地 RoboTwin 工作区 | 待计算 | 未公开 |
| `demo_train20/stack_blocks_two` | 采集数据 | 本地 RoboTwin 工作区 | 待计算 | 未公开 |
| ACT smoke checkpoint | 模型权重 | 本地 checkpoint 目录 | 待登记 | 未公开 |
| ACT 评测视频 | 视频 | 本地 `eval_result/` | 待登记 | 未公开 |

## 登记要求

每个可下载 artifact 至少记录：

- 稳定 URL 或数据集/模型仓库 ID
- 文件或目录大小
- SHA-256（目录可使用 manifest）
- 生成它的实验目录
- 许可证或访问限制

