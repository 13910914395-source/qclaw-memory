## 任务背景
用户排查OpenClaw定时任务WebSocket推送失败问题，同时询问Mac mini上定时任务内容的远程访问方案。

## 执行过程
1. 诊断确认：A股价值股任务已修复delivery配置（加--to FuFa）；其他10个任务推送失败，原因是WebSocket连接超时（Reply ack timeout）或断开（code 1006）
2. 验证：用户确认MacBookAir客户端一直开着，桌面端占用WebSocket导致手机端收不到
3. 修复：将全部11个cron任务的reply_timeout从30秒加大到120秒，测试触发早安鸡汤任务
4. 用户询问能否从Mac mini获取定时任务内容，发现当前无SSH密钥、无法远程访问Mac mini
5. 告知用户需要在Mac mini旁时开启SSH并提供IP地址

## 关键结果
- 修复A股价值股任务delivery target缺失问题
- 全部11个cron任务超时已加大至120秒
- 诊断结论：MacBookAir桌面端WebSocket占用导致手机端推送失败
- 确认当前无法远程访问Mac mini，需用户在旁时配置SSH

## 结论建议
cron任务超时加大后待用户确认手机端是否收到测试推送。如仍失败可考虑让cron任务写入文件再由主会话转发。Mac mini远程访问需用户在旁时开启SSH。