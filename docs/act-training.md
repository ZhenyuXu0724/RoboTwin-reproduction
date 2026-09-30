# ACT 训练与评测

## 当前实验

- 任务：`stack_blocks_two`
- Embodiment：`aloha-agilex`
- 动作：`joint`
- 数据：`demo_smoke`、`demo_train20`
- 指令类型：`seen`

## 训练前检查

- 数据中的相机名称与顺序必须和训练配置一致。
- state/action 维度必须与 `aloha_agilex` 的机器人配置一致。
- 保存训练配置、归一化统计、随机种子和最终 checkpoint。
- 生成固定输入及对应 action，供新进程重载 checkpoint 后做一致性验证。

## 评测记录

当前两轮评测均成功生成视频和 `_result.txt`，但成功率为 `0.0`。这说明链路能够运行，不等于策略已经学会任务。

下一轮建议依次检查：

1. 训练集 episode 是否均为真实成功轨迹。
2. 相机顺序、颜色通道和归一化是否与训练一致。
3. qpos/action 的拼接顺序、单位和反归一化是否一致。
4. 用训练样本离线回放预测，区分模型问题和仿真部署问题。
5. 20 条轨迹不足时再扩大数据量，而不是先盲目调整超参数。

具体已知问题见 [`troubleshooting.md`](troubleshooting.md)。

