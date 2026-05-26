## 任务背景
为友商参考华检联公司管理制度，需对文档进行脱敏处理后打包交付。

## 执行过程
1. 编写Python脚本处理docx
2. textutil转换旧doc格式
3. 金额/公司名/百分比脱敏
4. 修复表格内数字替换遗漏
5. 删除PDF文件不保留
6. 增加姓名脱敏（首字母替换）

## 关键结果
- 输出25个docx，无PDF
- 脱敏规则：金额→***、百分比→***、华检联→HJL、邱雪云→QXY、赵晶→ZJ、符发→FF
- /Users/fasimac/.qclaw/workspace/HJL管理制度_脱敏版.zip (185KB)
- /Users/fasimac/.qclaw/workspace/desensitize制度.py

## 结论建议
脱敏版已按要求完成，可直接发送给友商。