# 任务记录：网站截图并发送邮件

**时间**: 2026-06-05 14:59 - 15:06 (GMT+8)  
**任务类型**: 浏览器自动化 + 邮件发送

## 任务目标
在隔离浏览器中打开 https://qclaw.qq.com，截图后通过邮件发送。

## 执行步骤

### 1. 浏览器自动化（xbrowser 技能）
- ✅ 初始化 xbrowser 环境：`xb init` 成功
- ✅ 处理浏览器冲突：检测到 Chrome 正在运行，用户选择强制关闭
- ✅ 打开网站：`open 'https://qclaw.qq.com'` 成功
- ✅ 截图：`screenshot --full` 保存到 `/Users/fasimac/.agent-browser/tmp/screenshots/screenshot-1780643031980.png`

### 2. 邮件发送（imap-smtp-email 技能）
- ✅ 获取邮箱凭证：`get-token.sh` 成功，使用 2880914@qq.com (QQ邮箱)
- ⚠️ 依赖安装：初次执行时发现缺少 `nodemailer` 模块，执行 `npm install` 安装依赖
- ⚠️ 文件路径问题：邮件脚本有目录访问限制（`ALLOWED_READ_DIRS`），不允许从工作区或技能目录读取附件
- ✅ 解决路径问题：将截图复制到允许的目录 `/Users/fasimac/Downloads/qclaw-screenshot.png`
- ✅ 发送邮件：使用 `email_gateway.sh send` 成功发送带附件的邮件

## 关键发现

### xbrowser 技能要点
1. 必须先用 `xb init` 初始化环境
2. Chrome 运行时需要先关闭才能操作
3. 截图默认保存到 `~/.agent-browser/tmp/screenshots/`

### imap-smtp-email 技能要点
1. **强制首步**：必须先执行 `get-token.sh` 获取凭证
2. **目录限制**：`.env` 中的 `ALLOWED_READ_DIRS` 限制附件读取路径
   - 当前配置：`/Users/fasimac/Downloads,/Users/fasimac/Documents`
   - 附件必须放在这些目录下才能发送
3. **正确使用方式**：使用 `email_gateway.sh` 脚本，不要直接调用 `resolve-account.cjs`
4. **依赖管理**：首次使用需要 `npm install` 安装依赖（nodemailer 等）

## 最终结果
- **邮件发送成功**
  - Message ID: `<ab09f731-69f9-aa39-616c-0e8b5d011698@qq.com>`
  - 收件人: 2880914@qq.com
  - 主题: qclaw.qq.com 网站截图
  - 附件: qclaw-screenshot.png

## 临时文件位置
- 原始截图：`/Users/fasimac/.agent-browser/tmp/screenshots/screenshot-1780643031980.png`
- 工作区副本：`/Users/fasimac/.qclaw/workspace/qclaw-screenshot.png`
- 技能目录副本：`/Users/fasimac/.qclaw/skills/imap-smtp-email/qclaw-screenshot.png`
- 最终使用的文件：`/Users/fasimac/Downloads/qclaw-screenshot.png`

## 经验教训
1. 使用 imap-smtp-email 发送附件时，必须先将文件放到 `ALLOWED_READ_DIRS` 指定的目录
2. xbrowser 和 imap-smtp-email 技能可以很好地配合使用
3. 邮件发送前务必先执行 `get-token.sh` 刷新凭证
