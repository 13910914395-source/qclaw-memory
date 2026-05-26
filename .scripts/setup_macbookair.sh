#!/bin/bash
# MacbookAir 同步配置脚本
# 在 MacbookAir 终端中运行

set -e

echo "========================================="
echo "MacbookAir 记忆同步配置"
echo "========================================="

WORKSPACE="$HOME/.qclaw/workspace"
REPO="git@github.com:13910914395-source/qclaw-memory.git"

# 1. 检查 SSH 密钥
echo ""
echo "1️⃣  检查 SSH 密钥..."
if [ ! -f ~/.ssh/id_ed25519.pub ]; then
    echo "生成 SSH 密钥..."
    ssh-keygen -t ed25519 -C "qclaw-sync-mba" -f ~/.ssh/id_ed25519 -N ""
    echo ""
    echo "⚠️  请将以下公钥添加到 GitHub："
    echo "   https://github.com/settings/keys"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "添加完成后按回车继续..."
    read -r
else
    echo "✅ SSH 密钥已存在"
fi

# 添加 GitHub 到 known_hosts
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null

# 2. 备份现有记忆
echo ""
echo "2️⃣  备份现有记忆..."
BACKUP_DIR="$HOME/.qclaw/workspace_backup_$(date +%Y%m%d_%H%M%S)"
if [ -d "$WORKSPACE" ] && [ "$(ls -A "$WORKSPACE" 2>/dev/null)" ]; then
    mkdir -p "$BACKUP_DIR"
    cp -r "$WORKSPACE"/* "$BACKUP_DIR/" 2>/dev/null || true
    echo "✅ 已备份到: $BACKUP_DIR"
else
    echo "ℹ️  无需备份（workspace 为空或不存在）"
fi

# 3. 配置 Git
echo ""
echo "3️⃣  配置 Git..."
cd "$WORKSPACE"

if [ ! -d ".git" ]; then
    git init
    git branch -M main
    echo "✅ Git 已初始化"
else
    echo "✅ Git 已存在"
fi

# 4. 配置远程仓库
echo ""
echo "4️⃣  配置远程仓库..."
REMOTE_EXISTS=$(git remote | grep -c "origin" 2>/dev/null || echo "0")
if [ "$REMOTE_EXISTS" -gt 0 ]; then
    git remote set-url origin "$REPO"
else
    git remote add origin "$REPO"
fi
echo "✅ 远程仓库已配置: $REPO"

# 5. 拉取 Mac mini 的记忆
echo ""
echo "5️⃣  拉取 Mac mini 的记忆..."
git fetch origin main 2>&1

# 检查本地是否有需要保留的内容
LOCAL_CHANGES=$(git status --short 2>/dev/null | wc -l)

if [ "$LOCAL_CHANGES" -gt 0 ] || [ "$(git log --oneline 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "⚠️  本地有内容，执行合并..."
    git add -A
    git commit -m "MacbookAir: 本地内容合并前保存" 2>/dev/null || true
    git pull origin main --allow-unrelated-histories --no-edit 2>&1 || {
        echo "⚠️  合并有冲突，请手动解决后运行："
        echo "   cd $WORKSPACE && git add . && git commit -m 'Merge' && git push origin main"
        exit 1
    }
else
    echo "本地无历史，直接拉取..."
    git reset origin/main 2>/dev/null || true
    git checkout -- . 2>/dev/null || true
fi

echo ""
echo "6️⃣  推送 MacbookAir 内容..."
git add -A
git commit -m "MacbookAir: 加入同步 $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git push -u origin main 2>&1

echo ""
echo "========================================="
echo "✅ MacbookAir 同步配置完成！"
echo "========================================="
echo ""
echo "📋 现在两台设备已通过 GitHub 私有仓库同步"
echo "   仓库地址: https://github.com/13910914395-source/qclaw-memory"
echo ""
echo "🔄 日常同步命令："
echo "   cd ~/.qclaw/workspace"
echo "   git add . && git commit -m 'Sync' && git pull --rebase && git push"
echo ""
