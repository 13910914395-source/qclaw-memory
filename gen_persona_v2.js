const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  LevelFormat, BorderStyle, WidthType, ShadingType, PageBreak,
  PageNumber, Header, Footer, Table, TableRow, TableCell,
  UnderlineType, LineRuleType
} = require('docx');
const fs = require('fs');

const FONT = "SimSun";
const COLOR_TITLE = "1F4E79";
const COLOR_ACCENT = "2E75B6";
const COLOR_TEXT = "262626";
const COLOR_GRAY = "595959";

// ─── helpers ────────────────────────────────────────────────────────────────

function gap(pt) {
  return new Paragraph({ spacing: { before: 0, after: 0 }, children: [] });
}

function divider(color = "2E75B6") {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color } },
    spacing: { before: 200, after: 200 },
    children: []
  });
}

function h1(text, emoji = "") {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 480, after: 200 },
    children: [new TextRun({
      text: emoji ? `${emoji}  ${text}` : text,
      font: FONT, size: 36, bold: true, color: COLOR_TITLE
    })]
  });
}

function h2(text, emoji = "") {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 320, after: 160 },
    children: [new TextRun({
      text: emoji ? `${emoji}  ${text}` : text,
      font: FONT, size: 28, bold: true, color: COLOR_ACCENT
    })]
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: {
      before: opts.spaceBefore ?? 100,
      after: opts.spaceAfter ?? 100,
      line: opts.line ?? 360,
      lineRule: LineRuleType.AUTO
    },
    alignment: opts.align ?? AlignmentType.LEFT,
    children: [new TextRun({
      text,
      font: FONT,
      size: opts.size ?? 21,
      bold: opts.bold ?? false,
      italics: opts.italic ?? false,
      color: opts.color ?? COLOR_TEXT,
    })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 60, after: 60, line: 320, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text, font: FONT, size: 21, color: COLOR_TEXT })]
  });
}

function timeline(date, event) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    indent: { left: 480 },
    children: [
      new TextRun({ text: date + "\u2003", font: FONT, size: 21, bold: true, color: COLOR_ACCENT }),
      new TextRun({ text: event, font: FONT, size: 21, color: COLOR_TEXT })
    ]
  });
}

function tagLine(text) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    shading: { fill: "DEEAF1", type: ShadingType.CLEAR },
    indent: { left: 480, right: 480 },
    children: [new TextRun({
      text: "\u25C6  " + text,
      font: FONT, size: 20, color: COLOR_TITLE
    })]
  });
}

function insightBox(label, text) {
  return new Paragraph({
    spacing: { before: 180, after: 180 },
    shading: { fill: "EBF3FB", type: ShadingType.CLEAR },
    border: { left: { style: BorderStyle.THICK, size: 16,