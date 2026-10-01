"""
Script: generate_docx_report.py
Mục đích: Tự động lắp ráp và xuất bản tệp tin báo cáo đồ án Word (.docx) toàn diện
chuẩn học thuật với độ dài 40-45 trang, chuẩn OpenXML 100% không lỗi định dạng.
"""

import os
import sys

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thêm thư mục scripts vào đường dẫn import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Import các phân hệ chương
from report_data.frontmatter import build_frontmatter
from report_data.chapter1 import build_chapter1
from report_data.chapter2 import build_chapter2
from report_data.chapter3 import build_chapter3
from report_data.chapter4 import build_chapter4
from report_data.chapter5 import build_chapter5
from report_data.chapter6_and_refs import build_chapter6_and_refs


def set_cell_background(cell, hex_color):
    """Thiết lập màu nền chuẩn OpenXML có đầy đủ thuộc tính val, color, fill."""
    tcPr = cell._tc.get_or_add_tcPr()
    # Xóa thẻ shd cũ nếu đã tồn tại để tránh vi phạm cấu trúc XML
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>')
    tcPr.append(shading_elm)


def set_table_margins(tbl, top=100, bottom=100, left=140, right=140):
    """Thiết lập lề đệm ô ở cấp độ bảng (tblCellMar) chuẩn OpenXML ECMA-376."""
    tblPr = tbl._tbl.tblPr
    cell_mar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tblCellMar>'
    )
    tblPr.append(cell_mar)


def add_custom_heading(doc, text, level, space_before=12, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.bold = True

    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0, 51, 102)
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(20, 40, 80)
    elif level == 3:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.font.size = Pt(13)
        run.italic = True
        run.font.color.rgb = RGBColor(40, 40, 40)
    return p


def add_body_paragraph(doc, text, indent=True, space_after=6, line_spacing=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.4)

    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(30, 30, 30)
    return p


def add_callout_box(doc, text, title="GHI CHÚ HỌC THUẬT & ĐIỂM SÁNG TẠO"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_margins(tbl, top=140, bottom=140, left=180, right=180)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}:\n")
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(12)
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(0, 70, 140)

    run_c = p.add_run(text)
    run_c.font.name = "Times New Roman"
    run_c.font.size = Pt(12)
    run_c.italic = True
    run_c.font.color.rgb = RGBColor(40, 40, 40)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(4)


def add_code_snippet(doc, code_str, caption=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_margins(tbl, top=100, bottom=100, left=140, right=140)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15

    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(33, 37, 41)

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.italic = True


def add_styled_table(doc, headers, data, caption=""):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11.5)
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(0, 51, 102)

    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_margins(tbl, top=80, bottom=80, left=120, right=120)

    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1F497D")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_col = "F2F5F8" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            if bg_col != "FFFFFF":
                set_cell_background(row_cells[col_idx], bg_col)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(4)
    p_spacer.paragraph_format.space_after = Pt(6)


def add_image(doc, img_path, caption="", width_inches=5.8):
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.italic = True


def main():
    print("[*] Đang khởi tạo đối tượng tài liệu Word và thiết lập trang in...")
    doc = Document()

    # Cấu hình lề trang chuẩn luận văn học thuật:
    # Lề trái: 3.0 cm (để đóng gáy sách), Lề phải: 2.0 cm, Lề trên: 2.5 cm, Lề dưới: 2.5 cm
    for section in doc.sections:
        section.top_margin = Inches(0.98)     # ~2.5 cm
        section.bottom_margin = Inches(0.98)  # ~2.5 cm
        section.left_margin = Inches(1.18)    # ~3.0 cm
        section.right_margin = Inches(0.79)   # ~2.0 cm

    helpers = {
        "add_custom_heading": add_custom_heading,
        "add_body_paragraph": add_body_paragraph,
        "add_callout_box": add_callout_box,
        "add_code_snippet": add_code_snippet,
        "add_styled_table": add_styled_table,
        "add_image": add_image,
    }

    print("[*] Đang sinh Phần đầu (Trang bìa, Lời cam đoan, Abstract, Danh mục)...")
    build_frontmatter(doc, helpers)

    print("[*] Đang sinh Chương 1: Tổng quan và Đặt vấn đề...")
    build_chapter1(doc, helpers)

    print("[*] Đang sinh Chương 2: Cơ sở Lý thuyết và Khung Công nghệ...")
    build_chapter2(doc, helpers)

    print("[*] Đang sinh Chương 3: Thiết kế Kiến trúc Hệ thống Mini-SOC...")
    build_chapter3(doc, helpers)

    print("[*] Đang sinh Chương 4: Hiện thực hóa và Mã nguồn các Phân hệ...")
    build_chapter4(doc, helpers)

    print("[*] Đang sinh Chương 5: Thử nghiệm Thực tế, Đánh giá và Phân tích...")
    build_chapter5(doc, helpers)

    print("[*] Đang sinh Chương 6: Kết luận, Hướng phát triển và Tài liệu tham khảo...")
    build_chapter6_and_refs(doc, helpers)

    output_dir = "./reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "BAO_CAO_DO_AN_ACTIVE_DEFENSE_SOAR_40_TRANG.docx")

    print(f"[*] Đang lưu tệp Word hoàn chỉnh vào: {output_path}...")
    doc.save(output_path)
    print(f"[+] THÀNH CÔNG RỰC RỠ! Đã tạo xong báo cáo đồ án Word chuẩn OpenXML tại: {output_path}")


if __name__ == "__main__":
    main()
