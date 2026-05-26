# MacbookAir 配置指南

## 方法一：直接在 MacbookAir 上检查

请在 MacbookAir 的终端中运行：

```bash
# 1. 检查记忆文件
ls -la ~/.qclaw/workspace/MEMORY.md
ls -la ~/.qclaw/workspace/memory/

# 2. 查看记忆内容
cat ~/.qclaw/workspace/MEMORY.md

# 3. 查看最新日志
cat ~/.qclaw/workspace/memory/2026-05-26.md 2>/dev/null || echo "今日日志不存在"
```

## 方法二：复制检查脚本

**在 Mac mini 上执行：**

```bash
# 复制检查脚本到桌面，方便传输
cp ~/.qclaw/workspace/.scripts/check_macbookair.sh ~/Desktop/
```

**然后在 MacbookAir 上执行：**

```bash
# 方法 2.1: 通过 AirDrop/U盘传输后运行
cd ~/Desktop
bash check_macbookair.sh

# 方法 2.2: 或直接在 MacbookAir 的 OpenClaw 中运行检查命令
ls -la ~/.qclaw/workspace/memory/
```

## 方法三：通过 OpenClaw Web UI（推荐）

在 MacbookAir 上：

1. 打开浏览器访问 OpenClaw Web UI
2. 在对话中发送：`"检查我的记忆状态"`
3. AI 会自动检查并报告

## 配置 Git 同步

### 步骤 1: 创建共享仓库

**选项 A: GitHub 私有仓库**
```bash
# 在 GitHub 创建新的私有仓库: qclaw-memory-sync
# 然后在两台设备上分别执行：

# Mac mini
cd ~/.qclaw/workspace
git remote add origin https://github.com/YOUR_USERNAME/qclaw-memory-sync.git
git push -u origin main

# MacbookAir
cd ~/.qclaw/workspace
git remote add origin https://github.com/YOUR_USERNAME/qclaw-memory-sync.git
git pull origin main --allow-unrelated-histories
```

**选项 B: Gitee 私有仓库（国内访问更快）**
```bash
# 在 Gitee 创建私有仓库
# 配置同上，只是 URL 改为 gitee.com
```

**选项 C: 本地 Git 服务器**
```bash
# 如果两台设备在同一局域网
# 在 Mac mini 上设置 Git 服务器：

cd ~/.qclaw/workspace
git clone --bare . ../qclaw-memory.git
cd ../qclaw-memory.git
git daemon --base-path=. --enable=receive-pack --export-all

# 在 MacbookAir 上：
cd ~/.qclaw/workspace
git remote add origin git://MAC_MINI_IP/qclaw-memory.git
```

### 步骤 2: 配置自动同步

**在 MacbookAir 上创建同步脚本：**
```bash
mkdir -p ~/.qclaw/workspace/.scripts
cat > ~/.qclaw/workspace/.scripts/sync_workspace.sh << 'EOF'
#!/bin/bash
cd ~/.qclaw/workspace
git add -A
git commit -m "Sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
git pull --rebase origin main 2>/dev/null
git push origin main 2>/dev/null
EOF
chmod +x ~/.qclaw/workspace/.scripts/sync_workspace.sh
```

## 快速同步方案（立即可用）

如果暂时不想配置 Git 远程仓库，可以使用以下临时方案：

### 方案 1: 手动文件传输
```bash
# 在源设备上打包
cd ~/.qclaw/workspace
tar -czf ~/Desktop/qclaw_memory_backup.tar.gz MEMORY.md memory/

# 通过 AirDrop/U盘传输到目标设备

# 在目标设备上解压
cd ~/.qclaw/workspace
tar -xzf ~/Desktop/qclaw_memory_backup.tar.gz
```

### 方案 2: iCloud 同步（需要移动目录）
```bash
# 将 workspace 移动到 iCloud
mv ~/.qclaw/workspace ~/Library/Mobile\ Documents/com~apple~CloudDocs/QClaw/workspace

# 创建符号链接
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/QClaw/workspace ~/.qclaw/workspace
```

---

## 需要的信息

请告诉我：

1. **MacbookAir 的记忆状态** - 运行检查脚本后的输出
2. **选择哪种同步方案** - Git 远程仓库 / iCloud / 手动传输
3. **是否需要自动同步** - 配置定时任务

---

**等待您的反馈：**
- Mac mini 已准备好同步机制
- 需要 MacbookAir 的记忆状态确认
- 可以开始配置双向同步
