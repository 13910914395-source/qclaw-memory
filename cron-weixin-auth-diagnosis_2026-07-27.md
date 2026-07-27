# Cron 任务失败诊断与修复 — 2026-07-27

## 问题现象
用户收到 cron 失败通知（心学问诊·知行合一，jobId `ba4822ca`），判定「微信通道不通」。
错误：`No API key found for provider "qclaw". Auth store: .../openclaw-agent.sqlite`

## 诊断过程
1. **排除微信通道**：`openclaw-weixin` 通道本身是通的——认知推送（早/午/晚）、美股行情早报同样走该通道且 `delivered` 成功。
2. **对比成功/失败任务配置**：
   - 失败任务 payload **缺 `model` 字段** → isolated session 回退默认 provider 解析 `qclaw`，去 auth store 找 API key（缺失）→ 必败
   - 成功任务（认知推送等）payload 显式带 `"model": "qclaw/modelroute"` → 走 Gateway 托管认证路径 → 正常
3. **时间线（关键）**：
   - 08:48 一批任务全 auth error
   - 08:55 `gateway-supervisor-restart-handoff.json` 记录一次 **Gateway 重启**
   - 09:46 认知推送午间 ok（认证已恢复）
   - 结论：今早 Gateway 重启导致 LLM 认证短暂丢失（瞬时故障），叠加部分任务缺 model 配置致认证解析路径失败。
4. **异常点排查**：认知推送_晚间（有 model）今早也 error，但手动重跑已 ok → 印证是重启窗口的瞬时认证丢失，非配置问题。

## 修复动作
给全部 9 个缺 `model` 的 agentTurn 任务补上 `model: qclaw/modelroute`（与成功任务对齐）：
- a1fcec76 心灵警句_午间_微信
- ba4822ca 心学问诊·知行合一（已验证 ok+delivered）
- e6362dfb workspace_memory_sync
- c0df7055 心学夜思·致良知（原本 ok，防御性补齐）
- 8282a06a 心灵警句_晚间_微信
- bdf4b27b 海南勘察招标日报
- 7bc7b935 海口天气新闻早报_微信
- 42d25f8c 心灵警句_早间_微信
- ab02bbc1 心学晨读·核心概念

命令：`openclaw cron edit <id> --model qclaw/modelroute`

## 验证结果
- 手动 run 心学问诊 `ba4822ca`：lastRunStatus=ok，lastDeliveryStatus=delivered ✅
- 手动 run 认知推送_晚间 `efaa56b8`：lastRunStatus=ok，lastDeliveryStatus=delivered ✅

## 结论
- **微信通道是通的**，用户收到的两条测试推送即为证明。
- 真正故障 = 今早 Gateway 重启致 LLM 认证短暂丢失 + 部分 cron 任务缺 `model` 配置。
- 后续 cron 自动触发（如心学问诊 12:00、心灵警句 08:00）应恢复正常。

## 经验沉淀（供下次参考）
- isolated cron 的 `agentTurn` payload **必须**显式设 `"model": "qclaw/modelroute"`，否则走 auth store 解析 qclaw key 必失败。
- cron error 不一定是通道问题，先看 `lastErrorReason`（此处为 `auth`）与成功任务的 model 字段差异。
- Gateway 重启窗口（见 gateway-supervisor-restart-handoff.json）内运行的 cron 任务会出现瞬时 auth error，重启恢复后自愈；可手动 `cron run` 验证。
