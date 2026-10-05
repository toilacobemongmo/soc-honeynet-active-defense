"""
Script: generate_self_explanatory_diagram.py
Mục đích: Vẽ sơ đồ TỰ GIẢI THÍCH (Self-Explanatory) - nhìn 5 giây là hiểu toàn bộ câu chuyện:
1. Hacker giấu mặt qua Tor/VPN (IP Giả)
2. Honeypot đón tiếp & gài file mồi .aws/credentials
3. Hacker tò mò copy link mở trên Chrome máy thật (không qua VPN)
4. Webhook bóc trần IP THẬT (192.168.10.1) & trả về lỗi 403 ngụy trang
5. SOAR làm đơ shell hacker (Tarpit) & báo về Telegram
"""

import sys
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Kích thước 16:9 chuẩn slide thuyết trình và in ấn (300 DPI)
fig, ax = plt.subplots(figsize=(16, 9), dpi=300, facecolor='#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'Tahoma']

# ==================== HEADER ====================
ax.text(50, 95, "QUY TRÌNH BẪY & KHỬ ẨN DANH HACKER (ACTIVE DE-ANONYMIZATION)", 
        fontsize=16, fontweight='bold', ha='center', color='#111111')
ax.text(50, 91.5, "Nhìn vào sơ đồ để thấy: Hacker giấu IP bằng cách nào -> Bị lừa ra sao -> Lộ IP Thật như thế nào", 
        fontsize=10.5, ha='center', color='#555555')

def draw_card(x, y, w, h, step_num, title, badge_color, bg_color, border_color, lines, note=""):
    # Box chính
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.5,rounding_size=1.2",
        facecolor=bg_color, edgecolor=border_color, linewidth=1.8
    )
    ax.add_patch(box)
    
    # Nút tròn đánh số bước
    circle = patches.Circle((x + 3.5, y + h - 4.5), 2.8, facecolor=badge_color, edgecolor='none')
    ax.add_patch(circle)
    ax.text(x + 3.5, y + h - 4.5, str(step_num), fontsize=12, fontweight='bold', color='#ffffff', ha='center', va='center')
    
    # Tiêu đề bước
    ax.text(x + 7.5, y + h - 4.5, title, fontsize=11, fontweight='bold', color='#111111', va='center')
    
    # Đường kẻ ngang phân cách
    ax.plot([x + 1.5, x + w - 1.5], [y + h - 8.5, y + h - 8.5], color=border_color, linewidth=0.8, alpha=0.6)
    
    # Nội dung các dòng
    start_y = y + h - 12
    for i, line in enumerate(lines):
        ax.text(x + 2.5, start_y - (i * 3.8), line, fontsize=9.2, color='#222222')
        
    # Ghi chú / Kết quả mấu chốt ở đáy card
    if note:
        notebox = patches.FancyBboxPatch(
            (x + 1.5, y + 1.5), w - 3, 5.5,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor='#ffffff', edgecolor=badge_color, linewidth=1.2
        )
        ax.add_patch(notebox)
        ax.text(x + w/2, y + 4.2, note, fontsize=8.8, fontweight='bold', color=badge_color, ha='center', va='center')

# ==================== HÀNG TRÊN: BƯỚC 1 -> BƯỚC 2 -> BƯỚC 3 ====================

# BƯỚC 1
draw_card(
    x=4, y=51, w=28, h=36,
    step_num=1,
    title="HACKER NGỤY TRANG",
    badge_color="#dc3545", bg_color="#fff5f5", border_color="#e0a1a5",
    lines=[
        "• Máy thật của Hacker: 192.168.10.1",
        "• Hacker bật VPN / Tor để che giấu",
        "• Lệnh chạy: ssh root@target -p 2222",
        "• IP gửi tới server bị đổi thành IP giả",
        "• Hacker tin rằng mình đã ẩn danh 100%"
    ],
    note="[!] IP HONEYPOT NHÌN THẤY: 185.220.101.5 (IP Giả)"
)

# Mũi tên Bước 1 -> Bước 2
ax.annotate(
    "", xy=(36, 69), xytext=(32, 69),
    arrowprops=dict(facecolor="#212529", edgecolor="#212529", width=2.5, headwidth=8, headlength=8)
)
ax.text(34, 71, "SSH vào\nPort 2222", fontsize=8.5, fontweight='bold', ha='center', color='#333333')

# BƯỚC 2
draw_card(
    x=36, y=51, w=28, h=36,
    step_num=2,
    title="HONEYPOT GÀI BẪY",
    badge_color="#0d6efd", bg_color="#f0f7ff", border_color="#9ec5fe",
    lines=[
        "• Honeypot chấp nhận đăng nhập (Fake Auth)",
        "• Nhốt hacker vào Linux ảo trong RAM",
        "• Gài sẵn file mồi: /root/.aws/credentials",
        "• Trong file có tài khoản AWS và link bí mật:",
        "  http://192.168.10.130:8080/canary/aws..."
    ],
    note="[+] HACKER ĐỌC FILE VÀ THẤY LINK KIỂM TRA"
)

