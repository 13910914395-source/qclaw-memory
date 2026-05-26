const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  LevelFormat, BorderStyle, WidthType, ShadingType, PageBreak,
  TableOfContents, PageNumber, Header, Footer, Table, TableRow, TableCell,
  UnderlineType
} = require('docx');
const fs = require('fs');

// Helper: create a styled paragraph
function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.spaceBefore || 120, after: opts.spaceAfter || 120, line: 360 },
    alignment: opts.align || AlignmentType.LEFT,
    ...opts,
    children: [
      new TextRun({
        text,
        font: opts.font || "Microsoft YaHei",
        size: opts.size || 24,
        bold: opts.bold || false,
        italics: opts.italic || false,
        color: opts.color || "000000",
        underline: opts.underline ? { type: UnderlineType.SINGLE } : undefined,
      })
    ]
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 36, bold: true, color: "1F4E79" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 30, bold: true, color: "2E75B6" })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 22 })]
  });
}

function numbered(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 22 })]
  });
}

function infoTable(rows) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const headerBorder = { style: BorderStyle.SINGLE, size: 4, color: "2E75B6" };
  const headerBorders = { top: headerBorder, bottom: headerBorder, left: headerBorder, right: headerBorder };
  
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [2500, 6526],
    rows: rows.map(([label, value], i) =>
      new TableRow({
        children: [
          new TableCell({
            borders: i === 0 ? headerBorders : borders,
            width: { size: 2500, type: WidthType.DXA },
            shading: i === 0 ? { fill: "2E75B6", type: ShadingType.CLEAR } : { fill: i % 2 === 0 ? "DEEAF1" : "FFFFFF", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({
              children: [new TextRun({ text: label, font: "Microsoft YaHei", size: 22, bold: i === 0, color: i === 0 ? "FFFFFF" : "000000" })]
            })]
          }),
          new TableCell({
            borders: i === 0 ? headerBorders : borders,
            width: { size: 6526, type: WidthType.DXA },
            shading: i === 0 ? { fill: "2E75B6", type: ShadingType.CLEAR } : { fill: i % 2 === 0 ? "DEEAF1" : "FFFFFF", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({
              children: [new TextRun({ text: value, font: "Microsoft YaHei", size: 22, bold: i === 0, color: i === 0 ? "FFFFFF" : "000000" })]
            })]
          })
        ]
      })
    )
  });
}

function divider() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6" } },
    children: []
  });
}

function insightBox(label, text) {
  return new Paragraph({
    spacing: { before: 160, after: 160 },
    shading: { fill: "EBF3FB", type: ShadingType.CLEAR },
    border: {
      left: { style: BorderStyle.THICK, size: 12, color: "2E75B6" }
    },
    indent: { left: 360 },
    children: [
      new TextRun({ text: label + " ", font: "Microsoft YaHei", size: 22, bold: true, color: "2E75B6" }),
      new TextRun({ text, font: "Microsoft YaHei", size: 22, color: "000000" })
    ]
  });
}

function tagBadge(text) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    shading: { fill: "DEEAF1", type: ShadingType.CLEAR },
    indent: { left: 360 },
    children: [new TextRun({ text: "「" + text + "」", font: "Microsoft YaHei", size: 22, color: "1F4E79" })]
  });
}

