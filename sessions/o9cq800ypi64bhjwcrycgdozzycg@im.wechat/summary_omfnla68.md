## 任务背景
用户排查OpenClaw定时任务无法接收的根本原因：Gateway服务旧版导致密钥未正确注入isolated分身进程。

## 执行过程
1. 诊断auth库为空、Gateway版本旧
2. doctor --repair未修复认证库
3. launchctl重启Gateway成功注入密钥
4. 补发今日三个失败任务
5. 手动补送心学晨读内容至微信

## 关键结果
- 根因: Gateway为旧版(2026.4.21)，托管密钥未注入isolated分身
- 修复: launchctl unload/load后新Gateway(PID 14999)正常工作
- 心学晨读/认知推送早间均已手动补发并微信送达
- 晚间任务预计正常执行

## 结论建议
修复已完成，明天早间任务应由新Gateway正常调度。如复发可通过launchctl重载Gateway或QClaw桌面端重启服务。