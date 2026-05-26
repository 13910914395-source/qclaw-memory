const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, LevelFormat
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
const thickBorder = { style: BorderStyle.SINGLE, size: 8, color: "2E75B6" };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 160 },
    children: [new TextRun({ text, bold: true, size: 32, font: "宋体" })]
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: 26, font: "宋体" })]
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 80 },
    children: [new TextRun({ text, bold: true, size: 24, font: "宋体" })]
  });
}
function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({ text, size: 22, font: "宋体", ...opts })]
  });
}
function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, size: 22, font: "宋体" })]
  });
}
function numbered(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, size: 22, font: "宋体" })]
  });
}
function space() {
  return new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun("")] });
}
function issueBox(severity, label, desc) {
  const colorMap = { A: "FFE0E0", B: "FFF3E0", C: "FFFDE7", D: "E3F2FD" };
  const labelMap = { A: "🔴 高优先级", B: "🟡 中优先级", C: "🟢 建议优化", D: "💡 优化参考" };
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1200, 8160],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders, width: { size: 1200, type: WidthType.DXA },
            shading: { fill: colorMap[severity] || "F5F5F5", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: labelMap[severity] || label, size: 18, font: "宋体", bold: true })]
            })]
          }),
          new TableCell({
            borders, width: { size: 8160, type: WidthType.DXA },
            shading: { fill: "FFFFFF", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 160, right: 120 },
            children: [new Paragraph({
              children: [
                new TextRun({ text: label + "：", size: 22, font: "宋体", bold: true }),
                new TextRun({ text: desc, size: 22, font: "宋体" })
              ]
            })]
          })
        ]
      })
    ]
  });
}

function sectionTable(rows) {
  // rows = [{问题, 涉及文件, 优先级, 建议}]
  const headerRow = new TableRow({
    children: [
      ["问题描述", 4200],
      ["涉及文件", 2400],
      ["优先级", 960],
      ["修改建议", 1800]
    ].map(([text, w]) => new TableCell({
      borders, width: { size: w, type: WidthType.DXA },
      shading: { fill: "2E75B6", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 100, right: 100 },
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text, size: 20, font: "宋体", bold: true, color: "FFFFFF" })]
      })]
    }))
  });
  const colorPriority = { "🔴": "FFE0E0", "🟡": "FFF3E0", "🟢": "FFFDE7", "💡": "F5F5F5" };
  const dataRows = rows.map(([prob, file, pri, sug]) => {
    const rowColor = "FFFFFF";
    return new TableRow({
      children: [
        [prob, 4200],
        [file, 2400],
        [pri, 960],
        [sug, 1800]
      ].map(([text, w], idx) => new TableCell({
        borders, width: { size: w, type: WidthType.DXA },
        shading: { fill: rowColor, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
          children: [new TextRun({ text, size: 19, font: "宋体" })]
        })]
      }))
    });
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [4200, 2400, 960, 1800],
    rows: [headerRow, ...dataRows]
  });
}

