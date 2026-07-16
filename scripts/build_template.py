#!/usr/bin/env python3
"""One-time bootstrap: build templates/resume_style.docx with style definitions only.

Re-run this if you want to tweak the visual style (fonts, spacing, margins).
It always overwrites templates/resume_style.docx from scratch.
"""
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches, RGBColor

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "templates" / "resume_style.docx"

GRAY = RGBColor(0x40, 0x40, 0x40)
RULE_GRAY = RGBColor(0x60, 0x60, 0x60)


def add_style(styles, name, base, size, bold=False, italic=False, color=None,
              alignment=None, space_before=0, space_after=4, uppercase=False,
              keep_with_next=False):
    style = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles[base]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(size)
    font.bold = bold
    font.italic = italic
    if color is not None:
        font.color.rgb = color
    pf = style.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.keep_with_next = keep_with_next
    if alignment is not None:
        pf.alignment = alignment
    return style


def main() -> None:
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(4)

    add_style(doc.styles, "NameHeader", "Normal", 22, bold=True,
              alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, keep_with_next=True)

    add_style(doc.styles, "ContactLine", "Normal", 9.5, color=GRAY,
              alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    add_style(doc.styles, "Headline", "Normal", 12, bold=True,
              alignment=WD_ALIGN_PARAGRAPH.CENTER, color=GRAY, space_after=10)

    add_style(doc.styles, "SectionHeading", "Normal", 12, bold=True,
              space_before=10, space_after=4, keep_with_next=True)

    add_style(doc.styles, "JobTitle", "Normal", 11, bold=True,
              space_before=6, space_after=0, keep_with_next=True)

    add_style(doc.styles, "JobMeta", "Normal", 10, italic=True, color=GRAY,
              space_before=0, space_after=3, keep_with_next=True)

    bullet = add_style(doc.styles, "BulletList", "List Bullet", 10, space_after=2)
    bullet.paragraph_format.left_indent = Inches(0.25)

    add_style(doc.styles, "SkillCategory", "Normal", 10, bold=True, space_after=2)

    add_style(doc.styles, "PlainText", "Normal", 10.5, space_after=6)

    # Remove the default empty paragraph so the template has no stray content.
    body = doc.element.body
    for p in doc.paragraphs:
        body.remove(p._p)

    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(TEMPLATE_PATH)
    print(f"Wrote {TEMPLATE_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
