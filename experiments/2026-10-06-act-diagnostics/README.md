# ACT 修改与实验归档（2026-09-30 至 2026-10-05）

整理日期：2026-10-06。本目录保存代码快照和已有实验的轻量证据，不表示在整理当天重新训练或运行仿真。

## 代码与应用方式

| 文件 | 内容 | 应用位置 |
| --- | --- | --- |
| `robotwin-workspace.patch` | 完整渲染降噪开关、采集配置（3/20/50 条）、缓存频率、checkpoint 验证脚本 | RoboTwin 根目录 |
| `xpolicylab-act.patch` | ACT 数据对齐、训练集归一化、固定划分、训练指标与参考输出、权重续训、连续图像布局、14 项回归测试 | XPolicyLab 根目录 |
| `diagnostic-scripts.patch` | 数据审计、离线动作对比、阶段分析、视觉交换、执行 10 步诊断和实验运行脚本 | RoboTwin 根目录 |

基线：RoboTwin `30954692d06ba7e89f7a6b76064f4062c488fa81`；XPolicyLab `a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5`。

这两个主代码补丁是相对基线的完整快照。`robotwin-workspace.patch` 包含仓库旧 `patches/0001-*` 的渲染修改，请从干净基线应用，勿重复叠加。保留现有工作区时先在独立检出中检查。

```bash
git -C "$ROBOTWIN_ROOT" apply --check /path/to/robotwin-workspace.patch
git -C "$ROBOTWIN_ROOT" apply /path/to/robotwin-workspace.patch
git -C "$ROBOTWIN_ROOT/XPolicyLab" apply --check /path/to/xpolicylab-act.patch
git -C "$ROBOTWIN_ROOT/XPolicyLab" apply /path/to/xpolicylab-act.patch
cd "$ROBOTWIN_ROOT"
python -m unittest discover -s XPolicyLab/policy/ACT/tests -v
```

诊断脚本保留实验时的接口与路径组织，属于历史脚本快照，未在本次归档中逐一重跑。公开版本将机器绝对路径替换为 `${ROBOTWIN_ROOT}` / `${USER_HOME}` 占位符；Python 中的字符串需按本机位置替换后使用，这些占位符不会自动展开。脚本可能写入输出目录或启动训练/仿真，运行前检查参数和目的目录。

## 已做修改

- 转换器标记 `action_start_offset=0`，避免已对齐的状态/动作再次偏移；无元数据旧数据保留兼容行为。
- 归一化仅使用训练 episode，训练和验证共享足够的 padding 长度；支持固定 JSON episode 划分。
- 保存训练配置、逐 epoch 指标、优化步数、梯度范数及最终 checkpoint 参考输入/输出；遇到非有限值停止更新。
- 支持从已完成 run 继续加载模型权重到累计目标 epoch，并验证配置、划分和归一化一致；优化器和随机状态重置，不是精确续训。
- 部署图像使用连续布局。历史 smoke 验证中适配器误差约 `4.59e-4`；随后 checkpoint/适配器验证通过。详细报告及哈希见 `training-and-validation.json`。

## 实验与结果

| 尝试 | 已记录结果 | 解释边界 |
| --- | --- | --- |
| 专家 episode 0 回放 | 成功率 1.0 | 单条轨迹的链路检查 |
| 20 条训练数据与累计 4000 epoch 权重续训 | 记录了离线、已见及未见场景比较 | 具体种子与干预见证据文件，勿混为同一测试集 |
| 50 条数据，40 train / 10 validation，2000 → 4000 epoch | 累计更新 80000 → 160000；末 200 epoch validation L1 均值 0.10947 → 0.08268 | 优化器/RNG 在续训时重置 |
| 50 条数据的固定 5 场景，执行 50 步 | 2000/4000 epoch 模型均 0/5 | 场景为 RL×4、LR×1，未衡量同臂场景能力 |
| 相同 4000 epoch 模型，预测 chunk 50、每次执行 10 步 | 相同 5 个种子均未成功 | 单次配对尝试，不支持“缩短执行必然有效” |
| 交换初始图像、保持初始 qpos 一致 | 50 样本的预测差平均约 10.07°；43/50 更接近图像供体动作 | 支持模型使用视觉；不能证明闭环视觉/控制正确 |

当前失败主要发生在抓取和失败后的恢复阶段；降低离线误差没有自动带来任务成功。不能仅凭这些结果认定 RGB 交换、数据损坏、动作维度错误或过拟合是根因。10 步执行的后续结果已归档，早期 review 中“尚未测试”的描述属于当时状态。

## 证据与验证

- `diagnostic-evidence.json`：35 份诊断报告，键为原始工作区相对路径，保留历史报告的时间与限制。
- `training-and-validation.json`：5 个 run 的训练配置、首末指标和 checkpoint 验证报告，含实际 train/validation episode IDs。
- `evaluation-runs.csv`：所有发现的 `_result.txt` 摘要；每行是一个历史运行，重复场景/干预不可相加作为独立测试样本。
- 2026-10-06 重新运行现有 ACT 回归测试：14/14 通过。补丁经过基线应用检查；数据、权重、完整视频和原始训练日志未上传。

下一步可在固定模型和配对场景中比较执行 5/1 步，记录命令、实际 qpos/末端位姿、夹爪、物体和查询边界；用平衡的独立开发场景进一步区分抓取精度和失败恢复问题。
