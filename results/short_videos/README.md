# RoboTwin 展示视频

这里保留两个可快速查看的轻量视频。它们展示专家动作与历史组合系统行为，不代表所有场景，也不替代逐场统计。

| 视频 | 来源 | 用途 |
| --- | --- | --- |
| [专家轨迹 episode 0](expert-episode0-preview.mp4) | `demo_train50_wrist_v2` 的专家视频 episode 0 | 展示目标任务与演示动作 |
| [历史 ACT 加 RGB-D 成功场景](historical-act-rgbd-seed700000.mp4) | 2026-10-06 冻结评测 seed 700000 | 展示组合系统堆叠行为 |

副本保持整段原视频的时间轴，转为宽 480 像素、10 FPS、H.264，无音轨。视频帧率不是机器人控制频率或真实执行速度。原始来源、大小与 SHA-256 见 [media-provenance.json](media-provenance.json)。

最新四组与消融共 100 场没有独立 MP4 输出，因此不使用旧视频替代它们的行为证据；最新逐步动作和原始评分见 [最终材料](../../experiments/2026-10-08-policy-comparison/README.md)。后续可在配置冻结后另行录制演示，并与正式统计分开标注。
