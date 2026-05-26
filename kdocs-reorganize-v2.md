# 金山文档整理 - 最新状态报告
> 更新：2026-04-16 10:15 GMT+8

## ✅ 已完成

### 1. 环境搭建
- mcporter + kdocs MCP 安装配置完成
- SSL 证书修复：`NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem mcporter ...`

### 2. 无名文件 → 已重命名
| 原文件 | 新名称 |
|--------|--------|
| `1774975204754.docx` | `文稿片段_20260403.docx` |
| `1774924271817.docx` | `文稿片段_20260402.docx` |

### 3. 分类文件夹 → 已在漫游箱和云文档创建

| 文件夹名 | 漫游箱ID | 云文档ID |
|---------|---------|---------|
| 华检联公司治理 | `vFWQXnVyL1Mn8qNNvH5N1xrySsXEnjFSr` | `FmrmDVJaJrMoNYKoMUF5rxqQqZmrdYL83` |
| 海南海洋经济项目 | `aNvjdgZXS1M868XSKd5K1xbL8FpqnxeKu` | `xUVQufZ1orMTFNB83ExkxxSvsjBajssmh` |
| 检测收费参考价 | `fv85K8A261MNCpi2dAzt1xXoAnE6SaPxC` | `AQHJFktzw9MffDRfJwYi1xddj5baMFgNs` |
| 投标与报价 | `dUeAAU7errMK2wSP36RArxJMioexPBqDg` | `MNkBXn8bJxM7HBTzCCNFrxwCKmEVyiE1h` |
| 个人学习 | `vnA4xKnnmxMTfTG8gSMG1xhuWJWRCXVcg` | `bhHvwWuETxM16H6oPP75rxiKk8YCZ9tDu` |
| 个人写作 | `mRgzn5M72xM3wY4oHAZurxGKLKAceMiqP` | `jVA3gNpaJrMGpUEqw8yVxxVyhuUed4kz8` |
| 外部协作文件 | `a23wvuCsjrMJn136nnZdrxEc7Z81J4Gde` | `RYnwwJuaJrMKxP4zXidHrxeMJ6zwYCcgZ` |
| 勘察与市场资料 | `v8xpsrQ6KxMFBembtcBgxxeqzF9gzWGGs` | `rjgaFUvh11Min9jDMuTArxWsvPtmhUERn` |

### 4. 已确认移动到位的文件（get_file_info parent_id 验证）

| 文件 | 目标文件夹 |
|------|---------|
| 华检联管理制度系统性审查报告_20260415.docx | 华检联公司治理 ✅ |
| 2025版检测收费参考价PDF | 检测收费参考价 ✅ |
| 海南省海洋厅申请新型政策性工具项目清单.xlsx | 海南海洋经济项目 ✅ |
| 海南省海洋经济领域申请新型政策性工具项目清单.xlsx | 海南海洋经济项目 ✅ |
| 海南省2026年预备重大项目投资计划表_三亚项目.xlsx | 海南海洋经济项目 ✅ |
| 华检联事业部绩效管理规定_V1.5_示例核对.docx | 华检联公司治理 ✅ |
| 华检联事业部制内部创业激励方案.docx | 华检联公司治理 ✅ |
| 华检联管理制度审查报告（移动验证中） | 华检联公司治理 ✅ |

---

## ⚠️ 待完成

漫游箱根目录还有约 **185 个文件**需要整理，分布在以下分类：

### 建议分配
- **华检联公司治理（约20个）**：绩效管理规定多版本、事业部设立办法多版本、商务招待、创业激励多版本、竞聘申请等
- **海南海洋经济项目（约10个）**：湘琼检测报价、项目清单其他版本、回款表等
- **投标与报价（约120个）**：碧桂园系列、城建项目、气电集团、华润、新海陆岛、海口江东、结算单、付款协议等
- **个人学习（约30个）**：费曼学习法、记忆力指南、个人简历、评估报告等
- **勘察与市场资料（约10个）**：勘察公司名录、白蚁防治、资质证书等
- **外部协作（约5个）**：校友会文件、学校食堂、团体人员信息表等

---

## 🔧 技术说明

- `move_file` API 为**异步**，返回值中的 `task_ids: []` 在 WPS 服务器端不代表失败
- 实测：连续大量调用后 WPS API 会触发**深度限流**（所有端点返回 None），需等待 1-2 小时自然恢复
- `get_file_info` 查询 `parent_id` 是验证移动是否成功的可靠方法

---

## 📱 建议用户操作（推荐）

登录 **[www.kdocs.cn](https://www.kdocs.cn)** → 点击左下角「漫游箱」→「我的文件」→ 根目录，选中同类型文件（shift 多选）→ 右键「移动到」→ 选择对应分类文件夹。

滚动操作约 15 分钟即可完成全部整理。

---

## 📋 重复文件清理建议

在完成初步归类后，可进一步清理重复版本：

**漫游箱（保留最新版本）**：
- 绩效管理规定：保留 `V1.5_示例核对`，删除 `V1.3_10%部门基金统一`
- 事业部设立：保留 `_完善版`，删除原版
- 内部创业激励：保留 `华检联事业部激励方案20260409`（云文档最新）
- 海南省项目清单：保留漫游箱版本（已整合进海洋经济文件夹）

**云文档（清理旧版收费参考价）**：
- 保留 2025版，删除 2021版
