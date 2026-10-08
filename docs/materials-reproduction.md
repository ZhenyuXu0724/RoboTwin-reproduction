# RoboTwin 材料恢复与复现入口

公开仓库保存材料与代码快照，运行工作区是另一个检出到锁定版本的 RoboTwin 仓库。恢复工具将旧材料中的机器路径占位符替换为所指定工作区，并应用全部依赖补丁。不要把本仓库的目录误当成 RoboTwin 工作区。

## 检查公开材料

只需 Python 标准库，不需要 GPU、Torch 或下载数据：

```bash
python scripts/verify_materials.py
```

检查公开文件 SHA-256、五组结果计数、20 场种子与初始位置配对、消融动作前缀及 DP 训练 2000 轮记录。校验材料不等于重跑实验。

## 恢复代码

先准备 RoboTwin `30954692d06ba7e89f7a6b76064f4062c488fa81` 和 XPolicyLab `a9ccf8dbc34ad047534a14b7ee0503bddf0e54b5` 的干净检出：

```bash
python scripts/restore_materials.py --root /path/to/RoboTwin --check
python scripts/restore_materials.py --root /path/to/RoboTwin --apply
```

工具在临时副本上依次验证三份历史补丁及本轮 DP 补丁，再应用到指定工作区。历史补丁是完整基线快照，不能叠加在已有修改的工作区。本轮 DP 脚本原样保存；只替换历史依赖补丁里的 `${ROBOTWIN_ROOT}` 和 `${USER_HOME}`。冻结哈希属于历史原文件；本机路径替换后应重新生成自己的运行 manifest，不能声称新文件仍具备旧文件哈希。

## 准备环境和大文件

2026-10-08 从实际 RoboTwin Python 环境读取：Python 3.10.21、Torch 2.7.1+cu128、Torchvision 0.22.1+cu128、NumPy 1.26.4、h5py 3.16.0、SAPIEN 3.0.0b1、OpenCV 4.10.0.84、transforms3d 0.4.2、einops 0.8.1、zarr 2.18.3。这是整理时的环境读数，非锁定容器镜像；基础环境仍参考上游安装说明。

DP 的额外依赖当时安装在 RoboTwin 的 `data/dp_runtime`，脚本会优先加入该目录。对应版本为 diffusers 0.32.2、hydra-core 1.3.2、omegaconf 2.3.0、dill 0.3.8、antlr4-python3-runtime 4.9.3。完整基础依赖准备后，可使用：

```bash
python -m pip install --target "$ROBOTWIN_ROOT/data/dp_runtime" \
  diffusers==0.32.2 hydra-core==1.3.2 omegaconf==2.3.0 dill==0.3.8 antlr4-python3-runtime==4.9.3
```

准备采集/处理数据、ACT 权重和归一化统计、DP `training/2000.pt`；它们没有公开下载地址。路径与 SHA-256 见 [权重登记](../experiments/2026-10-08-policy-comparison/weights-registry.json)，原始数据来源与检查见 [数据审计](../experiments/2026-10-08-policy-comparison/dataset-audit.json)。保留固定划分和历史目录结构。

## 运行入口

在恢复出的 RoboTwin 根目录运行。每次使用新的输出目录；程序对已有结果采用排他写入，避免覆盖证据。

```bash
python scripts/dp_comparison/test_contracts.py
python scripts/dp_comparison/test_guard_initfix.py
python scripts/dp_comparison/test_act_ablation.py
python -m unittest discover -s XPolicyLab/policy/ACT/tests -v

# 单个纯策略场景，网络均只使用 RGB 与关节
python scripts/dp_comparison/evaluate.py --policy DP --seed 2700000 --steps 800 \
  --checkpoint data/dp_compare_20261007/run2000_v2/training/2000.pt --output data/new_dp_case
python scripts/dp_comparison/evaluate.py --policy ACT --seed 2700000 --steps 800 \
  --checkpoint data/dp_compare_20261007/run2000_v2/training/2000.pt --output data/new_act_case

# 同一外部 RGB-D 纠偏器
python scripts/dp_comparison/evaluate_rgbd.py --seed 2700000 --steps 800 \
  --checkpoint data/dp_compare_20261007/run2000_v2/training/2000.pt --output data/new_dp_rgbd_case
python scripts/dp_comparison/evaluate_act_rgbd.py --seed 2700000 --steps 800 --output data/new_act_rgbd_case

# 仅禁用 ACT 的释放分支
python scripts/dp_comparison/evaluate_act_ablation.py --seed 2700000 --steps 800 --output data/new_act_grasp_case
```

ACT 入口由历史 `act_eval_config.yml` 读取其自身权重；纯 ACT 命令中的 DP checkpoint 参数是共享 CLI 的参数，并非 ACT 权重来源。历史脚本中的冻结依赖哈希会检查控制器和串行相机，请先用恢复材料完成这些依赖。

DP 训练入口是 `train.py --output data/new_dp_training --train`；`launch.py --output data/new_dp_experiment` 会启动训练及评测，计算量较大。诊断 `diagnose_dp.py` 和消融协调器使用固定历史目录，适合作为已记录流程的源代码参考；正式新实验应先制定新的输出与场景协议。此次整理没有启动训练或仿真。

## 可重复性边界

补丁恢复、语法与现有测试已经验证；没有在全新 GPU 环境重跑 2000 轮训练和 100 场评测。RoboTwin 资源包与大文件仍需自行准备，GPU/驱动兼容性需在运行主机检查。公开路径替换会改变部分依赖文件指纹，应保留旧 manifest 作为历史证据并为自己的运行建立新指纹。
