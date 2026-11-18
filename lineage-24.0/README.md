# Galaxy Tab S9 Ultra Wi-Fi — LineageOS 24

本目录保存 SM-X910 / gts9uwifi 当前修改的固定版本清单及补丁。
设备树、内核、Samsung hardware 和 vendor 对应组织仓库的 `lineage-24.0` 分支。
Settings、frameworks/base 和 frameworks/av 的修改已包含在各自组织仓库中，不需要打补丁。其余 10 个尚无独立仓库的上游项目，通过本目录补丁恢复。

在新的空目录同步：

```bash
repo init -u https://github.com/zc4777-gts9u/manifest.git -b lineage-24.0 -m lineage-24.0/manifest.xml
repo sync -c -j8
python3 .repo/manifests/lineage-24.0/apply-patches.py "$PWD" --check
python3 .repo/manifests/lineage-24.0/apply-patches.py "$PWD"
```

手动构建：

```bash
source build/envsetup.sh
lunch lineage_gts9uwifi-cp2a-eng
set -o pipefail
mka bacon -j12 2>&1 | tee -a build-gts9uwifi-eng.log
```

`manifest.xml` 固定各仓库提交；`sources.json` 记录补丁基线与 SHA-256。
`patches/` 同时保留设备等项目本次修改的备份；应用脚本只处理同步后仍需要应用的上游项目。
这些提交包含尚待刷入验证的人脸录入暂停恢复、录入提示和所有设置入口的构建号签名后缀等修改；本次上传没有重新构建刷机包。
APNHLOS 不打包，设备需自行准备兼容的 CYG1 固件底包。

三个内核仓库的 lineage-24.0 分支使用完整源码快照提交，内容与本地源码树一致；原浅克隆基线记录在 sources.json 中。

Android 版本、关于设备及 API 页面统一显示构建 ID 和实际签名标签（例如 CP2A.260605.016 test-keys）。

2026-11-17 更新：修复 Samsung 户外状态读取导致的显示服务崩溃、HAL 重启后的重新连接及空校准值导致的系统软重启；隐藏不支持的影院模式并保护颜色列表；修复 Settings 构建号工具缺失导入。
户外开关的崩溃已修复；当前面板在 AUTO/UI、非 HBM 条件下缺少户外调校表，本次没有补齐该表。

2026-11-18 更新包含 AudioFlinger 到三星音频 HAL 的逐输出音量参考传递，使用 CYG1 原厂 Dolby 调音及原厂启停过渡。设备树增加一次性构建清理，移除会优先加载的旧通用 7.1 HAL。音频框架与 vendor 需要配套构建刷入。
