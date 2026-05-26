const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat
} = require('docx');
const fs = require('fs');

const C = {
  TITLE: "1F3864",
  ACCENT: "2E75B6",
  WARN: "C00000",
  BG_H: "D6E4F0",
  BG_A: "F5F9FD",
  TEXT: "2C2C2C",
  SUB: "595959",
  GREEN: "2E7D32",
  GOLD: "8B6914",
  WARN_BG: "FFF5F5",
  GREEN_BG: "F0FFF4",
  BLUE_BG: "EBF3FB",
  YELLOW_BG: "FFF8E1",
  YELLOW2_BG: "FFF3CD",
};

const bd = (color = "CCCCCC") => ({ style: BorderStyle.SINGLE, size: 4, color });
const borders = (c = "CCCCCC") => ({ top: bd(c), bottom: bd(c), left: bd(c), right: bd(c) });

function pg(text, opts = {}) {
  const { bold = false, sz = 22, color = C.TEXT, sp = 200, align = AlignmentType.LEFT, font = "宋体" } = opts;
  return new Paragraph({ alignment: align, spacing: { before: sp, after: sp }, children: [new TextRun({ text, bold, size: sz, color, font })] });
}

function h(text, level) {
  const sizes = [0, 40, 30, 26];
  const spaces = [0, { before: 400, after: 200 }, { before: 300, after: 160 }, { before: 240, after: 120 }];
  const colors = [null, C.TITLE, C.ACCENT, C.TEXT];
  return new Paragraph({
    heading: level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3,
    spacing: spaces[level],
    border: level === 1 ? { bottom: { style: BorderStyle.SINGLE, size: 8, color: C.ACCENT } } : undefined,
    children: [new TextRun({ text, bold: true, size: sizes[level], color: colors[level], font: "宋体" })]
  });
}

function bl(text, opts = {}) {
  const { sz = 22, color = C.TEXT, bold = false } = opts;
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, size: sz, color, bold, font: "宋体" })]
  });
}

function nr(text, n) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { before: 80, after: 80 },
    children: [
      new TextRun({ text: `${n}. `, bold: true, size: 22, color: C.ACCENT, font: "宋体" }),
      new TextRun({ text, size: 22, color: C.TEXT, font: "宋体" })
    ]
  });
}

function box(text, opts = {}) {
  const { sz = 28, bold = true, color = C.TITLE, bg = C.BLUE_BG } = opts;
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 120 },
    shading: { fill: bg, type: ShadingType.CLEAR },
    children: [new TextRun({ text, bold, size: sz, color, font: "宋体" })]
  });
}

function note(text, opts = {}) {
  const { sz = 20, color = C.GOLD, bg = C.YELLOW2_BG } = opts;
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    shading: { fill: bg, type: ShadingType.CLEAR },
    children: [new TextRun({ text, size: sz, color, font: "宋体" })]
  });
}

function sp(before = 0, after = 100) {
  return new Paragraph({ spacing: { before, after }, children: [new TextRun("")] });
}

function th(text, w) {
  return new TableCell({
    borders: borders("BFBFBF"),
    width: { size: w, type: WidthType.DXA },
    shading: { fill: C.BG_H, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 120, right: 120 },
    verticalAlign: "center",
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, bold: true, size: 20, color: C.TITLE, font: "宋体" })] })]
  });
}

function td(text, w, opts = {}) {
  const { align = AlignmentType.CENTER, bold = false, bg = "FFFFFF", color = C.TEXT } = opts;
  return new TableCell({
    borders: borders("CCCCCC"),
    width: { size: w, type: WidthType.DXA },
    shading: { fill: bg, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    verticalAlign: "center",
    children: [new Paragraph({ alignment: align, children: [new TextRun({ text: String(text), bold, size: 20, color, font: "宋体" })] })]
  });
}

function table(rows, colWidths) {
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: colWidths,
    rows
  });
}

function tr(cells) { return new TableRow({ children: cells }); }

// ===== 构建文档内容 =====
const children = [];

