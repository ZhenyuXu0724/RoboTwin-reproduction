# ACT on `stack_blocks_two` — 2026-09-30

## 目标

跑通 RoboTwin 2.0 中 ACT 的数据采集、训练、checkpoint 重载和仿真评测闭环。

## 固定条件

| 项目 | 值 |
| --- | --- |
| Task | `stack_blocks_two` |
| Policy | ACT |
| Embodiment | `aloha-agilex` |
| Action type | `joint` |
| Instruction type | `seen` |
| Domain randomization | 关闭 |
| Cameras | D435 head + D435 wrist |

## 运行记录

### `demo_smoke`

- 数据规模：3 个目标 episode
- 用途：采集、预处理、训练和评测链路检查
- 评测输出：成功生成视频与结果文件
- 成功率：`0.0`

### `demo_train20`

- 数据规模：20 个目标 episode
- 用途：第一轮小规模训练
- 评测输出：成功生成视频与结果文件
- 成功率：`0.0`

## 当前结论

基础链路已经能够运行，但现有策略没有完成任务。下一步重点不是润色结果，而是验证训练轨迹质量、相机顺序、state/action 编码、归一化，以及 checkpoint 在新进程中的确定性重载。

## 下一步

- [ ] 补齐实际 GPU、CUDA、Python 和训练环境信息
- [ ] 登记训练命令与超参数
- [ ] 统计有效成功轨迹数和帧数分布
- [ ] 完成 checkpoint 严格重载验证
- [ ] 保存训练样本上的离线预测对比
- [ ] 逐帧检查评测视频中的动作方向和幅值
- [ ] 通过上述检查后再扩大数据量

