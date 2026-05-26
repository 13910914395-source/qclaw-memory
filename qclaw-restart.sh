#!/bin/bash
# QClaw 安全重启脚本
# 使用 fdesetup authrestart，重启后自动解锁 FileVault，无需手动输入密码
# 用法: sudo bash ~/.qclaw/workspace/qclaw-restart.sh

set -euo pipefail

echo "🔄 准备安全重启..."
echo "   重启后 FileVault 将自动解锁，系统自动登录，QClaw 自动启动"
echo ""

# 检查是否支持 authrestart
if fdesetup supportsauthrestart 2>/dev/null; then
    echo "✅ 支持 authrestart，执行安全重启..."
    fdesetup authrestart
else
    echo "⚠️  当前系统不支持 authrestart，执行普通重启..."
    echo "   重启后需要在 FileVault 界面手动输入密码"
    shutdown -r now
fi