// 封面
children.push(sp(400, 0));
children.push(pg("时间自由", { bold: true, sz: 72, color: C.TITLE, align: AlignmentType.CENTER, sp: 0 }));
children.push(pg("重新定义财务自由的本质", { sz: 36, color: C.ACCENT, align: AlignmentType.CENTER, sp: 120 }));
children.push(sp(0, 200));
children.push(pg("内容来源：元宝AI（微信视频号解读）  |  整理加工：QClaw", { sz: 18, color: C.SUB, align: AlignmentType.CENTER }));

// 第一部分
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("一、核心概念重构", 1));
children.push(h("▌ 传统误区", 2, C.WARN));
children.push(pg("将财务自由等同于巨额财富积累（如1000万/1亿）——这是最大的思维陷阱。", { sz: 22, color: C.WARN, bold: true }));
children.push(sp(80, 80));
children.push(h("▌ 本质定义", 2));
children.push(box("被动收入 > 生活开支  =  时间自主权", { sz: 32 }));
children.push(sp(120, 80));
children.push(h("▌ 关键转变", 2));
children.push(pg("", { sz: 16, sp: 60 }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 100, after: 200 },
  children: [
    new TextRun({ text: "从 ", size: 28, color: C.SUB, font: "宋体" }),
    new TextRun({ text: ""赚更多"", bold: true, size: 28, color: C.WARN, font: "宋体" }),
    new TextRun({ text: "  →  ", size: 28, color: C.SUB, font: "宋体" }),
    new TextRun({ text: ""花更少"", bold: true, size: 28, color: C.GREEN, font: "宋体" }),
    new TextRun({ text: "  的思维升级", size: 28, color: C.SUB, font: "宋体" }),
  ]
}));
children.push(sp(100, 100));

children.push(table(tr([
  th("维度", 2000), th("❌ 传统思维", 3513), th("✅ FIRE思维", 3513)
]), [2000, 3513, 3513]));
children.push(table(tr([
  td("目标", 2000, { bg: C.BG_H, bold: true }), td("积累1000万/1亿", 3513, { bg: C.WARN_BG }), td("被动收入覆盖支出", 3513, { bg: C.GREEN_BG })
]), [2000, 3513, 3513]));
children.push(table(tr([
  td("路径", 2000, { bg: C.BG_H, bold: true }), td("拼命工作+高位投资", 3513, { bg: C.WARN_BG }), td("降低分母+稳定现金流", 3513, { bg: C.GREEN_BG })
]), [2000, 3513, 3513]));
children.push(table(tr([
  td("核心指标", 2000, { bg: C.BG_H, bold: true }), td("账户余额", 3513, { bg: C.WARN_BG }), td("收入/支出比率", 3513, { bg: C.GREEN_BG })
]), [2000, 3513, 3513]));
children.push(table(tr([
  td("自由度", 2000, { bg: C.BG_H, bold: true }), td("等我赚够了再说", 3513, { bg: C.WARN_BG }), td("今天就可以开始选择", 3513, { bg: C.GREEN_BG })
]), [2000, 3513, 3513]));

// 第二部分
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("二、FIRE运动实践框架", 1));
children.push(h("▌ 核心公式", 2));
children.push(sp(100, 80));
children.push(box("所需本金 = 年度开支 ÷ 4%", { sz: 34 }));
children.push(pg("（即"4%规则"：每年从本金中提取不超过4%，可维持30年以上资金不枯竭）", { sz: 20, color: C.SUB, align: AlignmentType.CENTER, sp: { before: 0, after: 200 } }));

