# 环境记录

## 上游安装

以 RoboTwin 官方安装文档为准，并确保检出 [`upstream.lock.yml`](../upstream.lock.yml) 中锁定的提交。XPolicyLab 是 RoboTwin 的 Git submodule，需要一并初始化。

RoboTwin 当前依赖基线包括：

- `torch==2.4.1`
- `numpy==1.26.4`
- `sapien==3.0.0b1`
- `gymnasium==0.29.1`
- `open3d==0.18.0`

完整依赖仍由对应 RoboTwin commit 中的 `scripts/requirements.txt` 和 XPolicyLab ACT 环境文件定义，避免在这里维护第二份容易漂移的依赖清单。

## 当前主机探测结果

记录日期：2026-09-30。

- 内核：Linux `7.0.0-31-generic`，x86_64
- 当前非训练 shell 中没有可用的 `python` 命令
- 当前 shell 无法通过 `nvidia-smi` 与 NVIDIA 驱动通信

这不代表此前训练环境缺失；正式复现时应进入实际使用的 Conda/容器环境后补齐下表。

| 项目 | 值 |
| --- | --- |
| GPU | 待记录 |
| NVIDIA Driver | 待记录 |
| CUDA Runtime | 待记录 |
| Python | 待记录 |
| Conda/容器名称 | 待记录 |
| Torch CUDA | 待记录 |

## 每次实验需保存

```bash
python --version
nvidia-smi
python -m pip freeze
git -C /path/to/RoboTwin rev-parse HEAD
git -C /path/to/RoboTwin/XPolicyLab rev-parse HEAD
```

`pip freeze` 通常作为实验附件保存；只有确认不包含本地路径或凭据后才提交。

