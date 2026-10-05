"""
Script: generate_simple_diagram.py
Mục đích: Tạo sơ đồ kiến trúc tối giản, học thuật, đen trắng/xám trang nhã cho báo cáo đồ án.
"""

import sys
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Kích thước chuẩn báo cáo (A4 ngang tỷ lệ đẹp)
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300, facecolor='#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Font mặc định
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']

# Tiêu đề chính
ax.text(50, 94, "SƠ ĐỒ NGUYÊN LÝ HOẠT ĐỘNG ACTIVE HONEYPOT & SOAR", 
        fontsize=15, fontweight='bold', ha='center', color='#111111')
ax.text(50, 90, "Quy trình 4 bước: Dụ bẫy (Deception) -> Gài mồi (Honeytokens) -> Khử ẩn danh (Canary) -> Phản ứng tự động (SOAR)", 
        fontsize=10, ha='center', color='#555555')

def draw_step_box(ax, x, y, w, h, step_num, title, items):
    # Hộp khối
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.8,rounding_size=1.2",
        facecolor="#f8f9fa", edgecolor="#212529", linewidth=1.4
    )
    ax.add_patch(rect)
    
    # Header khối
    badge = patches.FancyBboxPatch(
        (x, y + h - 6), w, 6,
        boxstyle="round,pad=0.2,rounding_size=1.0",
        facecolor="#e9ecef", edgecolor="#212529", linewidth=1.0
    )
    ax.add_patch(badge)
    ax.text(x + w/2, y + h - 3.8, f"BƯỚC {step_num}: {title.upper()}", 
            fontsize=9.5, fontweight='bold', ha='center', va='center', color='#111111')
    
    # Nội dung
    start_y = y + h - 9.5
    for idx, item in enumerate(items):
        ax.text(x + 2.5, start_y - (idx * 3.6), f"• {item}", fontsize=8.8, color='#2b2b2b')

# 4 Khối chính xếp thành hình chữ U cân đối
# Hàng trên: Bước 1 -> Bước 2
# Khối 1: Tấn công
draw_step_box(
    ax, 7, 52, 36, 28,
    step_num=1,
    title="Đột nhập & Lừa nhử (Deception)",
    items=[
        "Kẻ tấn công quét cổng & Brute-force qua SSH (Port 2222)",
        "Honeypot chấp nhận đăng nhập giả lập (Fake Auth)",
        "Kẻ tấn công bị cô lập hoàn toàn trong RAM (VFS Sandbox)",
        "Tin rằng đã chiếm quyền root của máy chủ Ubuntu thật"
    ]
)

# Mũi tên Bước 1 -> Bước 2
ax.annotate(
    "", xy=(57, 66), xytext=(43, 66),
    arrowprops=dict(facecolor="#212529", edgecolor="#212529", width=2.0, headwidth=7, headlength=7)
)
ax.text(50, 68, "Khám phá VFS\n(ls, cd, cat)", fontsize=8.5, ha='center', va='bottom', color='#333333', fontweight='bold')

# Khối 2: Gài mồi Honeytoken
draw_step_box(
    ax, 57, 52, 36, 28,
    step_num=2,
    title="Gài bẫy mồi (Honeytokens)",
    items=[
        "Hệ thống gài sẵn tài liệu nhạy cảm trong VFS:",
        "  - /root/.aws/credentials (Chứa AWS Key + Canary URL)",
        "  - /root/.bash_history (Lệnh curl patch.sh bí mật)",
        "  - /var/backups/db_backup.sql (Database Dump + SSO)",
        "Hacker đọc trộm file bằng cat / nano và sao chép link"
    ]
)

# Mũi tên Bước 2 xuống Bước 3
ax.annotate(
    "", xy=(75, 40), xytext=(75, 52),
    arrowprops=dict(facecolor="#212529", edgecolor="#212529", width=2.0, headwidth=7, headlength=7)
)
ax.text(76, 46, " Hacker copy link mở trên máy thật\n (Trình duyệt Chrome / Edge)", 
        fontsize=8.5, ha='left', va='center', color='#333333', fontweight='bold')

# Hàng dưới: Bước 3 <- Bước 4
# Khối 3: Khử ẩn danh
draw_step_box(
    ax, 57, 12, 36, 28,
    step_num=3,
    title="Khử ẩn danh (De-anonymization)",
    items=[
        "Hacker truy cập URL Canary Webhook (Port 8080)",
        "Kết nối đi trực tiếp từ máy thật, vượt qua Proxy/VPN",
        "Máy chủ Canary thu được IP THẬT (192.168.10.1) & User-Agent",
        "Hệ thống ngụy trang trả về trang 403 Forbidden",
        "Kích hoạt tức thời cảnh báo nguy cấp về SOAR Engine"
    ]
)

# Mũi tên Bước 3 sang Bước 4 (quay về trái)
ax.annotate(
    "", xy=(43, 26), xytext=(57, 26),
    arrowprops=dict(facecolor="#212529", edgecolor="#212529", width=2.0, headwidth=7, headlength=7)
)
ax.text(50, 28, "Bắn tín hiệu\nSOAR Alert", fontsize=8.5, ha='center', va='bottom', color='#333333', fontweight='bold')

# Khối 4: SOAR Phản ứng
draw_step_box(
    ax, 7, 12, 36, 28,
    step_num=4,
    title="Phản ứng tự động & Giam lỏng (SOAR)",
    items=[
        "TCP Socket Tarpit: Giảm tốc độ truyền dữ liệu 3s/byte (Làm treo shell)",
        "Reverse OSINT: Tự động điều tra AbuseIPDB, Shodan & GeoIP",
        "Malware Quarantine: Cô lập mẫu mã độc và kiểm tra VirusTotal",
        "Telegram SOAR Bot: Báo động tức thì đến chuyên viên SOC",
        "Hỗ trợ ra quyết định 1-click: [Chặn IP] - [Trinh sát] - [Bỏ qua]"
    ]
)

# Khung viền tổng thể toàn bộ trang
outer_border = patches.Rectangle(
    (2, 2), 96, 96,
    facecolor="none", edgecolor="#ced4da", linewidth=1.0, linestyle="-"
)
ax.add_patch(outer_border)

plt.tight_layout()
output_file = "reports/images/so_do_nguyen_ly_don_gian.png"
plt.savefig(output_file, dpi=300)
plt.close()
print(f"[+] Đã tạo sơ đồ đơn giản tại: {output_file}")