children.push(table(tr([th("要素", 2200), th("计算方式", 3000), th("示例数据", 3826)]), [2200, 3000, 3826]));
children.push(table(tr([td("安全提取率", 2200, { bg: C.BG_H, bold: true }), td("年度开支 × 25", 3000), td("月支出1万 → 需300万本金", 3826)]), [2200, 3000, 3826]));
children.push(table(tr([td("4%规则", 2200, { bg: C.BG_H, bold: true }), td("1994年Bengen提出", 3000), td("300万 → 年提取12万", 3826)]), [2200, 3000, 3826]));
children.push(table(tr([td("成功概率", 2200, { bg: C.BG_H, bold: true }), td("Morningstar验证", 3000), td("超90%概率维持30年", 3826)]), [2200, 3000, 3826]));
children.push(table(tr([td("适用前提", 2200, { bg: C.BG_H, bold: true }), td("全球化资产配置", 3000), td("指数基金+债券+黄金等分散", 3826)]), [2200, 3000, 3826]));
children.push(sp(200, 80));
children.push(note("⚠️ 重要前提：4%规则基于美国市场历史数据，实际成功概率受市场周期、通胀水平、寿命预期等因素影响，需定期复盘调整。", { color: C.GOLD, bg: C.YELLOW_BG }));

// 第三部分
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("三、财富积累的数学逻辑", 1));
children.push(h("▌ 复利模型（标普500历史数据）", 2));
children.push(sp(80, 60));

children.push(table(tr([th("参数", 4513), th("数值", 4513)]), [4513, 4513]));
children.push(table(tr([td("每月定投", 4513, { bg: C.BG_H, bold: true }), td("3,000 元", 4513)]), [4513, 4513]));
children.push(table(tr([td("投资周期", 4513, { bg: C.BG_H, bold: true }), td("25 年", 4513)]), [4513, 4513]));
children.push(table(tr([td("年化收益率", 4513, { bg: C.BG_H, bold: true }), td("10%", 4513)]), [4513, 4513]));
children.push(table(tr([td("累计本金", 4513, { bg: C.BG_H, bold: true }), td("90 万元（3,000 × 12 × 25）", 4513)]), [4513, 4513]));
children.push(table(tr([td("复利收益", 4513, { bg: C.BG_H, bold: true }), td("308 万元", 4513, { color: C.GREEN, bold: true })]), [4513, 4513]));
children.push(table(tr([td("终值合计", 4513, { bg: C.BG_H, bold: true }), td("398 万元", 4513, { bg: C.BG_H, bold: true, color: C.TITLE })]), [4513, 4513]));
children.push(table(tr([td("收益/本金倍数", 4513, { bg: C.BG_H, bold: true }), td("3.4 倍（复利威力）", 4513, { color: C.GREEN, bold: true })]), [4513, 4513]));
children.push(sp(200, 80));

children.push(h("▌ 地理套利：降低生活成本", 2));
children.push(pg("地理套利（Geographic Arbitrage）：利用不同城市间的生活成本差异，放大被动收入购买力。", { sz: 22 }));
children.push(sp(80, 80));

children.push(table(tr([th("城市类型", 3000), th("月均生活支出", 3000), th("所需本金（年支×25）", 3026)]), [3000, 3000, 3026]));
children.push(table(tr([td("一线城市（月入1万+）", 3000, { bg: C.WARN_BG }), td("~10,000 元", 3000, { bg: C.WARN_BG }), td("300 万", 3026, { bg: C.WARN_BG })]), [3000, 3000, 3026]));
children.push(table(tr([td("二三线城市", 3000), td("~5,000 元", 3000), td("150 万", 3026)]), [3000, 3000, 3026]));
children.push(table(tr([td("大理 / 清迈 / 东南亚", 3000, { bg: C.GREEN_BG }), td("~3,000 元", 3000, { bg: C.GREEN_BG }), td("90 万", 3026, { bg: C.GREEN_BG, color: C.GREEN, bold: true })]), [3000, 3000, 3026]));

// 第四部分
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("四、生活方式设计", 1));
children.push(h("▌ 成本优化案例", 2));
children.push(bl("北上广深 → 大理/清迈：生活成本降低 50% 以上，同时幸福感提升"));
children.push(bl("极简生活：重新定义"足够好"的标准，减少物质焦虑"));
children.push(bl("数字游民（Digital Nomad）：远程工作+低成本城市，效率与自由兼得"));
children.push(sp(120, 80));
children.push(h("▌ 时间价值公式", 2));
children.push(sp(80, 60));
children.push(box("30–60岁 黄金30年  >  延迟满足的退休生活", { sz: 30 }));
children.push(pg("真正的FIRE不是"拼命存钱等退休"，而是在黄金年龄段就拥有时间自主权。", { sz: 20, color: C.SUB, align: AlignmentType.CENTER }));

