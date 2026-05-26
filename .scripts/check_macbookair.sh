#!/bin/bash
# MacbookAir 记忆同步配置脚本
# 请在 MacbookAir 的终端中运行此脚本

echo "========================================="
echo "MacbookAir 记忆同步配置"
echo "========================================="
echo ""

# 1. 检查记忆系统
echo "1️⃣  检查记忆系统..."
WORKSPACE="$HOME/.qclaw/workspace"

if [ -d "$WORKSPACE" ]; then
    echo "✅ Workspace 目录存在"
    
    if [ -f "$WORKSPACE/MEMORY.md" ]; then
        echo "✅ MEMORY.md 存在"
        echo "   最后更新: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$WORKSPACE/MEMORY.md" 2>/dev/null || stat -c "%y" "$WORKSPACE/MEMORY.md" 2>/dev/null | cut -d'.' -f1)"
    else
        echo "⚠️  MEMORY.md 不存在"
    fi
    
    if [ -d "$WORKSPACE/memory" ]; then
        FILE_COUNT=$(ls -1 "$WORKSPACE/memory"/*.md 2>/dev/null | wc -l)
        echo "✅ memory/ 目录存在，包含 $FILE_COUNT 个日志文件"
        
        LATEST=$(ls -t "$WORKSPACE/memory"/*.md 2>/dev/null | head -1)
        if [ -n "$LATEST" ]; then
            echo "   最新日志: $(basename "$LATEST")"
        fi
    else
        echo "⚠️  memory/ 目录不存在"
    fi
else
    echo "❌ Workspace 目录不存在"
    echo "   请确认 OpenClaw 已正确安装"
    exit 1
fi

echo ""
echo "2️⃣  检查 Git 状态..."
cd "$WORKSPACE"

if [ -d ".git" ]; then
    echo "✅ Git 已初始化"
    
    # 检查是否有远程仓库
    REMOTE=$(git remote | grep -c "origin" 2>/dev/null || echo "0")
    if [ "$REMOTE" -gt 0 ]; then
        echo "✅ 已配置远程仓库"
        git remote -v
    else
        echo "⚠️  未配置远程仓库"
    fi
    
    # 检查是否有未提交的更改
    CHANGES=$(git status --short 2>/dev/null | wc -l)
    if [ "$CHANGES" -gt 0 ]; then
        echo "⚠️  有 $CHANGES 个文件未提交"
    else
        echo "✅ 工作目录干净"
    fi
else
    echo "⚠️  Git 未初始化"
    echo ""
    echo "是否初始化 Git 仓库？(y/n)"
    read -r INIT_GIT
    
    if [ "$INIT_GIT" = "y" ]; then
        git init
        echo "✅ Git 已初始化"
    fi
fi

echo ""
echo "3️⃣  记忆内容摘要..."
echo ""

if [ -f "$WORKSPACE/MEMORY.md" ]; then
    echo "--- MEMORY.md 内容预览 ---"
    head -20 "$WORKSPACE/MEMORY.md"
    echo "..."
fi

echo ""
echo "========================================="
echo "配置完成"
echo "========================================="
echo ""
echo "📋 下一步："
echo "1. 如需同步，请配置 Git 远程仓库："
echo "   git remote add origin <仓库URL>"
echo "2. 或使用以下命令手动同步："
echo "   git add ."
echo "   git commit -m 'Sync from MacbookAir'"
echo ""
