# 问题排查

## OIDN 初始化或渲染异常

症状：光线追踪渲染在 OIDN 初始化时失败或卡住。

当前处理：应用 [`0001-configurable-ray-tracing-denoiser.patch`](../patches/0001-configurable-ray-tracing-denoiser.patch)，通过 `ROBOTWIN_RAY_TRACING_DENOISER` 选择 denoiser。测试时可设为 `none`。

注意：渲染设置变化可能带来训练/评测视觉域偏差，必须在实验记录中保留。

## ACT 评测可以运行但成功率为 0

已确认：评测进程能够启动、生成视频并写出结果。

尚未确认：

- 训练轨迹的任务成功率与质量
- checkpoint 是否在全新进程中严格加载并复现参考输出
- 训练与评测相机顺序是否一致
- state/action 的维度、顺序和归一化是否一致
- 预测动作是否在仿真中被正确执行

不要仅以“生成了视频”判断部署正确；应逐层验证数据、模型输出和机器人执行。

