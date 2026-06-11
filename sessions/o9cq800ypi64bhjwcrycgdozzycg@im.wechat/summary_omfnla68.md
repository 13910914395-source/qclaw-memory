## 任务背景
用户反馈Gateway重启后cron任务虽执行但未收到微信推送，需要排查修复并新建每日认知推送任务。
## 执行过程
1. 测试直接推送确认微信通道正常
2. 手动触发cron任务确认delivered=true但用户未收到
3. 排查发现cron任务缺少accountId导致推送未送达微信
4. 为已有和新任务补上account参数
5. 创建三条认知推送任务
## 关键结果
- 排查出cron delivery问题：isolated session的announce推送缺少accountId
- 新建三条认知推送任务（07:30/12:30/19:00），覆盖海外贸易、心理学、谈判策略等主题
- 完成任务accountId补全配置
## 结论建议
建议手动触发午间任务验证修复效果，若仍失败需深入排查cron-delivery-guard插件逻辑。