// 第五部分
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("五、执行策略", 1));
children.push(nr("启动条件：每月3,000元定投全球指数基金（分散配置，降低单一市场风险）", 1));
children.push(sp(80, 60));
children.push(nr("持续要素：保持10%年化收益预期，拒绝短期市场波动干扰，坚持长期主义", 2));
children.push(sp(80, 60));
children.push(nr("终极目标：账户余额 ≠ 成功标准，可自由选择每日行程才是核心指标", 3));
children.push(sp(200, 80));

children.push(h("▌ 三大常见陷阱", 2));
children.push(table(tr([th("陷阱", 3000), th("说明", 6026)]), [3000, 6026]));
children.push(table(tr([td("高收入高消费陷阱", 3000, { bg: C.WARN_BG, bold: true, color: C.WARN }), td("收入涨了，消费也跟着涨，永远存不下本金", 6026)]), [3000, 6026]));
children.push(table(tr([td("投资过度集中", 3000, { bg: C.WARN_BG, bold: true, color: C.WARN }), td("ALL IN 单一个股或单一市场，黑天鹅事件导致归零", 6026)]), [3000, 6026]));
children.push(table(tr([td("低估生活成本", 3000, { bg: C.WARN_BG, bold: true, color: C.WARN }), td("医疗、子女、意外支出未纳入FIRE计算基础", 6026)]), [3000, 6026]));

// 结语
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h("结语：建立系统，而非追求数字", 1));
children.push(sp(100, 80));
children.push(box("核心在于建立"收入 − 支出 > 0"的可持续系统，\n而非追求账户里的绝对数字。", { sz: 28 }));
children.push(sp(200, 80));
children.push(note("⚠️ 数据警示：所有案例数据均为假设（如25年398万），实际收益需根据市场调整。本文档仅供思维启发，不构成投资建议。投资有风险，决策需谨慎。", { color: C.GOLD, bg: C.YELLOW2_BG }));
children.push(sp(200, 100));
children.push(pg("整理日期：2026年4月22日  |  整理工具：QClaw AI", { sz: 18, color: C.SUB, align: AlignmentType.RIGHT }));

// ===== 生成文档 =====
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 480, hanging: 240 } } } }]
      },
      {
        reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 300 } } } }]
      },
    ]
  },
  styles: {
    default: { document: { run: { font: "宋体", size: 22, color: C.TEXT } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 40, bold: true, color: C.TITLE, font: "宋体" },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, color: C.ACCENT, font: "宋体" },
        paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, color: C.TEXT, font: "宋体" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          spacing: { before: 0, after: 0 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.ACCENT } },
          children: [
            new TextRun({ text: "FIRE运动 · 财务自由实践指南", size: 18, color: C.SUB, font: "宋体" }),
            new TextRun({ text: "    2026年4月", size: 18, color: C.SUB, font: "宋体" }),
          ]
        })
      ] })
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.ACCENT } },
          spacing: { before: 80, after: 0 },
          children: [
            new TextRun({ text: "第 ", size: 18, color: C.SUB, font: "宋体" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: C.SUB, font: "宋体" }),
            new TextRun({ text: " 页", size: 18, color: C.SUB, font: "宋体" }),
            new TextRun({ text: "    |    内容由 QClaw AI 整理加工", size: 18, color: C.SUB, font: "宋体" }),
          ]
        })
      ] })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = "/Users/lijing/.qclaw/workspace/FIRE财务自由实践指南_20260422.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("✅ 文档生成成功：" + outPath);
}).catch(err => {
  console.error("❌ 生成失败：", err.message);
  process.exit(1);
});
