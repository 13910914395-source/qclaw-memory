const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, 
        HeadingLevel, Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: { 
      document: { 
        run: { font: "宋体", size: 24 }
      } 
    },
    paragraphStyles: [
      { 
        id: "Heading1", 
        name: "Heading 1", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 36, bold: true, font: "黑体" },
        paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
      },
      { 
        id: "Heading2", 
        name: "Heading 2", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 28, bold: true, font: "黑体" },
        paragraph: { spacing: { before: 180, after: 180 } }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "numbers",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 480, hanging: 480 } } }
        }]
      },
      {
        reference: "subnumbers",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "(%1)",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 480 } } }
        }]
      }
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
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "华检联（海南）检测技术有限公司", size: 20, font: "宋体" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", size: 20, font: "宋体" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
            new TextRun({ text: " 页 共 ", size: 20, font: "宋体" }),
            new TextRun({ children: [PageNumber.TOTAL], size: 20 }),
            new TextRun({ text: " 页", size: 20, font: "宋体" })
          ]
        })]
      })
    },
    children: [
      // 文件抬头
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: "华检联（海南）检测技术有限公司文件", size: 32, bold: true, font: "宋体", color: "FF0000" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "华检联〔2026〕管003号", size: 24, font: "黑体", underline: {} })]
      }),
      new Paragraph({ children: [] }),
      
      // 标题
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 240, after: 360 },
        children: [new TextRun({ text: "关于考勤打卡及薪资扣除标准的管理规定", size: 36, bold: true, font: "黑体" })]
      }),
      
      // 主送
      new Paragraph({
        children: [new TextRun({ text: "全体员工：", bold: true })]
      }),
      new Paragraph({ children: [] }),
      
      // 前言
      new Paragraph({
        indent: { firstLine: 480 },
        children: [new TextRun("为进一步规范公司日常考勤秩序，严明工作纪律，统一打卡、迟到早退、漏打卡及事假薪资扣除规则，经公司研究决定，特制定本规定。")]
      }),
      new Paragraph({ children: [] }),
      
      // 一、漏打卡考勤扣款规则
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("一、补卡及漏打卡考勤规则")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "补卡机会：", bold: true }), new TextRun("员工每月享有三次补卡机会。漏打卡后应在3个工作日内提交补卡申请，逾期未申请的，按漏卡处理。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "补卡流程：", bold: true }), new TextRun("员工提交补卡申请→部门负责人审核→人事部门审批。审批通过后，该次漏卡不扣除薪资。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "漏卡认定：", bold: true }), new TextRun("员工上下班未完成打卡、且未在规定时限内完成补卡审批手续的，判定为漏卡。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "漏卡处罚：", bold: true }), new TextRun("超过每月三次补卡机会后的漏卡，单次漏卡扣除半天工资。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "特殊说明：", bold: true }), new TextRun("员工正常迟到、早退可正常打卡记录，不按漏卡论处，按迟到早退对应标准执行扣款。")]
      }),
      new Paragraph({ children: [] }),
      
      // 二、迟到、早退薪资扣除标准
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("二、迟到、早退薪资扣除标准")]
      }),
      new Paragraph({
        indent: { firstLine: 480 },
        children: [new TextRun("所有迟到、早退均以考勤系统记录时间为准，分四档执行扣款：")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "迟到、早退时长≤30分钟：", bold: true }), new TextRun("每次扣除50元；")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "30分钟＜迟到、早退时长≤1小时：", bold: true }), new TextRun("每次扣除100元；")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "1小时＜迟到、早退时长≤2小时：", bold: true }), new TextRun("按当日工资的1/4扣除；")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "迟到、早退时长＞2小时：", bold: true }), new TextRun("按当日工资的1/2扣除（半天工资）。")]
      }),
      new Paragraph({ children: [] }),
      
      // 三、事假请假及日工资计算规则
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("三、事假请假及日工资计算规则")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "请假流程：", bold: true }), new TextRun("员工申请事假须提前按公司流程提交请假审批，事假期间不计发当日工资。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "计算公式：", bold: true }), new TextRun("单日事假扣款 = 基础工资 ÷ 21.75。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "基础工资定义：", bold: true }), new TextRun("基础工资以员工本人工资条中列明的固定工资项目为准，具体包括但不限于基本工资、岗位工资、工龄工资等项目。")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "适用范围：", bold: true }), new TextRun("本计算公式适用于标准工时制员工。实行综合计算工时制或不定时工作制的员工，按相关法律法规执行。")]
      }),
      new Paragraph({ children: [] }),
      
      // 四、特殊情形处理
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("四、特殊情形处理")]
      }),
      new Paragraph({
        indent: { firstLine: 480 },
        children: [new TextRun("因以下原因导致无法正常打卡的，经核实后不按漏卡或迟到处理：")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("因公外出、出差；")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("考勤设备故障；")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("其他经部门负责人或人事部门认可的特殊情况。")]
      }),
      new Paragraph({ children: [] }),
      
      // 五、申诉机制
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("五、申诉机制")]
      }),
      new Paragraph({
        indent: { firstLine: 480 },
        children: [new TextRun("员工对考勤记录有异议的，可在收到考勤异常通知后5个工作日内向人事部门提出书面申诉，人事部门应在3个工作日内核实并书面反馈结果。")]
      }),
      new Paragraph({ children: [] }),
      
      // 六、补充说明
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("六、补充说明")]
      }),
      new Paragraph({
        indent: { firstLine: 480 },
        children: [new TextRun("请全体员工自觉遵守上下班打卡制度，合理规划出行时间，确有特殊情况请提前履行补卡、请假审批手续。")]
      }),
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      
      // 落款
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { before: 480 },
        children: [new TextRun({ text: "华检联（海南）检测技术有限公司", bold: true })]
      }),
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun("2026年7月15日")]
      }),
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      
      // 印发信息
      new Paragraph({
        border: { top: { style: "single", size: 6, color: "000000" } },
        spacing: { before: 240 },
        children: []
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "华检联（海南）检测技术有限公司综合管理部    ", size: 20 }),
          new TextRun({ text: "2026年7月15日印发", size: 20 })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/fasimac/Downloads/考勤打卡管理规定（修订版）.docx", buffer);
  console.log("文档已生成：/Users/fasimac/Downloads/考勤打卡管理规定（修订版）.docx");
});
