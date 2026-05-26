# Mac Mini 自动登录 + AI Agent 自启动配置

## 目标
配置 Mac mini 重启后自动启动 AI Agent（OpenClaw），无需手动登录操作。

## 环境信息
- macOS 26.5 (Tahoe), Apple Silicon
- FileVault: **已开启**（全盘加密）
- 用户: fasimac
- QClaw 已在登录项中 ✅

## 配置结果

### ✅ 已完成
1. QClaw 已在 macOS 登录项中 → 登录后自动启动
2. OpenClaw Gateway 随 QClaw 自动启动
3. 创建安全重启脚本: `~/.qclaw/workspace/qclaw-restart.sh`

### ⚠️ 需要用户手动操作
- **开启 macOS 自动登录**: 系统设置 → 用户与群组 → 自动登录 → 选择 fasimac
- FileVault 开启时，开机仍需在 FileVault 解锁屏输入一次密码

## 重启流程

### 普通重启
```
开机 → FileVault解锁屏(输密码) → 自动进桌面 → QClaw自启 → AI Agent就绪
```

### 使用安全重启脚本（推荐）
```bash
sudo bash ~/.qclaw/workspace/qclaw-restart.sh
```
```
执行脚本 → FileVault自动解锁 → 自动进桌面 → QClaw自启 → AI Agent就绪
```

## FileVault 限制
- FileVault 开启状态下，无法实现完全无密码开机
- 意外重启（断电等）后，必须手动输入 FileVault 密码
- 只有通过 `fdesetup authrestart` 的计划重启才能跳过密码输入

## 参考
- `fdesetup authrestart` - 将 FileVault 密码临时注入 EFI，仅对下一次重启有效
- macOS 自动登录设置: 系统设置 → 用户与群组 → 自动登录
