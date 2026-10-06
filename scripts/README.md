# Scripts

这里用于保存不属于 RoboTwin 上游、但对复现有帮助的辅助程序，例如：

- checkpoint 重载与推理一致性验证
- 数据集 manifest 和 SHA-256 生成
- 指标聚合
- 实验环境快照

当前 RoboTwin 工作区已有 `scripts/validate_act_checkpoint.py`，待其接口稳定并完成一次成功验证后再同步到这里，避免把未验证的工具作为复现入口发布。