// Timeline helper
function timeline(date, event) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    indent: { left: 360 },
    children: [
      new TextRun({ text: date + "：", font: "Microsoft YaHei", size: 22, bold: true, color: "2E75B6" }),
      new TextRun({ text: event, font: "Microsoft YaHei", size: 22 })
    ]
  });
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 300 } } }
        }, {
          level: 1, format: LevelFormat.BULLET, text: "◦",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 960, hanging: 300 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 300 } } }
        }]
      }
    ]
  },
  styles: {
    default: {
      document: { run: { font: "Microsoft YaHei", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Microsoft YaHei", color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Microsoft YaHei", color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "2E75B6" } },
          spacing: { after: 120 },
          children: [new TextRun({ text: "用户叙事画像  |  QClaw AI 助手", font: "Microsoft YaHei", size: 18, color: "7F7F7F" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" } },
          spacing: { before: 120 },
          children: [
            new TextRun({ text: "第 ", font: "Microsoft YaHei", size: 18, color: "7F7F7F" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Microsoft YaHei", size: 18, color: "7F7F7F" }),
            new TextRun({ text: " 页", font: "Microsoft YaHei", size: 18, color: "7F7F7F" })
          ]
        })]
      })
    },
    children: [
      // === 封面区 ===
      new Paragraph({ spacing: { before: 1440, after: 120 }, alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 240, after: 120 },
        children: [new TextRun({ text: "用户叙事画像", font: "Microsoft YaHei", size: 72, bold: true, color: "1F4E79" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 600 },
        children: [new TextRun({ text: "User Narrative Profile", font: "Arial", size: 36, color: "7F7F7F", italics: true })]
      }),
      divider(),
      new Paragraph({ spacing: { before: 480, after: 0 }, alignment: AlignmentType.CENTER, children: [] }),

      // 核心原型标签
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 480 },
        shading: { fill: "EBF3FB", type: ShadingType.CLEAR },
        children: [new TextRun({ 
          text: "Archetype：勘察检测行业非技术实践者，以业务目标驱动技术集成\n——从「工具探索者」进化为「自动化工作流构建者」",
          font: "Microsoft YaHei", size: 26, bold: true, color: "1F4E79"
        })]
      }),

      // 基本信息表
      new Paragraph({ spacing: { before: 480, after: 200 }, children: [] }),
      heading2("基本信息"),
      infoTable([
        ["姓名", "符发（Fa's）"],
        ["技术背景", "无开发基础（非技术人员）"],
        ["权限角色", "钉钉企业管理员"],
        ["常驻地", "海口"],
        ["行业领域", "勘察检测行业（工程建设 / 检测技术）"],
        ["社交圈", "朋友经营华检联（海南）检测技术有限公司（B级勘察类公司）"],
        ["设备", "Fa's Mac mini（arm64）"],
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // === 第一章 ===
      heading1("📖 Chapter 1：全景语境"),

      para("符发是海口勘察检测行业的企业管理人员，担任钉钉企业管理员。2026年4月7日密集完成四项技能安装与钉钉开放平台配置，经两次通道修复（重启Gateway → 修正凭证文件路径）后，钉钉通道进入可用状态。", { spaceAfter: 160 }),

      para("4月8日清晨，钉钉通道首次承载生产级任务——海南招标监控 cron 于凌晨3点触发，PDF报告推送至「华检联业务信息群」。这是从「技术配置」到「业务基础设施」的质变，标志着工作流从探索进入落地阶段。同日上午建立招标信息源标准：明确要求 .gov.cn 官方来源，避开非官方聚合网站——这一标准暗示用户曾因劣质信息源吃过亏。", { spaceAfter: 160 }),

      para("同日上午，用户首次尝试将工程图纸（综合楼结构图，DWG格式，9.4MB）交由AI进行构件统计。AI反馈需转换格式后识别，用户未受阻挠，而是沿着「问题 → 方案」路径推进——与其处理钉钉通道故障时展现的运维心智一脉相承。DWG处理需求揭示AI角色从「信息助手」扩展到「工程计算助手」的边界突破。", { spaceAfter: 200 }),

      insightBox("关键叙事线", "从工具探索 → 日常自动化（早报、文件读取） → 业务自动化（招标监控） → 专业计算（工程图纸），每一步都遵循「确认边界 → 寻找路径 → 突破边界」的递进模式。"),

      // === 第二章 ===
      heading1("🎨 Chapter 2：生活的肌理"),

      para("用户习惯凌晨时段（03:17–03:58）进行技术操作和 cron 任务运行，凌晨3点运行招标监控——在上班前生成报告，体现对业务节奏的深度把控。密集安装技能——体现「拥抱数字化但回避代码」的技术采用模式。每天固定晨间获取天气和新闻摘要，以「信息驱动」开启一天。", { spaceAfter: 160 }),

      para("选择群推送而非个人通知（华检联业务信息群），桌面存放跨公司业务文件——指向团队协作场景与跨区域项目 / 分子公司管理。模型切换至 qwen-portal / qwen-plus 表明用户开始关注底层性能，具备「自下而上」的系统优化意识。", { spaceAfter: 200 }),

      // === 第三章 ===
      heading1("🤖 Chapter 3：交互与认知协议"),

      heading2("3.1  沟通策略"),
      bullet("直接务实：关注问题是否解决，沟通简洁高效"),
      bullet("避免代码层细节：无开发背景，聚焦配置层和结果层"),
      bullet("结合行业语境：涉及勘察文档 / 归档 / 招标等场景时使用行业相关表达"),
      new Paragraph({ spacing: { before: 160, after: 0 }, children: [] }),

      heading2("3.2  决策逻辑"),
      bullet("问题诊断 → 能力扩展：对AI能力边界有清晰认知，主动推动系统进化而非被动等待"),
      bullet("目标导向：关注数据能否读取 / 文档能否归档 / 报告能否推送，而非技术实现细节"),
      bullet("效率递进：从「能做」到「自动做」，持续优化工作流"),
      bullet("系统级排查优先：遇问题先尝试重启服务 / 检查配置 / 定位文件路径"),

      // === 第四章 ===
      heading1("🧩 Chapter 4：深层洞察与演变"),

      heading2("矛盾统一性"),
      para("无开发基础却能定位文件路径级别的运维错误、构建生产级自动化工作流——不懂代码，但懂业务目标，愿意动手尝试系统级操作，在「技术外行」与「业务能手」之间找到自己的实践路径。", { spaceAfter: 240 }),

      heading2("演变轨迹"),
      timeline("2026-04-07", "密集安装技能 + 配置钉钉应用，完成工具探索阶段"),
      timeline("2026-04-08 凌晨", "提出早报需求 + 文件读取能力，从「按需使用」过渡到「日常自动化」"),
      timeline("2026-04-08 清晨", "海南招标监控场景落地，钉钉通道从「技术配置」升级为「业务基础设施」"),
      timeline("2026-04-08", "运维心智从「重启服务」进化为「定位凭证文件路径错误」，排查粒度显著细化"),
      timeline("2026-04-08", "AI角色从「信息助手」扩展至「工程计算助手」（DWG图纸处理）"),
      timeline("2026-04-09", "军队采购网结构检测招标监控落地，官方信息来源标准进一步确立"),
      new Paragraph({ spacing: { before: 200, after: 0 }, children: [] }),

      heading2("涌现特征"),
      tagBadge("自动化工作流构建者 - 首个业务监控场景成功落地并承载生产任务"),
      tagBadge("业务基础设施搭建者 - 钉钉通道经生产验证，成为日常业务依赖"),
      tagBadge("效率递进者 - 从「能做」到「自动做」，持续驱动能力边界外扩"),
      tagBadge("晨间信息消费者 - 固定晨间天气 + 新闻早报，融入日间决策节奏"),
      tagBadge("主动排查派 - 遇问题先动手尝试，排查粒度持续细化"),
      tagBadge("能力边界清醒者 - 清晰认知AI局限，主动寻找突破路径而非放弃"),
      tagBadge("官方信息源坚守者 - 对.gov.cn来源的坚持，暗示质量底线思维"),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/Users/fasimac/Desktop/用户叙事画像.docx", buf);
  console.log("✅ 生成成功：/Users/fasimac/Desktop/用户叙事画像.docx");
}).catch(e => { console.error("❌", e.message); process.exit(1); });
