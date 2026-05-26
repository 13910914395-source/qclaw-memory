#!/bin/bash
# QClaw Workspace 同步脚本
# 用于在多台设备间同步记忆和工作空间

WORKSPACE="$HOME/.qclaw/workspace"
LOG_FILE="$WORKSPACE/.sync.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# 检查是否在 workspace 目录
cd "$WORKSPACE" || {
    log "❌ 无法进入 workspace 目录"
    exit 1
}

# Git 同步函数
sync_git() {
    log "🔄 开始 Git 同步..."
    
    # 检查是否有远程仓库
    if ! git remote | grep -q "origin"; then
        log "⚠️  未配置远程仓库，跳过 push/pull"
        log "   请运行: git remote add origin <repo-url>"
        return 1
    fi
    
    # 拉取远程更新
    log "📥 拉取远程更新..."
    git pull --rebase origin main 2>&1 | while read line; do log "   $line"; done
    
    # 添加所有更改
    log "📦 添加本地更改..."
    git add -A
    
    # 检查是否有更改
    if git diff --staged --quiet; then
        log "✅ 无本地更改需要提交"
    else
        # 提交更改
        log "💾 提交更改..."
        git commit -m "Sync: $(date '+%Y-%m-%d %H:%M')" 2>&1 | while read line; do log "   $line"; done
        
        # 推送到远程
        log "📤 推送到远程..."
        git push origin main 2>&1 | while read line; do log "   $line"; done
    fi
    
    log "✅ Git 同步完成"
}

# 仅本地提交（无远程仓库时）
local_commit() {
    log "🔄 检查本地更改..."
    cd "$WORKSPACE"
    
    git add -A
    
    if git diff --staged --quiet; then
        log "✅ 无更改需要提交"
    else
        git commit -m "Local: $(date '+%Y-%m-%d %H:%M')" 2>&1 | while read line; do log "   $line"; done
        log "✅ 本地提交完成"
    fi
}

# 主逻辑
case "$1" in
    "pull")
        cd "$WORKSPACE"
        if git remote | grep -q "origin"; then
            git pull --rebase origin main
            log "✅ 拉取完成"
        else
            log "⚠️  无远程仓库"
        fi
        ;;
    "push")
        sync_git
        ;;
    "local")
        local_commit
        ;;
    *)
        # 默认：尝试完整同步，失败则本地提交
        if git remote | grep -q "origin"; then
            sync_git
        else
            log "⚠️  未配置远程仓库，仅执行本地提交"
            local_commit
        fi
        ;;
esac
