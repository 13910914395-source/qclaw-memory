# 海南勘察招标日报 — 2026-08-28 执行记录

## 任务目标
抓取 cebpubservice.com 与 ccgp-hainan.gov.cn 近24小时（2026-08-27 03:00 ~ 2026-08-28 03:00）含
「勘察/检测/测绘/岩土/地质灾害」关键词的公告，生成 PDF 日报 + 钉钉卡片。

## 实际结果：近24h 未检索到符合条件的海南省公告（可自动化检索范围内）
未编造任何数据；如实标注数据访问受限。

## 关键发现
1. **ccgp-hainan.gov.cn（海南省政府采购网）**：前端为 Vue SPA + 网关 OAuth。
   - 公告列表接口 `/rest/web/v2/info/selectInfoForIndex` 匿名请求返回 HTTP 302 → /gp-auth-center/oauth/authorize（登录页）。
   - 仅 `/rest/v2/public/cmSeriousInfo`（失信曝光台）可匿名访问，非采购公告列表。
   - → 无法匿名获取海南省公告列表。
2. **cebpubservice.com（中国招标投标公共服务平台）**：
   - 可抓取入口为 asiancms = 亚行贷款(ADB)项目专用系统，非海南省属项目。
   - 对该系统近24h窗口做关键词检索：51 条关键词命中全部为 2020–2026 历史记录，最新为 2026-08-14，0 条落在近24h，0 条含“海南”。
   - 全国综合搜索 `queryMsglist.do` 依赖服务端会话态提交（含验证码/会话），无法直接以 HTTP 复现筛选。
3. 浏览器工具因 SSRF 策略禁止按域名导航（仅允许 IP），且站点 TLS 证书绑定域名，无法以 IP 直连渲染。
4. 已解析出 Hainan 前端 chunk 中的真实列表接口路径（selectInfoForIndex），但受 OAuth 网关拦截。

## 交付物
- PDF：`/tmp/hainan_kancha_daily_2026-08-28.pdf`（reportlab 生成，含封面/目录/正文表格/自动页脚，WPS 兼容）
- PDF base64：`/tmp/pdf_b64.txt`（14573 字符）
- 钉钉卡片纯文本：`/tmp/dingtalk_card.txt`

## 后续可优化
- 获取 ccgp-hainan.gov.cn 开放数据 API Token / 信息API 订阅 → 可稳定拉取海南省全量公告并每日自动成稿。
- 或人工导出后交由本代理做结构化解析。
