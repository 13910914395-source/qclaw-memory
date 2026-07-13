const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, 
        HeadingLevel, Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: { 
      document: { 
        run: { font: "微软雅黑", size: 24 }
      } 
    },
    paragraphStyles: [
      { 
        id: "Heading1", 
        name: "Heading 1", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 36, bold: true, font: "微软雅黑" },
        paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
      },
      { 
        id: "Heading2", 
        name: "Heading 2", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 28, bold: true, font: "微软雅黑" },
        paragraph: { spacing: { before: 180, after: 180 } }
      },
      { 
        id: "Heading3", 
        name: "Heading 3", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 24, bold: true, font: "微软雅黑" },
        paragraph: { spacing: { before: 120, after: 120 } }
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
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
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
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "考勤打卡管理规定审核意见", size: 18, color: "666666", font: "微软雅黑" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", size: 20, font: "微软雅黑" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
            new TextRun({ text: " 页", size: 20, font: "微软雅黑" })
          ]
        })]
      })
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("考勤打卡及薪资扣除标准管理规定")]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "审核意见书", size: 36, bold: true, font: "微软雅黑" })]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("文件信息")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "文件名：", bold: true }), new TextRun("【2026】管003关于考勤打卡及薪资扣除标准的管理规定.docx")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "审核日期：", bold: true }), new TextRun("2026年7月9日")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "发文单位：", bold: true }), new TextRun("华检联（海南）检测技术有限公司")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("一、总体评价")]
      }),
      new Paragraph({
        children: [new TextRun("该管理规定整体结构清晰，条款基本明确，主要涵盖漏打卡处理、迟到早退扣款、事假工资计算三大部分。经审核，制度内容基本合理，但存在部分条款表述不明确、扣款逻辑不一致等问题，建议完善后发布执行。")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("二、需要修改的问题")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（一）补卡规则需书面明确【重要】")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "原文：", bold: true }), new TextRun("无合规补卡审批手续")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("当前制度未明确每月补卡次数限制（实际执行为每月三次）")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("未说明补卡申请的时限要求和具体审批流程")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("员工可能因不了解规则而遭受不必要的扣款")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("在制度中增加补卡专条，明确以下内容：")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("每月享有三次补卡机会，超过三次的漏卡按制度处理")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("补卡申请应在漏卡发生后的3个工作日内提交")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("补卡审批流程：员工申请→部门负责人审核→人事部门审批")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（二）第一档迟到扣款标准缺失【重要】")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "原文：", bold: true }), new TextRun("迟到、早退时长≤1小时；按制度规定标准扣除")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("条款引用"制度规定标准"，但未明确具体是哪个制度、什么标准")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("执行依据不明确，可能导致争议和管理混乱")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("明确第一档扣款标准，建议分两档：")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("迟到、早退时长≤30分钟：每次扣除50元")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("30分钟＜时长≤1小时：每次扣除100元")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（三）扣款逻辑表述不一致【重要】")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "原文：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("1小时＜迟到、早退时长≤2小时：按当日全额工资的1/4扣除薪资")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("迟到、早退时长＞2小时：按半天工资扣除薪资")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun(""全额工资的1/4"与"半天工资"表述方式不统一")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("半天工资通常理解为全额工资的1/2，与前面的1/4表述逻辑不连贯")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("统一使用比例表述或统一使用时间表述，建议改为：")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("1小时＜时长≤2小时：按当日工资的1/4扣除")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("时长＞2小时：按当日工资的1/2扣除（或按半天工资扣除）")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（四）缺少申诉机制")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("员工对考勤记录有异议时，缺乏明确的申诉渠道和处理时限")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("可能引发劳资纠纷，不利于和谐劳动关系建设")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("增加申诉条款：员工对考勤记录有异议的，可在收到考勤异常通知后5个工作日内向人事部门提出书面申诉，人事部门应在3个工作日内核实并书面反馈结果。")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（五）缺少特殊情形处理")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("未规定因公外出、出差、考勤设备故障等非本人原因导致的打卡异常如何处理")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("实际执行中可能产生争议")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("增加特殊情形条款：因公外出、出差、考勤设备故障等非本人原因导致的打卡异常，经部门负责人或人事部门核实后，不按漏卡或迟到处理。")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（六）生效日期表述不规范")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "原文：", bold: true }), new TextRun("自2026年7月起按以下标准执行")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "问题分析：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun(""7月起"表述模糊，未明确具体生效日期")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("可能导致执行混乱，影响制度严肃性")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "修改建议：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("改为明确日期表述，如"本规定自2026年7月15日起执行"或"本规定自发布之日起执行"。")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("三、建议完善的内容")]
      }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（一）基础工资定义优化")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "原文：", bold: true }), new TextRun("基础工资定义：包含基本工资、学历工资、岗级工资、工龄工资、职务工资")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "建议：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("部分员工可能没有"学历工资"或"职务工资"项目，定义过于具体可能导致争议")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("建议改为：基础工资以员工本人工资条中列明的固定工资项目为准，具体包括但不限于基本工资、岗位工资、工龄工资等项目")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("（二）格式规范建议")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "文号格式：", bold: true }), new TextRun("建议使用六角括号"〔〕"，即"华检联〔2026〕管003号"")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "条款编号：", bold: true }), new TextRun("建议统一使用"一、（一）、1."的层级编号格式")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun({ text: "标点符号：", bold: true }), new TextRun("注意中英文标点混用问题，统一使用中文标点")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("四、法律合规提示")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({ text: "扣款总额限制：", bold: true }),
          new TextRun("根据《工资支付暂行规定》，因劳动者本人原因给用人单位造成经济损失的，每月扣除金额不得超过当月工资的20%，且扣除后剩余工资不得低于当地最低工资标准")
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({ text: "民主程序：", bold: true }),
          new TextRun("建议按照《劳动合同法》第四条规定，规章制度应经职工代表大会或全体职工讨论，并与工会或职工代表平等协商确定")
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({ text: "公示告知：", bold: true }),
          new TextRun("新制度执行前应当告知员工，建议组织培训或会议宣贯，并要求员工签字确认")
        ]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("五、修改优先级建议")]
      }),
      new Paragraph({
        children: [new TextRun({ text: "必须修改（影响制度执行）：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("明确补卡规则（补卡次数、时限、流程）")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("明确第一档迟到扣款标准")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("统一扣款表述逻辑")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("明确生效日期")]
      }),
      new Paragraph({ children: [] }),
      new Paragraph({
        children: [new TextRun({ text: "建议增加（完善制度）：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("增加申诉机制条款")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("增加特殊情形处理条款")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("优化基础工资定义")]
      }),
      new Paragraph({ children: [] }),
      new Paragraph({
        children: [new TextRun({ text: "建议完善（提升规范性）：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("规范文号格式和条款编号")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("完善民主程序和公示告知")]
      }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("六、总结")]
      }),
      new Paragraph({
        children: [new TextRun("该管理规定内容基本合理，扣款标准设置得当（特别是配合每月三次补卡机会）。主要问题集中在条款表述不够明确、部分执行标准缺失等方面。建议按上述修改意见完善后发布执行，并做好员工宣贯和签收确认工作。")]
      }),
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "审核人：QClaw", bold: true })]
      }),
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun("审核日期：2026年7月9日")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/fasimac/Downloads/考勤打卡管理规定审核意见.docx", buffer);
  console.log("文档已生成：/Users/fasimac/Downloads/考勤打卡管理规定审核意见.docx");
});
