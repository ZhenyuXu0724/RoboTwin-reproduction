# Upstream Patches

这里保存尚未合入上游、但复现实验需要的最小修改。

从锁定的 RoboTwin commit 开始，在 RoboTwin 根目录运行：

```bash
git apply /path/to/RoboTwin-reproduction/patches/0001-configurable-ray-tracing-denoiser.patch
```

应用后用 `git diff --check` 检查补丁，并在实验记录中注明是否设置了 `ROBOTWIN_RAY_TRACING_DENOISER`。

