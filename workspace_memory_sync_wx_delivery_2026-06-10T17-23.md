# 记忆同步微信推送修复 — 2026-06-10 17:23

## 问题
`workspace_memory_sync` 定时任务（每天 8:00/12:00/18:00/22:00）执行记忆同步后只写文件报告，未推送微信。

## 原因
该任务 delivery 配置为 `mode: "none"`，缺少渠道配置。

## 修复
更新 delivery 为 announce 模式，推送到微信：
- channel: openclaw-weixin
- to: o9cq800Ypi64bHjWcrycgDOZZycg@im.wechat
- accountId: 728fb9503382-im-bot
- bestEffort: false（确保送达）

与心灵警句、心学、天气早报等任务使用相同的微信推送配置。
