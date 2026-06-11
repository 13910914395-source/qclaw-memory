# 认知推送任务创建与 delivery 修复

## 目标
为用户创建每日早中晚三条「今日认知」推送，内容涵盖海外贸易商机、心理学技巧、谈判策略、跨文化商务、经济趋势洞察。

## 关键发现：cron delivery 缺 accountId

- 通过 CLI 创建 cron 任务时，新任务 delivery 中**缺少 accountId 字段**
- 虽然 `channel`、`to`、`mode` 都正确，但缺 accountId 可能导致推送实际不到达
- 旧任务（如天气早报）创建时 accountId 已存在，故正常运行
- **修复方法**：`openclaw cron edit <id> --account <accountId>`

## 最终配置

| 任务 | 时间 | ID |
|------|------|----|
| 认知推送_早间 | 07:30 | c44426ab-...c5db3 |
| 认知推送_午间 | 12:30 | ab77e66b-...9ff065 |
| 认知推送_晚间 | 19:00 | efaa56b8-...0ae827 |

delivery: announce → openclaw-weixin, accountId=728fb9503382-im-bot

## 验证
手动触发测试成功，用户确认收到消息 ✅
