#!/usr/bin/env python3
"""สร้าง reference.docx ภาษาไทยสำหรับ pandoc  ใช้: python3 make_thai_ref.py [base-ref.docx] [thai-ref.docx]"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

FONT = "TH Sarabun New"
BODY_PT = 16
INDENT_CM = 2.5
SIZES = {"Title": 20, "Heading 1": 18, "Heading 2": 16, "Heading 3": 16}
BODY = {"Body Text", "First Paragraph"}
AFTER_SZCS = ("w:highlight", "w:u", "w:effect", "w:bdr", "w:shd", "w:fitText",
              "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang",
              "w:eastAsianLayout", "w:specVanish", "w:oMath")
AFTER_LANG = ("w:eastAsianLayout", "w:specVanish", "w:oMath")

def set_child(rpr, tag, successors, **attrs):
    el = rpr.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        rpr.insert_element_before(el, *successors)
    for k, v in attrs.items():
        el.set(qn(k), v)

import sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "base-ref.docx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "thai-ref.docx"
doc = Document(BASE)
for st in doc.styles:
    if st.type not in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER):
        continue
    rpr = st.element.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rf.attrib.pop(qn(a), None)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), FONT)
    pt = SIZES.get(st.name, BODY_PT if st.type == WD_STYLE_TYPE.PARAGRAPH else None)
    if pt:
        st.font.size = Pt(pt)
        set_child(rpr, "w:szCs", AFTER_SZCS, **{"w:val": str(pt * 2)})
    set_child(rpr, "w:lang", AFTER_LANG, **{"w:val": "en-US", "w:bidi": "th-TH"})
    if st.name in SIZES:
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
    if st.type == WD_STYLE_TYPE.PARAGRAPH:
        pf = st.paragraph_format
        if st.name in BODY:
            pf.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
            pf.first_line_indent = Cm(INDENT_CM)
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
        else:
            pf.first_line_indent = Cm(0)   # หัวข้อ ตาราง รายการ ไม่ย่อหน้า
for s in doc.sections:
    s.left_margin, s.right_margin = Cm(3), Cm(2)
    s.top_margin, s.bottom_margin = Cm(2.5), Cm(2)
doc.save(OUT)
print("saved", OUT)
