# -*- coding: utf-8 -*-
"""
Bộ 4 sơ đồ phong cách Đồ họa An toàn thông tin (Cybersecurity Infographic)
Chuẩn quốc tế giống như báo cáo của Cloudflare, Palo Alto, CyStack, Viettel IDC.
- Đồ họa trực quan (Icon máy chủ, laptop hacker, proxy, khiên chắn, chip trạng thái)
- Đánh số bước 1, 2, 3, 4 rõ ràng, nhìn lướt qua 3 giây là hiểu toàn bộ nguyên lý
- Màu sắc tương phản chuẩn SOC: Đỏ (Tấn công), Tím/Xanh (Honeypot & Phân tích), Xanh lục (Phòng thủ SOAR)
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'Segoe UI', 'DejaVu Sans', 'Arial'

# ==============================================================================
# HÀM BỔ TRỢ ĐỒ HỌA (VECTOR DRAWING HELPERS)
# ==============================================================================
def draw_card(ax, x, y, w, h, bg="#FFFFFF", border="#CBD5E1", border_w=1.5, shadow=True, radius=1.0, z=1):
    """Vẽ thẻ chứa nội dung có bóng đổ mờ phong cách hiện đại"""
    if shadow:
        s_rect = FancyBboxPatch(
            (x + 0.35, y - 0.35), w, h,
            boxstyle=f"round,pad=0.0,rounding_size={radius}",
            facecolor="#0F172A", alpha=0.06, edgecolor="none", zorder=z
        )
        ax.add_patch(s_rect)
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, lw=border_w, zorder=z+1
    )
    ax.add_patch(card)
    return card

def draw_badge(ax, cx, cy, text, bg="#DC2626", fg="#FFFFFF", radius=1.8, z=8):
    """Vẽ huy hiệu số thứ tự tròn (1, 2, 3...) nổi bật"""
    circle = Circle((cx, cy), radius, facecolor=bg, edgecolor="#FFFFFF", lw=2.0, zorder=z)
    ax.add_patch(circle)
    ax.text(cx, cy, text, fontsize=11, fontweight='bold', color=fg, ha='center', va='center', zorder=z+2)

def draw_chip(ax, x, y, text, bg="#F1F5F9", fg="#334155", fontsize=8.5, border=None, z=4):
    """Vẽ chip trạng thái (Badge con)"""
    w = len(text) * 0.58 + 2.4
    h = 2.4
    chip = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.2,rounding_size=1.0",
        facecolor=bg, edgecolor=border if border else bg, lw=1.0, zorder=z
    )
    ax.add_patch(chip)
    ax.text(x, y, text, fontsize=fontsize, fontweight='bold', color=fg, ha='center', va='center', zorder=z+6)

def draw_laptop_icon(ax, cx, cy, scale=1.0, color="#EF4444", z=5):
    """Vẽ biểu tượng Laptop Kẻ tấn công"""
    screen = FancyBboxPatch((cx - 2.5*scale, cy - 0.5*scale), 5.0*scale, 3.4*scale,
                            boxstyle="round,pad=0.1,rounding_size=0.4",
                            facecolor="#1E293B", edgecolor=color, lw=2.0*scale, zorder=z)
    ax.add_patch(screen)
    in_scr = patches.Rectangle((cx - 2.1*scale, cy - 0.1*scale), 4.2*scale, 2.6*scale,
                               facecolor=color, alpha=0.2, zorder=z+1)
    ax.add_patch(in_scr)
    ax.text(cx - 1.2*scale, cy + 1.1*scale, ">_", fontsize=9*scale, fontweight='bold', color=color, zorder=z+2)
    base = Polygon([
        [cx - 3.4*scale, cy - 1.6*scale],
        [cx + 3.4*scale, cy - 1.6*scale],
        [cx + 2.8*scale, cy - 0.6*scale],
        [cx - 2.8*scale, cy - 0.6*scale]
    ], facecolor="#334155", edgecolor=color, lw=1.5*scale, zorder=z)
    ax.add_patch(base)

def draw_server_icon(ax, cx, cy, scale=1.0, color="#2563EB", z=5):
    """Vẽ biểu tượng Máy chủ Server Racks"""
    for i in range(3):
        sy = cy - 1.5*scale + (i * 1.5*scale)
        blade = FancyBboxPatch((cx - 2.8*scale, sy), 5.6*scale, 1.1*scale,
                               boxstyle="round,pad=0.08,rounding_size=0.2",
                               facecolor="#0F172A", edgecolor=color, lw=1.5*scale, zorder=z)
        ax.add_patch(blade)
        for sl in range(3):
            slot = patches.Rectangle((cx - 2.2*scale + (sl * 0.9*scale), sy + 0.3*scale), 0.6*scale, 0.5*scale,
                                     facecolor="#334155", zorder=z+1)
            ax.add_patch(slot)
        led1 = Circle((cx + 1.5*scale, sy + 0.55*scale), 0.18*scale, facecolor="#10B981", zorder=z+1)
        led2 = Circle((cx + 2.1*scale, sy + 0.55*scale), 0.18*scale, facecolor=color, zorder=z+1)
        ax.add_patch(led1)
        ax.add_patch(led2)

def draw_shield_icon(ax, cx, cy, scale=1.0, color="#10B981", z=5):
    """Vẽ biểu tượng Khiên phòng thủ an ninh chất lượng cao với dấu tích bảo vệ"""
    p1 = [cx, cy + 2.4*scale]
    p2 = [cx + 2.2*scale, cy + 1.6*scale]
    p3 = [cx + 2.0*scale, cy - 0.6*scale]
    p4 = [cx, cy - 2.4*scale]
    p5 = [cx - 2.0*scale, cy - 0.6*scale]
    p6 = [cx - 2.2*scale, cy + 1.6*scale]
    shield = Polygon([p1, p2, p3, p4, p5, p6], facecolor="#ECFDF5", edgecolor=color, lw=2.2*scale, zorder=z)
    ax.add_patch(shield)
    # Dấu checkmark bảo vệ
    ax.plot([cx - 0.9*scale, cx - 0.2*scale, cx + 1.0*scale],
            [cy - 0.1*scale, cy - 0.8*scale, cy + 0.8*scale],
            color=color, lw=2.5*scale, solid_capstyle='round', zorder=z+2)


# ==============================================================================
# SƠ ĐỒ 1: CƠ CHẾ CỬA SỔ THỜI GIAN TRƯỢT (SLIDING TIME WINDOW INFOGRAPHIC)
# ==============================================================================
def draw_sliding_window_infographic():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Banner
    draw_card(ax, 3, 86, 94, 11, bg="#0F172A", border="#1E293B", shadow=True, radius=1.0, z=1)
    draw_chip(ax, 16, 93.5, "GIẢI THUẬT PHÁT HIỆN BRUTE-FORCE", bg="#EF4444", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(3, 90, "   CƠ CHẾ CỬA SỔ THỜI GIAN TRƯỢT (SLIDING TIME WINDOW)", 
            fontsize=15, fontweight='bold', color='#FFFFFF', va='center', zorder=10)
    ax.text(3, 87.5, "   Phát hiện tấn công dò quét SSH (T1110.001) trong correlation_engine.py • Thu hồi bộ đệm deque tự động", 
            fontsize=9.2, color='#94A3B8', va='center', zorder=10)

    # KHỐI 1 (BÊN TRÁI): KẺ TẤN CÔNG
    draw_card(ax, 4, 28, 20, 54, bg="#FFFFFF", border="#FECACA", shadow=True, z=1)
    draw_laptop_icon(ax, 14, 71, scale=1.2, color="#DC2626", z=5)
    ax.text(14, 63, "Attacker / Botnet", fontsize=11, fontweight='bold', color='#991B1B', ha='center', zorder=10)
    ax.text(14, 60, "IP: 185.220.101.5", fontsize=9, color='#64748B', ha='center', fontfamily='Consolas', zorder=10)
    
    draw_chip(ax, 14, 53.5, "Hành vi tấn công", bg="#FEE2E2", fg="#991B1B", z=4)
    ax.text(14, 43, "• Gửi SSH Password liên tục\n• Mỗi lần sai sinh event:\n  cowrie.login.failed\n• Khoảng cách: 8-15s / lần\n• Dò quét âm ỉ né IPS", 
            fontsize=8.5, color='#334155', ha='center', linespacing=1.45, zorder=10)
    
    # Mũi tên từ Attacker vào dòng thời gian
    ax.annotate("", xy=(26, 52), xytext=(24, 52),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.5, mutation_scale=16), zorder=5)

    # KHỐI 2 (TRUNG TÂM): BỘ ĐỆM HÀNG ĐỢI ĐỘNG (DEQUE STREAM)
    draw_card(ax, 26, 24, 48, 58, bg="#FFFFFF", border="#CBD5E1", shadow=True, z=1)
    ax.text(50, 77.5, "BỘ ĐỆM HÀNG ĐỢI ĐỘNG (DEQUE STREAM)", fontsize=11.5, fontweight='bold', color='#0F172A', ha='center', zorder=10)
    ax.text(50, 74.5, "Mỗi IP sở hữu 1 hàng đợi riêng lưu trữ dấu thời gian (timestamps)", fontsize=8.8, color='#64748B', ha='center', zorder=10)

    # Trục thời gian chính
    ax.plot([29, 68], [52, 52], color="#94A3B8", lw=3.0, zorder=3)
    ax.annotate("", xy=(68.5, 52), xytext=(66.5, 52),
                arrowprops=dict(arrowstyle="-|>", color="#475569", lw=3.0, mutation_scale=16), zorder=4)
    ax.text(54.5, 38.5, "Chiều tăng dần của dòng thời gian (t)  --->", fontsize=8.2, fontweight='bold', color="#2563EB", ha='center', zorder=10)

    # Vùng 1: Quá hạn > 60s
    waste_box = FancyBboxPatch((28.5, 36), 10.5, 32, boxstyle="round,pad=0.2,rounding_size=0.8",
                               facecolor="#F1F5F9", edgecolor="#CBD5E1", linestyle="--", lw=1.5, zorder=2)
    ax.add_patch(waste_box)
    draw_chip(ax, 33.7, 64, "BỊ LOẠI BỎ", bg="#E2E8F0", fg="#475569", fontsize=7.5, z=4)
    ax.text(33.7, 40, "Quá hạn > 60s\npopleft() xóa", fontsize=8, color="#64748B", ha='center', style='italic', zorder=10)

    # Các điểm mốc t1, t2
    for px, t_label, t_sub in [(31.5, "t1", "10:00:05"), (36.0, "t2", "10:00:18")]:
        c = Circle((px, 52), 1.2, facecolor="#94A3B8", edgecolor="#FFFFFF", lw=1.5, zorder=5)
        ax.add_patch(c)
        ax.text(px, 55.5, t_label, fontsize=9, fontweight='bold', color="#64748B", ha='center', zorder=10)
        ax.text(px, 46.5, t_sub, fontsize=7.5, color="#94A3B8", ha='center', fontfamily='Consolas', zorder=10)

    # Vùng 2: KHUNG CỬA SỔ TRƯỢT W = 60 GIÂY
    win_box = FancyBboxPatch((40.5, 35), 29.5, 34, boxstyle="round,pad=0.4,rounding_size=1.0",
                             facecolor="#EFF6FF", edgecolor="#2563EB", lw=2.2, linestyle="-", zorder=2)
    ax.add_patch(win_box)
    draw_chip(ax, 55.2, 65, "KHUNG CỬA SỔ HIỆN TẠI (W = 60 GIÂY)", bg="#2563EB", fg="#FFFFFF", fontsize=8.5, z=4)
    
    # 5 điểm mốc sự kiện trong cửa sổ: t3, t4, t5, t6, t7
    points = [
        (43.5, "t3", "10:01:05", "#3B82F6"),
        (48.5, "t4", "10:01:14", "#3B82F6"),
        (53.5, "t5", "10:01:25", "#3B82F6"),
        (58.5, "t6", "10:01:38", "#3B82F6"),
        (64.5, "t7", "10:01:52", "#DC2626")
    ]
    for px, t_label, t_sub, col in points:
        c = Circle((px, 52), 1.35, facecolor=col, edgecolor="#FFFFFF", lw=2.0, zorder=5)
        ax.add_patch(c)
        ax.text(px, 55.5, t_label, fontsize=9.5, fontweight='bold', color=col, ha='center', zorder=10)
        ax.text(px, 46.5, t_sub, fontsize=7.2, color="#334155", ha='center', fontfamily='Consolas', zorder=10)

    # Nhãn số lượng đếm được
    draw_chip(ax, 55.2, 29, "TÍNH TOÁN: Count = 5 lần  >=  Ngưỡng Nguy hiểm (Threshold = 5)", 
              bg="#DC2626", fg="#FFFFFF", fontsize=8.8, z=4)

    # Mũi tên từ Cửa sổ trượt sang Khối SOAR
    ax.annotate("", xy=(77, 52), xytext=(72, 52),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.5, mutation_scale=16), zorder=5)

    # KHỐI 3 (BÊN PHẢI): PHẢN ỨNG SOAR ACTIVE DEFENSE
    draw_card(ax, 77, 28, 19, 54, bg="#FFFFFF", border="#A7F3D0", shadow=True, z=1)
    draw_shield_icon(ax, 86.5, 71, scale=1.1, color="#059669", z=5)
    ax.text(86.5, 63, "SOAR Phản xạ", fontsize=11.5, fontweight='bold', color='#065F46', ha='center', zorder=10)
    ax.text(86.5, 60, "Hành động phòng thủ chủ động", fontsize=8.2, color='#64748B', ha='center', zorder=10)

    # Thẻ chi tiết hành động
    sub_action = FancyBboxPatch((78.5, 31), 16, 25, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#F0FDF4", edgecolor="#86EFAC", lw=1.2, zorder=2)
    ax.add_patch(sub_action)
    ax.text(86.5, 52.5, "KÍCH HOẠT ALERT", fontsize=9.5, fontweight='bold', color='#15803D', ha='center', zorder=10)
    ax.text(86.5, 49.5, "MITRE ATT&CK T1110.001", fontsize=8.0, fontweight='bold', color='#DC2626', ha='center', zorder=10)
    ax.plot([80, 93], [47.5, 47.5], color='#86EFAC', lw=1.0, zorder=3)
    ax.text(86.5, 40, "1. Gửi lệnh NAT sang Tarpit\n2. Bóp nghẹt socket kết nối\n3. Bắn Telegram cho SOC\n4. Reset sạch bộ đệm deque", 
            fontsize=8.0, color='#1E293B', ha='center', linespacing=1.35, zorder=10)

    # Footer
    draw_card(ax, 4, 8, 92, 13, bg="#F8FAFC", border="#E2E8F0", shadow=False, z=1)
    ax.text(6, 17, "TỔNG KẾT NGUYÊN LÝ HOẠT ĐỘNG:", fontsize=9.2, fontweight='bold', color='#0F172A', zorder=10)
    ax.text(6, 12.5, "1. Tiết kiệm RAM: Khi có kết nối mới, vòng lặp `while deque and now - deque[0] > 60: deque.popleft()` loại bỏ ngay rác cũ.\n2. Chống Bypass: Hacker quét chậm cách 13 giây/lần vẫn bị gom đủ 5 lần trong 60s và kích hoạt bẫy Tarpit tức thì.", 
            fontsize=8.5, color='#475569', linespacing=1.4, zorder=10)

    out_file = os.path.join(OUTPUT_DIR, "01_sliding_time_window.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Hoàn thành Sơ đồ 1 (Infographic): {out_file}")


# ==============================================================================
# SƠ ĐỒ 2: LƯU ĐỒ GIẢI THUẬT ĐỘNG CƠ TƯƠNG QUAN (CORRELATION ENGINE INFOGRAPHIC)
# ==============================================================================
def draw_correlation_flowchart_infographic():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Banner
    draw_card(ax, 3, 86, 94, 11, bg="#0F172A", border="#1E293B", shadow=True, radius=1.0, z=1)
    draw_chip(ax, 15, 93.5, "KIẾN TRÚC XỬ LÝ SỰ KIỆN JSON", bg="#7C3AED", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(3, 90, "   LƯU ĐỒ GIẢI THUẬT ĐỘNG CƠ TƯƠNG QUAN (CORRELATION ENGINE)", 
            fontsize=15, fontweight='bold', color='#FFFFFF', va='center', zorder=10)
    ax.text(3, 87.5, "   Phân loại sự kiện đa luồng từ Honeypot • Ánh xạ MITRE ATT&CK • Kích hoạt phản xạ SOAR Active Defense", 
            fontsize=9.2, color='#94A3B8', va='center', zorder=10)

    # KHỐI START
    draw_card(ax, 34, 73, 32, 10, bg="#FFFFFF", border="#7C3AED", border_w=2.0, shadow=True, z=1)
    draw_chip(ax, 50, 80.5, "START: TIẾP NHẬN SỰ KIỆN", bg="#7C3AED", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(50, 76, "Gói tin JSON từ Cowrie Honeypot / Syslog\n{'eventid': ..., 'src_ip': '...', 'message': '...'}", 
            fontsize=8.0, color='#334155', ha='center', fontfamily='Consolas', zorder=10)

    # Mũi tên từ Start xuống Khối Phân luồng
    ax.annotate("", xy=(50, 68), xytext=(50, 73),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2.2, mutation_scale=14), zorder=5)

    # KHỐI ĐIỀU PHỐI TRUNG TÂM (DISPATCHER)
    draw_card(ax, 32, 58, 36, 10, bg="#F5F3FF", border="#8B5CF6", border_w=1.8, shadow=True, z=1)
    ax.text(50, 64.5, "BỘ PHÂN TÍCH eventid CỦA SỰ KIỆN", fontsize=10.5, fontweight='bold', color='#5B21B6', ha='center', zorder=10)
    ax.text(50, 61, "Trích xuất định danh hành vi và phân luồng tới 4 module chuyên trách", fontsize=8.2, color='#6D28D9', ha='center', zorder=10)

    # 4 NHÁNH PHÂN TÍCH
    col_w = 21.5
    gap = 2.4
    left_start = 3.5

    # 1. NHÁNH LOGIN.FAILED (ĐỎ)
    x1 = left_start
    ax.annotate("", xy=(x1 + col_w/2, 53), xytext=(40, 58),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.8, mutation_scale=12), zorder=5)
    draw_card(ax, x1, 23, col_w, 30, bg="#FFFFFF", border="#FCA5A5", shadow=True, z=1)
    draw_badge(ax, x1 + 2.5, 50.5, "1", bg="#DC2626", z=8)
    ax.text(x1 + col_w/2, 49.5, "login.failed", fontsize=11, fontweight='bold', color='#B91C1C', ha='center', zorder=10)
    draw_chip(ax, x1 + col_w/2, 45.5, "DÒ QUÉT MẬT KHẨU", bg="#FEE2E2", fg="#B91C1C", fontsize=7.8, z=4)
    ax.text(x1 + col_w/2, 41.5, "• Nạp IP vào Sliding Window\n• Kiểm tra Count >= 5 trong 60s\n• Tra cứu AbuseIPDB Score\n• Nếu vi phạm -> Sinh Alert:\n  T1110.001 (Brute-Force)", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)
    draw_chip(ax, x1 + col_w/2, 26, "MỨC ĐỘ: HIGH (CAO)", bg="#DC2626", fg="#FFFFFF", fontsize=7.8, z=4)

    # 2. NHÁNH LOGIN.SUCCESS (XANH DƯƠNG)
    x2 = x1 + col_w + gap
    ax.annotate("", xy=(x2 + col_w/2, 53), xytext=(46, 58),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.8, mutation_scale=12), zorder=5)
    draw_card(ax, x2, 23, col_w, 30, bg="#FFFFFF", border="#93C5FD", shadow=True, z=1)
    draw_badge(ax, x2 + 2.5, 50.5, "2", bg="#2563EB", z=8)
    ax.text(x2 + col_w/2, 49.5, "login.success", fontsize=11, fontweight='bold', color='#1D4ED8', ha='center', zorder=10)
    draw_chip(ax, x2 + col_w/2, 45.5, "CHIẾM QUYỀN TRUY CẬP", bg="#DBEAFE", fg="#1D4ED8", fontsize=7.8, z=4)
    ax.text(x2 + col_w/2, 41.5, "• Hacker vào trong Terminal\n• Bật Silent Monitoring\n• Theo dõi tệp lệnh phiên làm việc\n• Sinh Alert Initial Access:\n  T1078 (Valid Accounts)", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)
    draw_chip(ax, x2 + col_w/2, 26, "MỨC ĐỘ: MEDIUM", bg="#2563EB", fg="#FFFFFF", fontsize=7.8, z=4)

    # 3. NHÁNH COMMAND.INPUT (TÍM)
    x3 = x2 + col_w + gap
    ax.annotate("", xy=(x3 + col_w/2, 53), xytext=(54, 58),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.8, mutation_scale=12), zorder=5)
    draw_card(ax, x3, 23, col_w, 30, bg="#FFFFFF", border="#C4B5FD", shadow=True, z=1)
    draw_badge(ax, x3 + 2.5, 50.5, "3", bg="#7C3AED", z=8)
    ax.text(x3 + col_w/2, 49.5, "command.input", fontsize=11, fontweight='bold', color='#6D28D9', ha='center', zorder=10)
    draw_chip(ax, x3 + col_w/2, 45.5, "SỤP BẪY HONEYTOKEN", bg="#EDE9FE", fg="#6D28D9", fontsize=7.8, z=4)
    ax.text(x3 + col_w/2, 41.5, "• Regex bắt lệnh đọc file mồi:\n  cat / nano / grep / aws / env\n• Trúng bẫy mật khẩu giả\n• Sinh Alert tối khẩn cấp:\n  T1552.001 (Credentials)", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)
    draw_chip(ax, x3 + col_w/2, 26, "MỨC ĐỘ: CRITICAL (NGUY CẤP)", bg="#7C3AED", fg="#FFFFFF", fontsize=7.8, z=4)

    # 4. NHÁNH FILE_DOWNLOAD (CAM)
    x4 = x3 + col_w + gap
    ax.annotate("", xy=(x4 + col_w/2, 53), xytext=(60, 58),
                arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=1.8, mutation_scale=12), zorder=5)
    draw_card(ax, x4, 23, col_w, 30, bg="#FFFFFF", border="#FDBA74", shadow=True, z=1)
    draw_badge(ax, x4 + 2.5, 50.5, "4", bg="#EA580C", z=8)
    ax.text(x4 + col_w/2, 49.5, "file_download", fontsize=11, fontweight='bold', color='#C2410C', ha='center', zorder=10)
    draw_chip(ax, x4 + col_w/2, 45.5, "TẢI MÃ ĐỘC LÊN BẪY", bg="#FFEDD5", fg="#C2410C", fontsize=7.8, z=4)
    ax.text(x4 + col_w/2, 41.5, "• Thu hồi file hacker đẩy lên\n• Băm mã SHA256 mã độc\n• Gửi Sandbox & VirusTotal\n• Sinh Alert công cụ xâm nhập:\n  T1105 (Ingress Tool)", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)
    draw_chip(ax, x4 + col_w/2, 26, "MỨC ĐỘ: HIGH (CAO)", bg="#EA580C", fg="#FFFFFF", fontsize=7.8, z=4)

    # KHỐI TẬP TRUNG CUỐI CÙNG (END): SOAR DISPATCH
    draw_card(ax, 10, 4, 80, 14, bg="#0F172A", border="#1E293B", shadow=True, radius=1.0, z=1)
    for cx_col in [x1 + col_w/2, x2 + col_w/2, x3 + col_w/2, x4 + col_w/2]:
        ax.annotate("", xy=(cx_col, 18), xytext=(cx_col, 23),
                    arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2.0, mutation_scale=12), zorder=5)

    draw_chip(ax, 50, 15, "END: THỰC THI PHẢN ỨNG SOAR TỰ ĐỘNG (AUTOMATED PLAYBOOK)", 
              bg="#10B981", fg="#FFFFFF", fontsize=9.0, z=4)
    ax.text(50, 9.5, "Đóng gói ThreatAlert(alert_id, mitre_technique, severity, attacker_ip) -> Bắn cảnh báo Telegram SOC\n-> Kích hoạt Tarpit (Port 22222) giam lỏng kẻ tấn công -> Thiết lập luật iptables DROP cách ly vĩnh viễn", 
            fontsize=8.5, color='#E2E8F0', ha='center', linespacing=1.4, zorder=10)

    out_file = os.path.join(OUTPUT_DIR, "02_correlation_engine_flowchart.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Hoàn thành Sơ đồ 2 (Infographic): {out_file}")


# ==============================================================================
# SƠ ĐỒ 3: CHU TRÌNH BẪY MỒI & KHỬ ẨN DANH (CANARY DE-ANONYMIZATION INFOGRAPHIC)
# ==============================================================================
def draw_deanonymization_infographic():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Banner
    draw_card(ax, 3, 86, 94, 11, bg="#0F172A", border="#1E293B", shadow=True, radius=1.0, z=1)
    draw_chip(ax, 16, 93.5, "KỸ THUẬT ACTIVE DEFENSE ĐỘC QUYỀN", bg="#DC2626", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(3, 90, "   SƠ ĐỒ CHU TRÌNH BẪY MỒI & KHỬ ẨN DANH HACKER (CANARY DE-ANONYMIZATION)", 
            fontsize=15, fontweight='bold', color='#FFFFFF', va='center', zorder=10)
    ax.text(3, 87.5, "   Bóc trần địa chỉ IP thật của Hacker dù ngụy trang qua nhiều lớp Tor / VPN Proxy • Đánh lạc hướng thông minh", 
            fontsize=9.2, color='#94A3B8', va='center', zorder=10)

    # 4 CỘT THỰC THỂ CHÍNH (ENTITIES)
    col_w = 20.0
    gap = 4.0
    
    # 1. HACKER MÁY THẬT
    x1 = 4.0
    c1 = x1 + col_w/2
    draw_card(ax, x1, 66, col_w, 18, bg="#FFFFFF", border="#FCA5A5", shadow=True, z=1)
    draw_laptop_icon(ax, c1, 78, scale=1.0, color="#DC2626", z=5)
    ax.text(c1, 72.5, "KẺ TẤN CÔNG (MÁY THẬT)", fontsize=9.2, fontweight='bold', color='#991B1B', ha='center', zorder=10)
    ax.text(c1, 69.0, "IP Thật: 192.168.10.1\nOS: Windows 11 / Chrome", fontsize=7.8, color='#64748B', ha='center', fontfamily='Consolas', zorder=10)

    # 2. VỎ BỌC TOR / VPN PROXY
    x2 = x1 + col_w + gap
    c2 = x2 + col_w/2
    draw_card(ax, x2, 66, col_w, 18, bg="#FFFFFF", border="#CBD5E1", shadow=True, z=1)
    c_node = Circle((c2, 78), 2.0, facecolor="#F1F5F9", edgecolor="#475569", lw=1.8, zorder=5)
    ax.add_patch(c_node)
    ax.text(c2, 78, "VPN", fontsize=8.2, fontweight='bold', color="#475569", ha='center', va='center', zorder=10)
    ax.text(c2, 72.5, "LỚP VỎ BỌC ẨN DANH", fontsize=9.2, fontweight='bold', color='#334155', ha='center', zorder=10)
    ax.text(c2, 69.0, "IP Giả: 185.220.101.5\n(Tor Exit Node / VPN)", fontsize=7.8, color='#64748B', ha='center', fontfamily='Consolas', zorder=10)

    # 3. COWRIE HONEYPOT
    x3 = x2 + col_w + gap
    c3 = x3 + col_w/2
    draw_card(ax, x3, 66, col_w, 18, bg="#FFFFFF", border="#93C5FD", shadow=True, z=1)
    draw_server_icon(ax, c3, 78, scale=0.9, color="#2563EB", z=5)
    ax.text(c3, 72.5, "SSH HONEYPOT (PORT 2222)", fontsize=9.2, fontweight='bold', color='#1D4ED8', ha='center', zorder=10)
    ax.text(c3, 69.0, "Bẫy SSH mồi nhử\nChứa .aws/credentials giả", fontsize=7.8, color='#64748B', ha='center', zorder=10)

    # 4. CANARY WEBHOOK SERVER
    x4 = x3 + col_w + gap
    c4 = x4 + col_w/2
    draw_card(ax, x4, 66, col_w, 18, bg="#FFFFFF", border="#C4B5FD", shadow=True, z=1)
    draw_server_icon(ax, c4, 78, scale=0.9, color="#7C3AED", z=5)
    ax.text(c4, 72.5, "CANARY WEBHOOK (PORT 8080)", fontsize=9.2, fontweight='bold', color='#6D28D9', ha='center', zorder=10)
    ax.text(c4, 69.0, "Máy chủ bẫy HTTP ngầm\nChuyên khử ẩn danh", fontsize=7.8, color='#64748B', ha='center', zorder=10)

    # 4 ĐƯỜNG DÒNG THỜI GIAN (LIFELINES) CHẠY DỌC TỪ CÁC THỰC THỂ
    for cx_line in [c1, c2, c3, c4]:
        ax.plot([cx_line, cx_line], [66, 23], color="#CBD5E1", lw=1.8, linestyle="--", zorder=2)

    # BƯỚC 1: VPN -> COWRIE HONEYPOT
    y_step1 = 56
    ax.annotate("", xy=(c3 - 1, y_step1), xytext=(c2 + 1, y_step1),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.4, mutation_scale=14), zorder=5)
    draw_badge(ax, 43, y_step1 + 2.8, "1", bg="#DC2626", radius=1.4, z=8)
    ax.text(45.5, y_step1 + 2.8, "SSH Session (qua VPN): cat /root/.aws/credentials", 
            fontsize=8.5, fontweight='bold', color='#991B1B', va='center', zorder=10)
    ax.text((c2+c3)/2, y_step1 - 2.5, "Honeypot chỉ nhìn thấy IP VPN ngụy trang: 185.220.101.5", 
            fontsize=7.8, color='#64748B', ha='center', zorder=10)

    # BƯỚC 2: COWRIE HONEYPOT -> ATTACKER TERMINAL (QUA VPN)
    y_step2 = 45
    ax.annotate("", xy=(c2 + 1, y_step2), xytext=(c3 - 1, y_step2),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2.4, mutation_scale=14), zorder=5)
    draw_badge(ax, 57, y_step2 + 2.8, "2", bg="#2563EB", radius=1.4, z=8)
    ax.text(54.5, y_step2 + 2.8, "Trả về File mồi Honeytoken chứa URL bẫy độc quyền", 
            fontsize=8.5, fontweight='bold', color='#1D4ED8', ha='right', va='center', zorder=10)
    ax.text((c2+c3)/2, y_step2 - 2.5, "Nhúng URL: http://<Honeynet>:8080/canary/aws_verify?token=canary_aws_8892", 
            fontsize=7.8, color='#334155', fontfamily='Consolas', ha='center', zorder=10)

    # BƯỚC 3: MÁY THẬT -> CANARY WEBHOOK (BỎ QUA VPN!) - TÂM ĐIỂM SƠ ĐỒ
    y_step3 = 33
    # Card làm nổi bật bước 3
    draw_card(ax, 20, y_step3 - 5.0, 60, 9.5, bg="#F5F3FF", border="#8B5CF6", border_w=1.8, shadow=True, radius=0.8, z=3)
    ax.annotate("", xy=(c4 - 1, y_step3), xytext=(c1 + 1, y_step3),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=3.0, mutation_scale=16), zorder=5)
    draw_badge(ax, 23.5, y_step3 + 1.8, "3", bg="#7C3AED", radius=1.5, z=8)
    ax.text(26.5, y_step3 + 1.8, "SAI LẦM CHÍ MẠNG: Hacker click mở link trên trình duyệt máy thật!", 
            fontsize=9.2, fontweight='bold', color='#6D28D9', va='center', zorder=10)
    ax.text(50, y_step3 - 2.8, "Gói tin HTTP GET gửi TRỰC TIẾP từ card mạng vật lý -> BỎ QUA HOÀN TOÀN VPN / TOR!", 
            fontsize=8.2, fontweight='bold', color='#DC2626', ha='center', zorder=10)

    # BƯỚC 4: WEBHOOK BÓC TRẦN DANH TÍNH & PHẢN ỨNG SOAR CHỦ ĐỘNG
    y_step4 = 4
    draw_card(ax, 4, y_step4, 92, 17, bg="#0F172A", border="#10B981", border_w=2.0, shadow=True, radius=1.0, z=1)
    draw_badge(ax, 7.5, y_step4 + 12.5, "4", bg="#10B981", radius=1.6, z=8)
    ax.text(11, y_step4 + 12.5, "BƯỚC 4: LẬT TẨY TOÀN BỘ DANH TÍNH VÀ THỰC THI PHẢN ỨNG SOAR CHỦ ĐỘNG", 
            fontsize=10.5, fontweight='bold', color='#10B981', va='center', zorder=10)
    
    # 2 thẻ con kết quả
    draw_card(ax, 10, y_step4 + 1.5, 40, 9.5, bg="#1E293B", border="#334155", shadow=False, radius=0.6, z=2)
    draw_card(ax, 52, y_step4 + 1.5, 42, 9.5, bg="#1E293B", border="#334155", shadow=False, radius=0.6, z=2)

    ax.text(12, y_step4 + 9.2, "THU THẬP THÀNH CÔNG TẠI WEBHOOK (PORT 8080):", fontsize=8.2, fontweight='bold', color='#38BDF8', zorder=10)
    ax.text(12, y_step4 + 7.5, "• IP Thật vật lý: 192.168.10.1 (Bóc trần danh tính 100%)\n• User-Agent: Chrome 120 / Windows 11 vật lý\n• Token định danh: canary_aws_8892", 
            fontsize=8.0, color='#F8FAFC', fontfamily='Consolas', va='top', linespacing=1.35, zorder=10)

    ax.text(54, y_step4 + 9.2, "CHIẾN THUẬT PHÒNG THỦ CHỦ ĐỘNG (SOAR ACTIVE DEFENSE):", fontsize=8.2, fontweight='bold', color='#4ADE80', zorder=10)
    ax.text(54, y_step4 + 7.5, "• Phản hồi giả lập: Trả về HTTP 403 Forbidden SSO (Đánh lạc hướng)\n• Hacker tưởng token hết hạn -> Không nghi ngờ đã lộ IP thật\n• SOAR Enforcer tự động cô lập IP 192.168.10.1 trên Firewall!", 
            fontsize=8.0, color='#F8FAFC', va='top', linespacing=1.35, zorder=10)

    out_file = os.path.join(OUTPUT_DIR, "03_deanonymization_sequence.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Hoàn thành Sơ đồ 3 (Infographic): {out_file}")


# ==============================================================================
# SƠ ĐỒ 4: SƠ ĐỒ MÁY TRẠNG THÁI PHẢN XẠ SOAR & TARPIT (STATE MACHINE INFOGRAPHIC)
# ==============================================================================
def draw_state_machine_infographic():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Banner
    draw_card(ax, 3, 86, 94, 11, bg="#0F172A", border="#1E293B", shadow=True, radius=1.0, z=1)
    draw_chip(ax, 16, 93.5, "ĐIỀU PHỐI LUỒNG MẠNG TỰ ĐỘNG", bg="#059669", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(3, 90, "   SƠ ĐỒ MÁY TRẠNG THÁI PHẢN XẠ SOAR & TARPIT (STATE MACHINE)", 
            fontsize=15, fontweight='bold', color='#FFFFFF', va='center', zorder=10)
    ax.text(3, 87.5, "   Mô hình chuyển trạng thái phân loại rủi ro tại soar_enforcer.py • Cách ly, giam lỏng và hoàn nguyên tự động", 
            fontsize=9.2, color='#94A3B8', va='center', zorder=10)

    card_w = 26
    card_h = 24
    y_row1 = 54

    # TRẠNG THÁI 1: NORMAL (XÁM TRẮNG)
    x1 = 5
    draw_card(ax, x1, y_row1, card_w, card_h, bg="#FFFFFF", border="#94A3B8", shadow=True, z=1)
    draw_chip(ax, x1 + card_w/2, y_row1 + card_h - 3.2, "STATE 1", bg="#64748B", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(x1 + card_w/2, y_row1 + card_h - 7.0, "NORMAL", fontsize=13.5, fontweight='bold', color='#1E293B', ha='center', zorder=10)
    ax.text(x1 + card_w/2, y_row1 + card_h - 9.8, "Khách vãng lai / Kết nối mới", fontsize=8.0, color='#64748B', ha='center', zorder=10)
    ax.plot([x1 + 2, x1 + card_w - 2], [y_row1 + card_h - 11.2, y_row1 + card_h - 11.2], color='#E2E8F0', lw=1.2, zorder=3)
    ax.text(x1 + card_w/2, y_row1 + card_h - 12.8, "• Chưa có tiền sử vi phạm\n• Cổng 22 được NAT sang:\n  Cowrie Port 2222\n• Thu thập nhật ký thụ động\n• Điểm rủi ro (Abuse Score) = 0", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)

    # TRẠNG THÁI 2: SUSPICIOUS (CAM)
    x2 = 37
    draw_card(ax, x2, y_row1, card_w, card_h, bg="#FFFFFF", border="#FDBA74", shadow=True, z=1)
    draw_chip(ax, x2 + card_w/2, y_row1 + card_h - 3.2, "STATE 2", bg="#EA580C", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(x2 + card_w/2, y_row1 + card_h - 7.0, "SUSPICIOUS", fontsize=13.5, fontweight='bold', color='#C2410C', ha='center', zorder=10)
    ax.text(x2 + card_w/2, y_row1 + card_h - 9.8, "Nghi vấn / Dò quét mật khẩu", fontsize=8.0, color='#64748B', ha='center', zorder=10)
    ax.plot([x2 + 2, x2 + card_w - 2], [y_row1 + card_h - 11.2, y_row1 + card_h - 11.2], color='#FFEDD5', lw=1.2, zorder=3)
    ax.text(x2 + card_w/2, y_row1 + card_h - 12.8, "• Đăng nhập sai (Count < 5)\n• Tích lũy trong Sliding Window 60s\n• Bật chế độ Silent Monitoring\n• Tra cứu điểm tín nhiệm IP\n• Đưa vào danh sách giám sát ngầm", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)

    # TRẠNG THÁI 3: TARPITTED (ĐỎ)
    x3 = 69
    draw_card(ax, x3, y_row1, card_w, card_h, bg="#FFFFFF", border="#FCA5A5", shadow=True, z=1)
    draw_chip(ax, x3 + card_w/2, y_row1 + card_h - 3.2, "STATE 3", bg="#DC2626", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(x3 + card_w/2, y_row1 + card_h - 7.0, "TARPITTED", fontsize=13.5, fontweight='bold', color='#991B1B', ha='center', zorder=10)
    ax.text(x3 + card_w/2, y_row1 + card_h - 9.8, "Giam lỏng / Bóp nghẹt Socket", fontsize=8.0, color='#64748B', ha='center', zorder=10)
    ax.plot([x3 + 2, x3 + card_w - 2], [y_row1 + card_h - 11.2, y_row1 + card_h - 11.2], color='#FEE2E2', lw=1.2, zorder=3)
    ax.text(x3 + card_w/2, y_row1 + card_h - 12.8, "• Kích hoạt khi Count >= 5\n  hoặc chạm file bẫy Canary\n• NAT chuyển hướng sang: Port 22222\n• Gửi nhỏ giọt 1 byte / 10 giây\n• Giữ chân làm kiệt sức hacker!", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)

    # TRẠNG THÁI 4: DROPPED (XANH LÁ)
    x4 = 37
    y_row2 = 12
    draw_card(ax, x4, y_row2, card_w, card_h, bg="#FFFFFF", border="#86EFAC", shadow=True, z=1)
    draw_chip(ax, x4 + card_w/2, y_row2 + card_h - 3.2, "STATE 4", bg="#10B981", fg="#FFFFFF", fontsize=8.5, z=4)
    ax.text(x4 + card_w/2, y_row2 + card_h - 7.0, "DROPPED", fontsize=13.5, fontweight='bold', color='#065F46', ha='center', zorder=10)
    ax.text(x4 + card_w/2, y_row2 + card_h - 9.8, "Cách ly triệt để / Chặn tường lửa", fontsize=8.0, color='#64748B', ha='center', zorder=10)
    ax.plot([x4 + 2, x4 + card_w - 2], [y_row2 + card_h - 11.2, y_row2 + card_h - 11.2], color='#DCFCE7', lw=1.2, zorder=3)
    ax.text(x4 + card_w/2, y_row2 + card_h - 12.8, "• Luật tường lửa Linux tức thì:\n  iptables -I INPUT -s <IP> -j DROP\n• Từ chối mọi gói tin từ IP thật\n• Hẹn giờ TTL Timeout = 3600s\n• Tự động thu hồi lệnh khi hết hạn", 
            fontsize=8.0, color='#334155', ha='center', va='top', linespacing=1.35, zorder=10)

    # CÁC MŨI TÊN CHUYỂN TRẠNG THÁI (TRANSITIONS VỚI CHIP RÕ NÉT)
    # 1 -> 2
    ax.annotate("", xy=(x2, y_row1 + 12), xytext=(x1 + card_w, y_row1 + 12),
                arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=2.2, mutation_scale=14), zorder=4)
    draw_chip(ax, (x1 + card_w + x2)/2, y_row1 + 15, "Login fail lần 1", bg="#EA580C", fg="#FFFFFF", fontsize=7.8, z=6)

    # 2 -> 3
    ax.annotate("", xy=(x3, y_row1 + 12), xytext=(x2 + card_w, y_row1 + 12),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.2, mutation_scale=14), zorder=4)
    draw_chip(ax, (x2 + card_w + x3)/2, y_row1 + 15, "Count >= 5 / Canary Hit", bg="#DC2626", fg="#FFFFFF", fontsize=7.8, z=6)

    # 3 -> 4 (Bấm nút Telegram hoặc SOAR Rule)
    ax.annotate("", xy=(x4 + card_w, y_row2 + card_h - 3), xytext=(x3 + 3, y_row1),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.2, mutation_scale=14), zorder=4)
    draw_chip(ax, 67.5, 43.5, "Nút bấm Telegram: [ Chặn IP 3600s ]", bg="#059669", fg="#FFFFFF", fontsize=8.0, z=6)

    # 2 -> 4 (AbuseIPDB > 90% Chặn thẳng)
    ax.annotate("", xy=(x4 + card_w/2, y_row2 + card_h), xytext=(x2 + card_w/2, y_row1),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.0, mutation_scale=14), zorder=4)
    draw_chip(ax, x2 + card_w/2, (y_row1 + y_row2 + card_h)/2, "AbuseIPDB > 90%", bg="#FEE2E2", fg="#991B1B", fontsize=8.0, z=6)

    # 4 -> 1 (Hết hạn Timeout 3600s -> Quay về Normal)
    ax.plot([x4, 18, 18], [y_row2 + 10, y_row2 + 10, y_row1], color="#64748B", lw=2.0, linestyle=":", zorder=3)
    ax.annotate("", xy=(18, y_row1), xytext=(18, y_row1 - 2),
                arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=2.0, mutation_scale=12), zorder=4)
    draw_chip(ax, 27.5, y_row2 + 10, "Hết hạn TTL 3600s: Gỡ iptables, Hoàn nguyên Normal", 
              bg="#FFFFFF", fg="#475569", border="#CBD5E1", fontsize=7.8, z=6)

    out_file = os.path.join(OUTPUT_DIR, "04_soar_tarpit_state_machine.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[+] Hoàn thành Sơ đồ 4 (Infographic): {out_file}")


if __name__ == "__main__":
    print("[*] Đang xuất 4 sơ đồ phong cách Cybersecurity Infographic cao cấp...")
    draw_sliding_window_infographic()
    draw_correlation_flowchart_infographic()
    draw_deanonymization_infographic()
    draw_state_machine_infographic()
    print("[+] Hoàn tất toàn bộ 4 sơ đồ tại:", OUTPUT_DIR)
