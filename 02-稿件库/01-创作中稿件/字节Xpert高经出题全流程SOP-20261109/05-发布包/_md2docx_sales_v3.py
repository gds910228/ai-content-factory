# -*- coding: utf-8 -*-
"""付费版-飞书Markdown.md -> 付费版-飞书导入.docx（图片内嵌，飞书导入Word即带图）
用法：在 05-发布包 目录下运行  python _md2docx.py
图片打码覆盖 images/ 后重跑本脚本即可重新生成。"""
import re, os, sys
from urllib.parse import unquote
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.stdout.reconfigure(encoding='utf-8')
SRC, DST = '私域销售物料-闲鱼朋友圈微信话术.md', '私域销售物料-闲鱼朋友圈微信话术-v3.docx'

text = open(SRC, encoding='utf-8').read()
# 剔除管理员导入指引块（从标记行到其后的 ---）
text = re.sub(r'> \*\*【管理员导入指引[^\n]*\n(?:>[^\n]*\n)+\n---\n', '', text)

doc = Document()
# 全局字体：正文等线/微软雅黑
normal = doc.styles['Normal']
normal.font.name = 'Calibri'; normal.font.size = Pt(10.5)
normal.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2.2)

def set_ea(run, font='微软雅黑'):
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), font)

def shade(el_pr, color):
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:fill'), color)
    el_pr.append(shd)

def add_runs(p, s, base_size=None):
    for tok in re.split(r'(\*\*[^*]+\*\*|`[^`]+`|^[^*]+\*$)', s):
        if not tok: continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1]); r.font.name = 'Consolas'
            r.font.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            r.font.color.rgb = RGBColor(0xC7,0x25,0x4E)
        else:
            r = p.add_run(tok)
        set_ea(r)
        if base_size: r.font.size = Pt(base_size)

def heading(s, lvl):
    p = doc.add_heading('', level=lvl)
    r = p.add_run(re.sub(r'\*\*|`', '', s)); set_ea(r, '微软雅黑')
    for r in p.runs:
        r.font.color.rgb = RGBColor(0x1F,0x3A,0x5F); r.font.element.rPr.rFonts.set(qn('w:eastAsia'),'微软雅黑')
    return p

def para_shade(p, color):
    shade(p._p.get_or_add_pPr(), color)

lines = text.split('\n'); i = 0; n = len(lines)
prev_img = False
while i < n:
    line = lines[i]
    s = line.rstrip()
    if not s.strip():
        i += 1; continue
    # 图片
    m = re.match(r'^!\[\]\((images/[^)]+)\)', s)
    if m:
        path = unquote(m.group(1))
        if os.path.exists(path):
            doc.add_picture(path, width=Cm(15.0))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p = doc.add_paragraph(f'[缺图: {path}]')
        prev_img = True; i += 1; continue
    # 图注（图后紧跟的 *…* 行）
    if prev_img and re.match(r'^\*[^*].*\*$', s.strip()):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(s.strip().strip('*')); set_ea(r); r.italic = True
        r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x8C,0x8C,0x8C)
        prev_img = False; i += 1; continue
    prev_img = False
    # 分隔线
    if re.match(r'^-{3,}$', s.strip()):
        i += 1; continue
    # 标题
    m = re.match(r'^(#{1,4})\s+(.*)', s)
    if m:
        heading(m.group(2), len(m.group(1))); i += 1; continue
    # 代码块
    if s.strip().startswith('```'):
        i += 1; buf = []
        while i < n and not lines[i].strip().startswith('```'):
            buf.append(lines[i]); i += 1
        i += 1
        for bl in buf:
            p = doc.add_paragraph(); para_shade(p, 'F6F8FA')
            p.paragraph_format.left_indent = Cm(0.4)
            r = p.add_run(bl if bl else ' '); r.font.name='Consolas'; set_ea(r,'Consolas'); r.font.size = Pt(9)
        continue
    # 引用块（连续 > 行合并为若干段）
    if s.lstrip().startswith('>'):
        buf = []
        while i < n and lines[i].lstrip().startswith('>'):
            buf.append(lines[i].lstrip()[1:].lstrip()); i += 1
        for chunk in re.split(r'\n\s*\n', '\n'.join(buf)):
            for ln in chunk.split('\n'):
                if not ln.strip(): continue
                p = doc.add_paragraph(); para_shade(p, 'FFFBE6')
                p.paragraph_format.left_indent = Cm(0.4)
                add_runs(p, ln, base_size=10)
                for r in p.runs: r.font.color.rgb = RGBColor(0x5A,0x45,0x00)
        continue
    # 表格
    if s.lstrip().startswith('|'):
        rows = []
        while i < n and lines[i].lstrip().startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.match(r'^:?-+:?$', c) for c in cells):
                rows.append(cells)
            i += 1
        if rows:
            t = doc.add_table(rows=len(rows), cols=len(rows[0]))
            t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row in enumerate(rows):
                for ci in range(len(rows[0])):
                    cell = t.cell(ri, ci); cell.text = ''
                    p = cell.paragraphs[0]
                    add_runs(p, row[ci] if ci < len(row) else '', base_size=9.5)
                    if ri == 0:
                        shade(cell._tc.get_or_add_tcPr(), 'EAF1FB')
                        for r in p.runs: r.bold = True
        continue
    # 列表
    m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)', line)
    if m:
        indent = len(m.group(1)) // 2
        style = 'List Bullet' if m.group(2) in '-*' else 'List Number'
        p = doc.add_paragraph(style=style if indent == 0 else f'{style} {indent+1}')
        add_runs(p, m.group(3)); i += 1; continue
    # 普通段落
    p = doc.add_paragraph(); add_runs(p, s); i += 1

doc.save(DST)
# 校验
d2 = Document(DST)
print('docx 已生成:', DST, '| 内嵌图片:', len(d2.inline_shapes), '| 段落:', len(d2.paragraphs), '| 表格:', len(d2.tables), '| 大小:', os.path.getsize(DST)//1024, 'KB')
