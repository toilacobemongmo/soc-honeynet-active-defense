"""
Script: generate_md_report.py
Mục đích: Xuất bản toàn bộ nội dung đồ án 40 trang ra định dạng Markdown (.md) chuẩn GitHub / Academic,
giúp người dùng có thể xem trước tức thì ngay trong trình soạn thảo, in ấn hoặc chuyển đổi sang PDF.
"""

import os
import sys

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def docx_to_md_builder():
    from report_data.frontmatter import build_frontmatter
    from report_data.chapter1 import build_chapter1
    from report_data.chapter2 import build_chapter2
    from report_data.chapter3 import build_chapter3
    from report_data.chapter4 import build_chapter4
    from report_data.chapter5 import build_chapter5
    from report_data.chapter6_and_refs import build_chapter6_and_refs

    md_lines = []

    class DummyDoc:
        def __init__(self):
            self.paragraphs = []
            self.tables = []
            self.sections = []

        def add_paragraph(self):
            p = DummyParagraph()
            self.paragraphs.append(p)
            return p

        def add_table(self, rows, cols):
            t = DummyTable(rows, cols)
            self.tables.append(t)
            return t

        def add_page_break(self):
            md_lines.append("\n---\n")

    class DummyParagraph:
        def __init__(self):
            self.runs = []
            self.alignment = None
            self.paragraph_format = DummyFormat()

        def add_run(self, text=""):
            r = DummyRun(text)
            self.runs.append(r)
            return r

        @property
        def text(self):
            return "".join(r.text for r in self.runs)

    class DummyRun:
        def __init__(self, text=""):
            self.text = text
            self.font = DummyFont()
            self.bold = False
            self.italic = False

        def add_picture(self, path, width=None):
            rel_path = os.path.basename(path)
            md_lines.append(f"\n![Biểu đồ minh họa](./images/{rel_path})\n")

    class DummyFont:
        def __init__(self):
            self.name = "Times New Roman"
            self.size = None
            self.color = DummyColor()

    class DummyColor:
        def __init__(self):
            self.rgb = None

    class DummyFormat:
        def __init__(self):
            self.space_before = 0
            self.space_after = 0
            self.line_spacing = 1.5
            self.left_indent = 0
            self.first_line_indent = 0
            self.keep_with_next = False

    class DummyTable:
        def __init__(self, rows, cols):
            self.rows = [DummyRow(cols) for _ in range(rows)]
            self.alignment = None
            self.style = None
            self._tbl = DummyTbl()

        def cell(self, r, c):
            return self.rows[r].cells[c]

    class DummyRow:
        def __init__(self, cols):
            self.cells = [DummyCell() for _ in range(cols)]

    class DummyCell:
        def __init__(self):
            self.paragraphs = [DummyParagraph()]
            self.text = ""
            self._tc = DummyTc()

    class DummyTbl:
        def __init__(self):
            self.tblPr = None

    class DummyTc:
        def __init__(self):
            pass
        def get_or_add_tcPr(self):
            return []

    # Mock helpers
    def add_custom_heading(doc, text, level, **kwargs):
        prefix = "#" * level
        md_lines.append(f"\n{prefix} {text}\n")
        p = doc.add_paragraph()
        p.add_run(text)
        return p

    def add_body_paragraph(doc, text, **kwargs):
        md_lines.append(f"\n{text}\n")
        p = doc.add_paragraph()
        p.add_run(text)
        return p

    def add_callout_box(doc, text, title="GHI CHÚ HỌC THUẬT & ĐIỂM SÁNG TẠO"):
        md_lines.append(f"\n> [!NOTE]\n> **📌 {title}**\n> {text}\n")
        t = doc.add_table(1, 1)
        t.cell(0, 0).paragraphs[0].add_run(text)

    def add_code_snippet(doc, code_str, caption=""):
        cap = f"\n*{caption}*\n" if caption else ""
        md_lines.append(f"\n```python\n{code_str}\n```{cap}\n")
        t = doc.add_table(1, 1)
        t.cell(0, 0).paragraphs[0].add_run(code_str)

    def add_styled_table(doc, headers, data, caption=""):
        if caption:
            md_lines.append(f"\n**{caption}**\n")
        header_line = "| " + " | ".join(headers) + " |"
        sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
        md_lines.append(header_line)
        md_lines.append(sep_line)
        for row in data:
            row_line = "| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |"
            md_lines.append(row_line)
        md_lines.append("\n")
        t = doc.add_table(len(data) + 1, len(headers))

    def add_image(doc, img_path, caption="", width_inches=5.8):
        rel = os.path.basename(img_path)
        cap = f"\n*{caption}*\n" if caption else ""
        md_lines.append(f"\n![{caption}](./images/{rel}){cap}\n")

    helpers = {
        "add_custom_heading": add_custom_heading,
        "add_body_paragraph": add_body_paragraph,
        "add_callout_box": add_callout_box,
        "add_code_snippet": add_code_snippet,
        "add_styled_table": add_styled_table,
        "add_image": add_image,
    }

    dummy = DummyDoc()
    build_frontmatter(dummy, helpers)
    build_chapter1(dummy, helpers)
    build_chapter2(dummy, helpers)
    build_chapter3(dummy, helpers)
    build_chapter4(dummy, helpers)
    build_chapter5(dummy, helpers)
    build_chapter6_and_refs(dummy, helpers)

    out_md = "./reports/BAO_CAO_DO_AN_ACTIVE_DEFENSE_SOAR_40_TRANG.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[+] Đã xuất bản song song bản Markdown tại: {out_md}")


if __name__ == "__main__":
    docx_to_md_builder()
