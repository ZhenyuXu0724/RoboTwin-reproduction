# 数据采集

当前复现任务为 `stack_blocks_two`，机器人本体为 `aloha-agilex`，动作类型为 `joint`。

## 配置

- [`configs/demo_smoke.yml`](../configs/demo_smoke.yml)：3 个 episode，用于快速验证采集链路。
- [`configs/demo_train20.yml`](../configs/demo_train20.yml)：20 个 episode，用于第一轮 ACT 训练。

两套配置都采集头部和腕部 RGB、末端位姿与关节位置，不采集深度和点云；目前关闭 domain randomization。

## 建议流程

1. 先用 `demo_smoke` 确认渲染、相机、动作和文件写入正常。
2. 随机抽查 episode 是否完整，确认相机顺序与 ACT 配置一致。
3. 再运行 `demo_train20`。
4. 训练前记录成功 episode 数、失败 episode 数、帧数分布和数据目录 manifest。

如果 OIDN 在当前机器不可用，可在应用本仓库补丁后设置：

```bash
export ROBOTWIN_RAY_TRACING_DENOISER=none
```

关闭降噪可能改变图像分布，因此实验记录里必须注明实际值。

