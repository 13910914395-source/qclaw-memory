# 设备同步配置

## 当前设备信息
- 设备名称: Mac mini (Fa's的Mac mini)
- 系统: Darwin 25.5.0 (arm64)
- Workspace: /Users/fasimac/.qclaw/workspace

## 同步机制

### 方案 1: Git + 远程仓库（推荐）
1. 在 GitHub/Gitee/自建 GitLab 创建私有仓库
2. 在各设备上配置:
   ```bash
   cd ~/.qclaw/workspace
   git remote add origin <repo-url>
   ```
3. 定时任务自动同步（见下方配置）

### 方案 2: Syncthing（P2P 同步）
适合局域网内设备间直接同步，无需云服务

### 方案 3: 云盘同步
- iCloud: 需要移动 workspace 到 iCloud 目录
- 坚果云/百度网盘: 支持 WebDAV，可配置同步

## 定时同步配置

### Mac mini 定时任务
```bash
# 每小时自动同步记忆
0 * * * * /Users/fasimac/.qclaw/workspace/.scripts/sync_workspace.sh local

# 每天 8:00 和 20:00 完整同步（需配置远程仓库）
0 8,20 * * * /Users/fasimac/.qclaw/workspace/.scripts/sync_workspace.sh
```

### MacbookAir 定时任务
（待配置）

## 跨设备任务调用

### 机制说明
两台设备可以通过 cron 任务相互触发：
1. 通过 HTTP 调用对方的 OpenClaw API
2. 通过共享文件系统触发（如 Syncthing）
3. 通过消息队列触发（如 Redis）

### 配置示例
见 `cross_device_tasks.json`
