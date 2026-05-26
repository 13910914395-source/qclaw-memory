# UTM olib 安装进度记录 2026-04-28

## 目标
在 UTM Windows 11 ARM64 VM 中安装 olib（0-lib），最终实现本地量化数据订阅。

## 当前状态

### ✅ 已完成
1. **config.plist 清理**：Drive 从 4 减至 2（系统盘 + Win11 ISO），多余 olib-tiny.iso 驱动已移除
2. **WebDAV 共享配置**：共享目录已设为 `~/Library/Containers/com.utmapp.UTM/Shared`
3. **安装包已放置**：Shared 目录包含 install-olib.bat、install-olib.ps1、README.txt、autorun.inf

### ⚠️ 阻断问题
1. **utmctl exec/file 需要 GUI 会话**：在 exec 环境里调用 utmctl exec 或 file push 时超时/阻塞，无法在自动化脚本中直接使用
2. **utmctl status 显示 started 但无 QEMULauncher 进程**：VM 状态存疑（GuestAgent 报告 vs 实际进程）
3. **截图方案均失败**：AppleScript（display 不匹配）、pyautogui（安装受阻）、spicy（Unix socket URI 解析错误）、socat+SPICE（超时）
4. **SPICE Unix socket URI 格式问题**：spicy-screenshot 无法解析 `unixsock=` 参数，期望 `spice://` scheme

### 🔑 关键发现
- **utmctl exec** 和 **utmctl file push** 是最直接的 VM 命令执行方案，但需要 GUI 用户会话才能工作
- UTM 的 QMP/QEMU monitor socket 不存在（只有 SPICE socket 和 swtpm socket）
- VM IP: 192.168.0.33（via utmctl ip-address），可能有远程接入方式

## 下一步行动
1. **用户手动**：在 Mac 桌面上点击 UTM 窗口中的"开始"按钮启动 VM
2. **VM 启动后**：通过 WebDAV 网络共享访问 Shared 目录，运行 install-olib.bat
3. **备选**：用户手动在 VM 内执行 PowerShell 命令 `irm https://ghproxy.com/.../install.ps1|iex`

## 文件路径
- VM 配置：`~/Library/Containers/com.utmapp.UTM/Data/Documents/Windows.utm/config.plist`
- WebDAV 共享：`~/Library/Containers/com.utmapp.UTM/Shared/`
- SPICE socket：`~/Library/Group Containers/WDNLXAD4W8.com.utmapp.UTM/B0987A5E-16C1-47F1-B256-C3AA63DC21A4.spice`