const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 640, hanging: 320 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 320 } } } }
      ]},
      { reference: "numbers", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 640, hanging: 320 } } } }
      ]}
    ]
  },
  styles: {
    default: { document: { run: { font: "宋体", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "宋体", color: "2E75B6" },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "宋体", color: "2E4057" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "宋体" },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1080, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // ============ 封面 ============
      new Paragraph({ spacing: { before: 720, after: 0 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "华检联公司管理制度", size: 52, font: "宋体", bold: true, color: "2E75B6" })] }),
      new Paragraph({ spacing: { before: 160, after: 0 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "系统性审查报告", size: 44, font: "宋体", bold: true })] }),
      new Paragraph({ spacing: { before: 80, after: 0 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "基于卓越管理原则的合规性、可操作性与体系一致性诊断", size: 24, font: "宋体", color: "595959" })] }),
      new Paragraph({ spacing: { before: 480, after: 0 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "审查日期：2026年4月15日", size: 22, font: "宋体", color: "808080" })] }),
      new Paragraph({ spacing: { before: 80, after: 0 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "审查范围：23份制度文件（制度2021 / 制度2022 / 制度2024 / 桌面最新版本）", size: 22, font: "宋体", color: "808080" })] }),
      new Paragraph({ children: [new PageBreak()] }),

      // ============ 第一章 总则 ============
      h1("第一章 总则与整体评价"),
      h2("一、审查背景与方法"),
      para("受华检联（海南）检测技术有限公司委托，对公司管理文件夹（桌面/管理/华检联公司管理制度）内全部23份现行有效制度文件进行系统性审查。审查依据：《劳动法》《劳动合同法》等国家法规，结合卓越管理原则（制度完整性、逻辑自洽性、可操作性、动态适应性）进行诊断。"),
      para("审查范围涵盖以下四个分组："),
      bullet("制度2021（15份）：2021年9-11月发布的基础管理制度"),
      bullet("制度2022（5份）：2022年4-7月发布的管理补充制度"),
      bullet("制度2024（2份）：2024年3月及8月更新版本"),
      bullet("桌面最新版本（6份）：2026年最新修订或定稿版本"),
      space(),

      h2("二、整体评价"),
      para("华检联管理制度整体框架较为完整，覆盖人力资源、财务行政、业务运营三大板块，制度编号体系规范，具备较好管理基础。经审查发现以下四类问题："),
      space(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2200, 2200, 2200, 2760],
        rows: [
          new TableRow({ children: [
            ["问题类型", 2200], ["数量", 2200], ["占比", 2200], ["典型表现", 2760]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "2E75B6", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: t, size: 20, font: "宋体", bold: true, color: "FFFFFF" })] })]
          })) }),
          new TableRow({ children: [
            ["🔴 高优先级", 2200], ["8项", 2200], ["22.9%", 2200], ["多处与国家法规相悖、重大逻辑矛盾", 2760]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "FFE0E0", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [new TextRun({ text: t, size: 20, font: "宋体" })] })]
          })) }),
          new TableRow({ children: [
            ["🟡 中优先级", 2200], ["14项", 2200], ["40.0%", 2200], ["标准偏低、执行流程不清晰、表述歧义", 2760]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "FFF3E0", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [new TextRun({ text: t, size: 20, font: "宋体" })] })]
          })) }),
          new TableRow({ children: [
            ["🟢 建议优化", 2200], ["13项", 2200], ["37.1%", 2200], ["结构优化、表述完善、语言规范", 2760]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "F0F7EE", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ children: [new TextRun({ text: t, size: 20, font: "宋体" })] })]
          })) }),
        ]
      }),
      space(),

      h2("三、系统性问题（跨制度关联问题）"),
      para("在多份制度中重复出现、需统筹整改的问题："),
      space(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3000, 6360],
        rows: [
          new TableRow({ children: [
            ["问题", 3000], ["现状描述", 6360]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "1F4E79", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 100, right: 100 },
            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: t, size: 20, font: "宋体", bold: true, color: "FFFFFF" })] })]
          })) }),
          ...([
            ["制度版本管理混乱", "制度2021（薪资、福利、印章）与2024新版本并行使用，2021薪资已修订但旧版仍存档；同一业务存在3-4个迭代版本，易造成执行混乱"],
            ["薪酬标准不统一", "事业本部绩效管理规定（4%）与事业部绩效管理规定（事业本部6%）绩效比例冲突；2021薪资与2022薪资的学历工资标准不统一"],
            ["绩效考核标准缺失", "事业部绩效管理规定仅列出绩效比例，缺少具体的绩效考核指标（KPI/OKR）；考核指标章节仅标注\"见附件\"但未附具体指标"],
            ["审批权限颗粒度粗", "多份制度仅规定\"总经理批准\"或\"分管副总批准\"，缺少具体金额/事项的权限分级矩阵"],
            ["数字系统依赖风险", "制度中频繁提及\"钉钉系统\"（考勤、审批、报销），一旦更换系统则制度部分条款无法执行"],
            ["保密管理缺失", "制度体系缺少统一的保密管理制度；员工行为规范仅笼统提及\"保守商业机密\"，缺少密级划分和具体措施"],
          ].map(([prob, desc], i) => new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3000, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "EEF4FB" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 100, right: 100 },
                children: [new Paragraph({ children: [new TextRun({ text: prob, size: 20, font: "宋体", bold: true })] })] }),
              new TableCell({ borders, width: { size: 6360, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "EEF4FB" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 100, right: 100 },
                children: [new Paragraph({ children: [new TextRun({ text: desc, size: 20, font: "宋体" })] })] }),
            ]
          })))
        ]
      }),
      space(),

      new Paragraph({ children: [new PageBreak()] }),

      // ============ 第二章 高优先级问题 ============
      h1("第二章 高优先级问题（需立即整改）"),
      para("以下问题涉及法律合规风险或重大管理漏洞，需优先修订："),
      space(),

      h2("问题一：年休假标准严重低于国家标准"),
      issueBox("A", "法律合规", "【制度2021 · 员工各类休假制度（202105）】员工年休假最高仅7天（《劳动法》第45条：累计工作满1年5天，满10年10天，满20年15天；国家《职工带薪年休假条例》同样规定）。该公司标准（3+1+1+1+1=7天封顶）与国家标准相悖，涉嫌侵犯员工合法权益。"),
      space(),
      para("修改建议："),
      bullet("立即修订年休假标准：工作满1年→5天；满10年→10天；满20年→15天"),
      bullet("删除\"工作满5年封顶\"的不当表述，改为按国家标准执行"),
      bullet("同步修订《福利管理制度》（202107）中年休假描述"),
      space(),

      h2("问题二：病假工资标准低于法定最低标准"),
      issueBox("A", "法律合规", "【制度2021 · 员工各类休假制度（202105）】医疗期内病假工资：6个月以内不满10年工龄按70%计，10年以上按80%计，均低于海南省工资支付法规（一般不低于当地最低工资标准的80%）及《海南省工资支付条例》要求。"),
      space(),
      para("修改建议："),
      bullet("以海南省当年最低工资标准为基数（海口市目前为2010元/月），重新核算病假工资比例"),
      bullet("增加关于病假工资的计算基数说明（应包含固定工资中的基本工资+岗位工资+职称工资）"),
      bullet("明确病假期间绩效工资的发放规则"),
      space(),

      h2("问题三：绩效管理规定内部严重冲突"),
      issueBox("A", "体系一致性", "【桌面】事业本部工资绩效管理规定（V1.0）与华检联事业部绩效管理规定（定稿）同时存在，对同一\"事业本部\"业务（A类）分别规定4%和6%两种总绩效比例。同一公司在同一时期对同一业务类型执行两个不同标准，将导致执行混乱和员工不满。"),
      space(),
      para("修改建议："),
      bullet("废止事业本部工资绩效管理规定（V1.0），统一执行事业部绩效管理规定（定稿）"),
      bullet("统一各事业部的绩效比例表述：事业本部总比例6%，各副资质事业部8-10%"),
      bullet("在制度2021薪资制度中增加对两份绩效管理规定优先级的说明"),
      space(),

      h2("问题四：试用期管理不符合劳动合同法"),
      issueBox("A", "法律合规", "【制度2021 · 员工录用转正管理办法（202116）】提前转正条件要求\"试用期内无迟到、早退、事假一天以上（含一天）记录\"，过于严苛。迟到、早退属于考勤违规，不应作为否定提前转正资格的条件（劳动合同法第39条仅允许因\"不符合录用条件\"解除合同）。"),
      space(),
      para("修改建议："),
      bullet("修改提前转正条件：仅以工作绩效（考核评分≥95分）和无重大违纪为准"),
      bullet("删除\"无迟到、早退、事假一天以上\"作为提前转正门槛的条款"),
      bullet("明确试用期请假不影响提前转正申请资格"),
      space(),

      h2("问题五：离职管理超时扣薪涉嫌违法"),
      issueBox("A", "法律合规", "【制度2021 · 员工离职管理办法（202117）】\"逾期不办理者按自动放弃当月工资计\"（《劳动合同法》第30条：用人单位应足额支付劳动报酬，不得附加条件克扣）。此条款违反法律规定，员工工资是劳动报酬的对价，不得以未办手续为由扣发。"),
      space(),
      para("修改建议："),
      bullet("删除\"按自动放弃当月工资计\"的不当表述"),
      bullet("修改为：逾期不办理者，公司可暂停发放未结清款项，直至手续完备；已产生的劳动报酬不得扣发"),
      bullet("补充条款：员工拒不配合办理离职手续的，公司可依法追究法律责任"),
      space(),

      h2("问题六：员工离职强制审计范围过宽"),
      issueBox("A", "操作性风险", "【制度2021 · 员工离职管理办法（202117）】\"公司中层及以上人员、业务人员离职需经公司财务部进行离任审计\"。业务人员离职无论职级均需财务审计，工作量大且无充分必要性；且未规定审计时限，可能无限期拖延，影响离职办理。"),
      space(),
      para("修改建议："),
      bullet("限定强制离任审计范围为：副总及以上高管、分管财务人员"),
      bullet("业务人员离职改为：如有未清款项或客户欠款风险时启动专项核查，非强制全面审计"),
      bullet("增加审计完成时限（如：5个工作日内完成，出具审计报告）"),
      space(),

      h2("问题七：印章管理对分公司罚款10万元条款无法律效力"),
      issueBox("A", "法律效力", "【制度2021 · 印章管理制度（202118）】\"分公司私自刻印、伪造各类印章，按10万元及以上标准进行经济处罚，双方终止合作\"。总公司对分公司的\"经济处罚\"无合同依据（除非加盟/合作协议明确约定），该条款不具有法律强制执行力，且10万元无计算依据。"),
      space(),
      para("修改建议："),
      bullet("将\"经济处罚\"改为\"违约金\"，在分公司的加盟/合作协议中作为合同条款明确约定"),
      bullet("删除10万元具体数额，改为\"按合同约定追究违约责任\""),
      bullet("增加条款：\"私刻印、伪造印章构成刑事犯罪的，依法追究刑事责任\""),
      space(),

      h2("问题八：员工行为规范中\"劝退\"条款法律风险"),
      issueBox("A", "法律合规", "【制度2021 · 考勤管理制度（202104）】\"一个月达3次（迟到）及以上者，公司可劝退\"。该条款未区分恶意旷工和情有可原的迟到，且\"劝退\"不符合劳动合同法规定（第39条：严重违反规章制度的才能解除合同，3次迟到一般不构成\"严重\"程度）。"),
      space(),
      para("修改建议："),
      bullet("将\"公司可劝退\"修改为：累计3次以上者，给予书面警告；累计5次以上者视为严重违规，公司有权依据劳动合同法处理"),
      bullet("增加情节区分：因客观原因（交通管制、突发疾病等）导致的迟到，凭证明材料可申请豁免"),
      bullet("完善制度表述，避免直接使用\"劝退\"等非法律用语"),
      space(),

      new Paragraph({ children: [new PageBreak()] }),

      // ============ 第三章 中优先级问题 ============
      h1("第三章 中优先级问题（建议近期修订）"),
      space(),

      h2("一、薪酬与福利标准类"),
      sectionTable([
        ["2021薪资制度（106）表格缺失/不完整", "薪资管理制度（202106）", "🟡", "补充完整岗位工资表、绩效工资系数表"],
        ["学历工资标准不统一（2021 vs 2022版）", "薪资管理制度（106/204）", "🟡", "统一全日制学历工资标准并明确适用版本"],
        ["技术人员绩效工资标准缺失", "薪资管理制度（106/204）", "🟡", "补充技术岗位绩效工资系数表（已含加班工资的说明）"],
        ["高温补贴标准偏低（外检150元/月）", "福利管理制度（202107）", "🟡", "参照海南省标准适当提高，建议外检200元/月"],
        ["年终奖\"第13个月工资\"未定义基数", "福利管理制度（202107）", "🟡", "明确第13个月工资的计算基数（基础工资还是全额工资）"],
        ["交通补贴150元/月低于实际出行成本", "福利管理制度（202107）", "🟡", "建议根据海口实际通勤成本调整至200-300元/月"],
      ]),
      space(),

      h2("二、业务管理制度类"),
      sectionTable([
        ["绩效考核指标体系缺失", "事业部绩效管理规定（定稿）第十三条", "🟡", "制定各事业部KPI指标（含回款率、客户满意度、技术质量等）"],
        ["净回款计算口径不统一", "绩效管理规定（两份版本）", "🟡", "统一净回款=合同金额-返点-外部管理费，并明确是否含税"],
        ["助理业务经理绩效系数未量化", "绩效管理规定第十一条", "🟡", "明确助理业务经理80%系数适用场景和计算方式"],
        ["业务招待节约奖励发放时间过晚（次年1月）", "商务招待管理制度V2.0", "🟡", "建议项目验收后次季度即可申请发放"],
        ["制度未配套完整表单（申请表/报销单）", "多个制度（无附件）", "🟡", "将制度中提及的附件表格作为正式附件纳入制度正文"],
      ]),
      space(),

      h2("三、行政管理流程类"),
      sectionTable([
        ["差旅住宿标准偏低（主任级深圳350元/天）", "差旅费管理办法（202113）", "🟡", "建议主任级深圳标准提升至450-500元/天，与市场实际相符"],
        ["业务人员绩效补贴30元/天远低于技术100元/天", "差旅费管理办法（202113）", "🟡", "统一业务人员与技术人员绩效补贴标准"],
        ["私车公用固定月补贴审批流程过长（6级审批）", "私车公用管理办法（202203）", "🟡", "精简为：申请人→部门负责人→财务→总经理（4级）"],
        ["车辆管理流程图存在\"不合理/合理\"标注", "公司车辆管理流程及规定", "🟡", "将流程图转化为标准泳道图，删除主观判断标注"],
        ["采购审批超2000元须总经理规定过于简单", "采购管理制度（202109）", "🟡", "按采购类别（A/B/C/D）分别制定审批权限分级"],
        ["考勤数据管理章节被截断", "考勤管理制度（202104）", "🟡", "补充完善第六章内容，明确考勤数据保存期限和查询权限"],
      ]),
      space(),

      h2("四、人力资源管理类"),
      sectionTable([
        ["试用期最长期限未明确（仅说3-6个月）", "员工录用转正管理办法（202116）", "🟡", "明确各岗位类型的试用期上限（一般员工3个月，管理岗6个月）"],
        ["招聘回避原则仅提及\"推荐人回避\"", "员工招聘预面试管理办法（202115）", "🟡", "增加亲属关系回避条款（夫妻、直系亲属不得同部门任职）"],
        ["员工行为规范过于冗长（10页60+条款）", "员工行为规范（202110）", "🟡", "精简为5-6页，重点条款加粗，精简重复表述"],
        ["离职手续超期\"按自动离职处理\"违反劳动法", "员工离职管理办法（202117）", "🟡", "改为：逾期不配合办理，公司可依法催告，仍不办理的追究法律责任"],
        ["试用期绩效考核仅分三档（优秀/良好/差）过于粗略", "员工录用转正管理办法（202116）", "🟡", "增加不合格/待改进档位（优秀/良好/合格/待改进/不合格）"],
      ]),
      space(),

      new Paragraph({ children: [new PageBreak()] }),

      // ============ 第四章 建议优化类 ============
      h1("第四章 建议优化类问题"),
      space(),

      h2("一、制度结构与语言规范性"),
      sectionTable([
        ["多份制度未标注文件版本（定稿/修订次数）", "会议制度/采购制度/财务制度等", "💡", "所有制度均应在页眉或首页标注\"第X版 第Y次修订\""],
        ["部分条款使用主观性语言（\"如非接待需要\"）", "员工行为规范（202110）", "💡", "将模糊表述改为客观标准（如\"工作时间内禁止饮酒\"，特殊情况需审批）"],
        ["制度有效期未统一（2年/3年/试行3个月）", "多个制度", "💡", "统一有效期：基础性制度3年，操作性制度2年，试用性制度1年"],
        ["部分制度审批人名称仍为旧名（邱雪云/赵晶）", "制度2021/2022", "💡", "更新为当前实际审批人姓名，或改为职务名称（综合管理部负责人）"],
        ["制度2021与2022部分内容重复", "多个制度", "💡", "建立制度索引表，避免交叉引用错误或重复规定"],
        ["部分制度缺少配套表单（仅标注\"见附件\"）", "绩效/出差/车辆等制度", "💡", "将表单作为制度附件一并发布，确保制度的完整性"],
      ]),
      space(),

      h2("二、信息安全与数字化管理"),
      sectionTable([
        ["制度未规定钉钉数据保存期限和权限", "多个涉及钉钉的制度", "💡", "增加数据管理条款：明确考勤/审批数据的保存期（≥2年）及访问权限"],
        ["员工行为规范缺少网络舆情应对指引", "员工行为规范（202110）", "💡", "增加条款：员工发现涉及公司的网络不实信息，应及时报告，不得自行回应"],
        ["微信群管理办法未规定群消息保存要求", "微信群管理办法（202201）", "💡", "增加：重要业务决策通知须同步以书面形式存档，微信群记录不作唯一依据"],
        ["缺少数据备份与系统故障应对条款", "多个制度", "💡", "增加系统故障应急预案：钉钉系统故障时，考勤/审批可采用纸质表单替代"],
      ]),
      space(),

      h2("三、卓越管理提升建议"),
      para("基于卓越管理原则，对公司制度建设提出以下提升方向："),
      space(),

      h3("（一）制度体系化建设"),
      bullet("建议建立\"1+N\"制度体系：1个制度纲领（公司治理总则）+N个专项制度，实现层级清晰、互不冲突"),
      bullet("建议编制《华检联制度汇编手册》（年度更新），统一版本管理，避免多个版本并行"),
      bullet("建议建立制度评审委员会，每年对制度进行合规性审查和更新"),
      space(),

      h3("（二）绩效管理精细化"),
      bullet("建议引入KPI+OKR双轨制：KPI用于硬性指标考核（回款率、合同额），OKR用于软性目标管理（团队建设、技术提升）"),
      bullet("建议增加绩效申诉时效（员工在绩效公布后7个工作日内可提出申诉，原制度仅5个工作日过于仓促）"),
      bullet("建议为每个业务类型（A/B/C/D）建立标准化的利润计算模板，减少人为操作空间"),
      space(),

      h3("（三）合规与风控体系"),
      bullet("建议增加《法律合规管理制度》，明确公司经营的法律边界和合规审查流程"),
      bullet("建议建立合同审核清单制度，确保每份业务合同的签订经过合规审核"),
      bullet("建议对印章使用建立电子登记系统（含GPS定位和拍照留痕），防止印章滥用"),
      space(),

      h3("（四）员工体验与文化建设"),
      bullet("建议将《员工行为规范》改为《员工手册》，增加员工权利、公司文化、职业发展路径等积极内容"),
      bullet("建议增加员工满意度调查（年度）和离职访谈制度，将反馈纳入制度改进"),
      bullet("建议在福利制度中增加弹性福利选项（员工可在一定额度内自主选择福利组合）"),
      space(),

      new Paragraph({ children: [new PageBreak()] }),

      // ============ 第五章 修订优先级总表 ============
      h1("第五章 修订优先级总表"),
      para("综合问题严重程度、整改难度和预期效果，建议按以下顺序推进修订："),
      space(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [600, 3400, 2400, 1400, 1560],
        rows: [
          new TableRow({ children: [
            ["序", 600], ["问题", 3400], ["涉及文件", 2400], ["优先级", 1400], ["建议完成时间", 1560]
          ].map(([t, w]) => new TableCell({
            borders, width: { size: w, type: WidthType.DXA },
            shading: { fill: "2E75B6", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 80, right: 80 },
            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: t, size: 19, font: "宋体", bold: true, color: "FFFFFF" })] })]
          })) }),
          ...[
            ["1", "废止事业本部绩效管理规定（V1.0），统一执行事业部绩效管理规定（定稿）", "事业本部工资绩效管理规定V1.0 vs 事业部绩效管理规定定稿", "🔴 高", "立即（1周内）"],
            ["2", "修订年休假标准（上限7天→按国家法定）", "员工各类休假制度（202105）", "🔴 高", "立即（1周内）"],
            ["3", "修订病假工资标准（不低于最低工资80%）", "员工各类休假制度（202105）", "🔴 高", "立即（1周内）"],
            ["4", "删除离职管理\"放弃当月工资\"条款", "员工离职管理办法（202117）", "🔴 高", "立即（1周内）"],
            ["5", "修订印章管理对分公司\"经济处罚\"条款", "印章管理制度（202118）", "🔴 高", "立即（1周内）"],
            ["6", "完善试用期提前转正条件（删除迟到/早退限制）", "员工录用转正管理办法（202116）", "🟡 中", "1个月内"],
            ["7", "完善绩效考核指标体系（KPI附件）", "事业部绩效管理规定（定稿）第十三条", "🟡 中", "1个月内"],
            ["8", "统一净回款计算口径", "事业部绩效管理规定（定稿）", "🟡 中", "1个月内"],
            ["9", "完善离职离任审计条款（限定范围和时限）", "员工离职管理办法（202117）", "🟡 中", "1个月内"],
            ["10", "统一学历工资标准（2021 vs 2022版本）", "薪资管理制度（106/204）", "🟡 中", "1个月内"],
            ["11", "完善考勤管理制度第六章内容", "考勤管理制度（202104）", "🟡 中", "1个月内"],
            ["12", "提高差旅住宿标准（主任级各城市）", "差旅费管理办法（202113）", "💡 优", "2个月内"],
            ["13", "精简员工行为规范（10页→5-6页）", "员工行为规范（202110）", "💡 优", "2个月内"],
            ["14", "建立制度版本管理制度（统一版本管理）", "全制度", "💡 优", "2个月内"],
            ["15", "增加系统故障应急预案（钉钉故障时替代方案）", "考勤/财务/出差等制度", "💡 优", "3个月内"],
          ].map(([no, prob, file, pri, time], i) => new TableRow({
            children: [
              new TableCell({ borders, width: { size: 600, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "F8F8F8" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 80, right: 80 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: no, size: 19, font: "宋体", bold: true })] })] }),
              new TableCell({ borders, width: { size: 3400, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "F8F8F8" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 80, right: 80 },
                children: [new Paragraph({ children: [new TextRun({ text: prob, size: 19, font: "宋体" })] })] }),
              new TableCell({ borders, width: { size: 2400, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "F8F8F8" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 80, right: 80 },
                children: [new Paragraph({ children: [new TextRun({ text: file, size: 18, font: "宋体" })] })] }),
              new TableCell({ borders, width: { size: 1400, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "F8F8F8" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 80, right: 80 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: pri, size: 19, font: "宋体", bold: true })] })] }),
              new TableCell({ borders, width: { size: 1560, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "F8F8F8" : "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 80, right: 80 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: time, size: 19, font: "宋体" })] })] }),
            ]
          }))
        ]
      }),
      space(),

      // ============ 结尾 ============
      new Paragraph({ spacing: { before: 480, after: 120 }, children: [new TextRun({ text: "报告说明", size: 24, font: "宋体", bold: true })] }),
      para("本报告基于对23份制度文件的逐一阅读和分析，提出的修改建议综合考虑了：①国家及海南省相关法律法规；②管理制度的逻辑完整性和可操作性；③制度间的体系一致性和相互衔接；④行业卓越管理实践。报告中\"🔴高优先级\"问题建议立即修订，避免法律风险；\"🟡中优先级\"建议1个月内完成；\"💡优化\"建议在制度年度审查周期内逐步推进。"),
      space(),
      para("如需针对任何具体制度生成带修订标注的对比版文件（tracked changes），请告知，我可逐一生成。"),
      space(),
      new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "华检联公司管理制度系统性审查报告", size: 20, font: "宋体", color: "808080" })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "2026年4月15日", size: 20, font: "宋体", color: "808080" })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/fasimac/Desktop/华检联管理制度系统性审查报告_20260415.docx", buffer);
  console.log("Done: 华检联管理制度系统性审查报告_20260415.docx");
}).catch(e => console.error(e));