# Mũi tên Bước 2 -> Bước 3
ax.annotate(
    "", xy=(68, 69), xytext=(64, 69),
    arrowprops=dict(facecolor="#212529", edgecolor="#212529", width=2.5, headwidth=8, headlength=8)
)
ax.text(66, 71, "Copy link ra\nmáy thật", fontsize=8.5, fontweight='bold', ha='center', color='#333333')

# BƯỚC 3
draw_card(
    x=68, y=51, w=28, h=36,
    step_num=3,
    title="HACKER SẬP BẪY",
    badge_color="#fd7e14", bg_color="#fff9f2", border_color="#ffc78e",
    lines=[
        "• Hacker tò mò muốn biết tài khoản AWS",
        "  có xài được không",
        "• Hacker mở Chrome trên máy tính thật",
        "• Dán link vào và bấm ENTER",
        "• Trình duyệt Chrome KHÔNG chạy qua Tor!"
    ],
    note="[!] BẪY KÍCH HOẠT: KẾT NỐI ĐI THẲNG TỪ IP THẬT"
)

# Mũi tên uốn từ Bước 3 xuống Bước 4
ax.annotate(
    "", xy=(82, 42), xytext=(82, 51),
    arrowprops=dict(facecolor="#6f42c1", edgecolor="#6f42c1", width=2.5, headwidth=8, headlength=8)
)
ax.text(82.5, 46.5, " Gửi request HTTP về Port 8080", fontsize=9, fontweight='bold', color='#6f42c1', va='center')


# ==================== HÀNG DƯỚI: BƯỚC 4 & BƯỚC 5 ====================

# BƯỚC 4
draw_card(
    x=52, y=6, w=44, h=35,
    step_num=4,
    title="LỘ TRẦN IP THẬT (KHỬ ẨN DANH)",
    badge_color="#6f42c1", bg_color="#f8f5fc", border_color="#d8c5f5",
    lines=[
        "• Máy chủ Canary Webhook (Port 8080) tiếp nhận kết nối",
        "• Thu được IP NGUỒN: 192.168.10.1 (IP THẬT MÁY HACKER!)",
        "• Thu được User-Agent: Chrome / Windows 11 của hacker",
        "• Trả về trang: 403 Forbidden (Fake SSO: Invalid Certificate)",
        "• Hacker tưởng link công ty bị lỗi -> KHÔNG HỀ BIẾT MÌNH ĐÃ BỊ LỘ!"
    ],
    note="[KẾT QUẢ] TƯỚC BỎ HOÀN TOÀN LỚP VỎ BỌC VPN / TOR CỦA HACKER!"
)

# Mũi tên Bước 4 -> Bước 5 (quay sang trái)
ax.annotate(
    "", xy=(48, 23.5), xytext=(52, 23.5),
    arrowprops=dict(facecolor="#198754", edgecolor="#198754", width=2.5, headwidth=8, headlength=8)
)
ax.text(50, 26, "SOAR Phản công", fontsize=8.5, fontweight='bold', ha='center', color='#198754')

# BƯỚC 5
draw_card(
    x=4, y=6, w=44, h=35,
    step_num=5,
    title="SOAR PHẢN CÔNG & GIAM LỎNG",
    badge_color="#198754", bg_color="#f2fcf5", border_color="#a3cfbb",
    lines=[
        "1. TCP TARPIT: Giảm tốc độ truyền SSH còn 3 giây / 1 byte",
        "   -> Làm ĐƠ CỨNG terminal của hacker, không gõ tiếp được!",
        "2. REVERSE OSINT: Tự tra cứu AbuseIPDB, Shodan, vị trí địa lý của hacker",
        "3. BÁO ĐỘNG TELEGRAM: Gửi thông báo khẩn cấp tới Chuyên viên SOC",
        "   -> Kèm nút bấm: [ Chặn IP 192.168.10.1 3600 giây ]"
    ],
    note="[KẾT QUẢ] HACKER BỊ KHỐNG CHẾ - SOC KIỂM SOÁT HOÀN TOÀN"
)

# Viền ngoài trang nhã
outer = patches.Rectangle((1.5, 2), 97, 96, facecolor="none", edgecolor="#dee2e6", linewidth=1.2)
ax.add_patch(outer)

plt.tight_layout()
output_path = os.path.abspath("./reports/images/so_do_truc_quan_de_hieu_nhat.png")
plt.savefig(output_path, dpi=300)
plt.close()
print(f"[+] Đã tạo thành công ảnh trực quan dễ hiểu tại: {output_path}")
