# 堆叠方块阶段成果：ACT + RGB-D 视觉校正

实验日期：2026-10-06；整理日期：2026-10-07。

在冻结模型、相机与控制器后，20 个新随机种子场景全部有效，成功 19 个，成功率 **95%**。这是修复后 ACT 与 RGB-D 校正模块的组合成绩，不是纯 RGB ACT 的成功率。纯 ACT 在此前五个固定场景中仍为 0/5，视觉校正 v2 在这五个开发场景中为 4/5；20 个新场景没有边测试边调参。

## 实验条件和结果

| 项目 | 条件 / 结果 |
| --- | --- |
| 任务与机器人 | `stack_blocks_two`，`aloha_agilex`，joint 动作 |
| 训练数据 | 50 条演示，固定 40 train / 10 validation |
| 训练 | 从新 ACT 权重开始，预训练 ResNet18，2000 epoch，80000 更新，batch 1，seed 0 |
| 修复项 | 使用最终 decoder 层；有效 target loss 归一化；夹爪权重 4；关键阶段采样比例 0.5 |
| 相机 | 腕部偏移 `[-0.14, 0, 0.22]`，RPY `[0, 55, 0]` 度，采集/部署一致 |
| 控制 | chunk 50，temporal aggregation 关闭；视觉校正后清空缓存并重新预测 |
| 新场景 | 种子 700000 至 2600000，步长 100000，每场景上限 800 步 |
| 官方成功 | 19/20；方块相对放置容差满足且双夹爪打开 |
| 模式覆盖 | LL 1/1，LR 7/7，RL 9/10，RR 2/2，覆盖不均衡 |
| 抓取 XY 误差 | 38 次记录，中位数 2.18 mm，最大 4.33 mm（评分使用真实位置） |

20 个场景样本仍有限。未额外测试释放后长时间稳定性、真实相机、不同颜色/尺寸/物体、背景变化、标定误差和深度噪声。

## RGB-D 校正做了什么

通过头部与双腕 RGB、深度和相机标定，用已知红/绿颜色及 5 cm 方块尺寸估计三维中心。接触前先对齐 XY 再下降，TCP 到目标距离小于 6 mm 才闭合；闭合后保持 5 个动作步并重新预测。松开绿块前对齐红块上方，XY 和 Z 误差均小于 8 mm 才松开。

校正器读取机器人实际关节状态，通过运动学求解修正关节命令。方块 actor 真值用于测试记录和官方评分，不进入 `visual_guard.py` 的控制决策。测试脚本还保留可选的历史干预诊断功能，本轮使用默认 `--fine=-1`，未启用该干预。

唯一失败为种子 2600000：红块始终可见，但 TCP 最低仍高于方块中心约 16.7 cm，未进入 12 cm 的校正触发区，最终 800 步超时。停滞检测和安全接近恢复尚未实现，ACT 高位停滞的原因未隔离。详见 [冻结测试报告](frozen-test20-report.md)。

## 文件与使用方式

| 文件 | 用途 |
| --- | --- |
| `robotwin-workspace.patch` | 相对上游基线的完整 RoboTwin 修改，含腕部安装配置、渲染设置、采集配置和验证脚本 |
| `xpolicylab-act-repaired.patch` | 完整 ACT 修复和 20 项测试，含 `losses.py`、decoder 层选择与部署配置验证 |
| `training-and-controller.patch` | 历史训练入口、关键阶段采样表、固定 split、评测配置、纯 ACT 对照、冻结 RGB-D 控制器与测试器 |
| `demo_train50_wrist_v2.yml` | 可直接查看的采集/相机配置 |
| `evidence.json` | 逐场景结果、分析、冻结 manifest、采集来源、训练配置和 checkpoint 验证 |
| `test20-results.csv` | 20 个场景的精简指标，包含校正步数 |
| `artifact-manifest.json` | 公开文件 SHA-256 与上游版本；原始测试代码校验值另存于证据内 |

基线：RoboTwin `30954692d06ba7e89f7a6b76064f4062c488fa81`；XPolicyLab `a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5`。

主代码补丁是完整快照，已包含前两轮修改，请从干净基线应用，勿与旧补丁重复叠加。

```bash
git -C "$ROBOTWIN_ROOT" apply --check /path/to/robotwin-workspace.patch
git -C "$ROBOTWIN_ROOT" apply /path/to/robotwin-workspace.patch
git -C "$ROBOTWIN_ROOT/XPolicyLab" apply --check /path/to/xpolicylab-act-repaired.patch
git -C "$ROBOTWIN_ROOT/XPolicyLab" apply /path/to/xpolicylab-act-repaired.patch
git -C "$ROBOTWIN_ROOT" apply --check /path/to/training-and-controller.patch
git -C "$ROBOTWIN_ROOT" apply /path/to/training-and-controller.patch
cd "$ROBOTWIN_ROOT"
python -m unittest discover -s XPolicyLab/policy/ACT/tests -v
```

训练与测试脚本是历史接口快照，依赖 RoboTwin 仿真资源、CUDA 环境、采集数据和对应 checkpoint。机器绝对路径已改成 `${ROBOTWIN_ROOT}` / `${USER_HOME}` 占位符；Python、JSON、YAML 中的占位符需手动替换后使用，不会自动展开。测试器 `run_twenty.py` 校验原始冻结文件哈希，替换路径后的副本需要重新生成自己的 manifest 并保留原始 manifest 为历史证据。不能用修改后的公开文件哈希冒充原始测试哈希。

复现单个场景的入口为补丁恢复出的 `visual_guard_test20_20261006_231054/simulate.py --seed 700000 --steps 800`；批量入口为同目录 `run_twenty.py`。脚本生成视频、轨迹和截图，已有输出使用排他打开，运行前选择新输出目录。当前没有公开数据与权重下载地址，因此这是代码和结果归档，尚非可下载后一键重跑的完整包。

## 本次验证和后续

2026-10-07 运行现有 ACT 测试，20/20 通过。三份补丁通过锁定基线的应用检查；冻结测试四个文件的原始 SHA-256 与 manifest 一致；20 个有效场景和 19 个成功的统计重新核对。本次未重新训练或运行仿真。

阶段目标已达成：训练、部署、诊断和已知方块的高成功率组合方案。后续研究可分别评估纯 ACT 改进、不同输入条件的公平对照，以及停滞/掉落恢复和长期稳定性。
