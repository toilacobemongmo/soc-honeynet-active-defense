"""
Script: generate_missing_report_diagrams.py
Mục đích: Tự động vẽ các sơ đồ học thuật chất lượng cao (300 DPI)
phục vụ báo cáo chuyên khảo đồ án tốt nghiệp:
- Hình 2.1: Phân loại Honeypot theo mức độ tương tác (Low, Medium, High)
- Hình 2.2: Kiến trúc mô phỏng hệ thống tệp và lệnh của Cowrie Honeypot
- Hình 2.3: Vòng đời xử lý sự cố an ninh NIST SP 800-61 r2 tích hợp SOAR
- Hình 3.1: Sơ đồ kiến trúc tổng thể 5 phân lớp Active Defense & SOAR
- Hình 3.4: Giao diện Thẻ cảnh báo và Bàn phím Inline Buttons của Telegram SOAR Bot
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans", "Tahoma"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.abspath("./reports/images")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# 1. HÌNH 2.1: PHÂN LOẠI HONEYPOT THEO MỨC ĐỘ TƯƠNG TÁC
# ==============================================================================
def generate_fig_2_1():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Tiêu đề
    ax.text(50, 94, "MÔ HÌNH PHÂN LOẠI HONEYPOT THEO MỨC ĐỘ TƯƠNG TÁC",
            fontsize=13, fontweight="bold", ha="center", color="#111111")
    ax.text(50, 89.5, "So sánh đánh đổi giữa Độ sâu Tình báo (Intelligence Depth) và Mức độ Rủi ro (Security Risk)",
            fontsize=9.5, ha="center", color="#555555", style="italic")

    # Trục mũi tên đánh đổi bên dưới
    ax.annotate("", xy=(92, 10), xytext=(8, 10),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2c3e50"))
    ax.text(8, 6, "Tiêu tốn ít tài nguyên / Rủi ro thấp", fontsize=9, color="#555555", ha="left")
    ax.text(92, 6, "Tình báo phong phú / Rủi ro xâm nhập cao", fontsize=9, color="#555555", ha="right")
    ax.text(50, 11.5, "MỨC ĐỘ TƯƠNG TÁC & PHỨC TẠP TĂNG DẦN --->", fontsize=9, fontweight="bold", color="#2c3e50", ha="center")

    columns = [
        {
            "x": 8, "w": 26, "title": "1. LOW-INTERACTION",
            "subtitle": "Honeypot Tương tác Thấp",
            "bg": "#f8f9fa", "border": "#495057",
            "items": [
                "• Mô phỏng: Chỉ TCP/IP stack & banner tĩnh",
                "• Đại diện: Honeyd, Specter",
                "• Ưu điểm: Tiêu tốn cực ít RAM/CPU",
                "• Không có OS thật, an toàn 100%",
                "• Nhược điểm: Dễ bị phát hiện fingerprint",
                "• Không thu thập được payload hay shell"
            ]
        },
        {
            "x": 37, "w": 26, "title": "2. MEDIUM-INTERACTION",
            "subtitle": "Honeypot Tương tác Trung bình",
            "bg": "#f1f3f5", "border": "#1c7ed6",
            "items": [
                "• Mô phỏng: Shell ảo (VFS) & dịch vụ ứng dụng",
                "• Đại diện: Cowrie (SSH/Telnet), Dionaea",
                "• Bẫy tương tác dòng lệnh Linux",
                "• Bắt giữ và tải file mã độc (Staging)",
                "• Cân bằng lý tưởng an toàn và tình báo",
                "• Trọng tâm ứng dụng trong đồ án này"
            ]
        },
        {
            "x": 66, "w": 26, "title": "3. HIGH-INTERACTION",
            "subtitle": "Honeypot Tương tác Cao",
            "bg": "#f8f9fa", "border": "#e03131",
            "items": [
                "• Mô phỏng: Máy ảo OS thực (Real OS & Kernel)",
                "• Đại diện: Honeywall, Cuckoo Sandbox",
                "• Kẻ tấn công có toàn quyền root thật",
                "• Giám sát qua Hypervisor / EBPF Hook",
                "• Tình báo 0-day và hành vi sâu sắc nhất",
                "• Rủi ro cao: Nguy cơ bị chiếm làm bàn đạp"
            ]
        }
    ]

    for col in columns:
        rect = patches.FancyBboxPatch(
            (col["x"], 18), col["w"], 66,
            boxstyle="round,pad=1.0,rounding_size=1.5",
            facecolor=col["bg"], edgecolor=col["border"], linewidth=1.8
        )
        ax.add_patch(rect)
        ax.text(col["x"] + col["w"]/2, 79, col["title"],
                fontsize=11, fontweight="bold", ha="center", color=col["border"])
        ax.text(col["x"] + col["w"]/2, 75, col["subtitle"],
                fontsize=9, ha="center", color="#333333", style="italic")
        ax.plot([col["x"] + 2, col["x"] + col["w"] - 2], [72, 72], color="#ced4da", lw=1)

        y_item = 67
        for it in col["items"]:
            ax.text(col["x"] + 2, y_item, it, fontsize=8.5, color="#212529", va="top")
            y_item -= 8

    out_file = os.path.join(OUTPUT_DIR, "hinh_2_1_phan_loai_honeypot.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Đã tạo: {out_file}")


# ==============================================================================
# 2. HÌNH 2.2: KIẾN TRÚC COWRIE SSH/TELNET HONEYPOT
# ==============================================================================
def generate_fig_2_2():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 94, "KIẾN TRÚC MÔ PHỎNG HỆ THỐNG TỆP VÀ LỆNH CỦA COWRIE HONEYPOT",
            fontsize=12.5, fontweight="bold", ha="center", color="#111111")
    ax.text(50, 89.5, "Cơ chế cách ly Twisted Event Engine, Shell Emulation và Lưu vết Mã độc",
            fontsize=9.5, ha="center", color="#555555", style="italic")

    boxes = [
        {"x": 4, "y": 42, "w": 18, "h": 36, "title": "ATTACKER / BOTNET",
         "color": "#c92a2a", "bg": "#fff5f5",
         "lines": ["Hydra / Medusa", "Nmap / Metasploit", "SSH / Telnet Traffic", "Gửi lệnh thô & băm"]},
        {"x": 26, "y": 42, "w": 20, "h": 36, "title": "TWISTED CORE ENGINE",
         "color": "#1864ab", "bg": "#e7f5ff",
         "lines": ["Async Event-driven", "Cổng SSH 2222 / Telnet", "Xác thực tài khoản giả", "Thỏa thuận thuật toán"]},
        {"x": 50, "y": 56, "w": 22, "h": 26, "title": "SHELL & VFS EMULATOR",
         "color": "#2b8a3e", "bg": "#ebfbee",
         "lines": ["Virtual FS (fs.pickle)", "> 50 lệnh Linux ảo", "cd, ls, cat, uname", "Cách ly tuyệt đối OS thật"]},
        {"x": 50, "y": 20, "w": 22, "h": 26, "title": "MALWARE STAGING",
         "color": "#d9480f", "bg": "#fff4e6",
         "lines": ["Đánh chặn wget/curl", "Tự tải vào /downloads", "Băm SHA256 / MD5", "Tước quyền chạy (-x)"]},
        {"x": 76, "y": 42, "w": 20, "h": 36, "title": "TELEMETRY & LOGGING",
         "color": "#5f3dc4", "bg": "#f3f0ff",
         "lines": ["cowrie.json thời gian thực", "TTY Session Replay", "Metadata sự kiện chi tiết", "Đồng bộ về Mini-SOC"]}
    ]

    for b in boxes:
        r = patches.FancyBboxPatch(
            (b["x"], b["y"]), b["w"], b["h"],
            boxstyle="round,pad=0.8,rounding_size=1.2",
            facecolor=b["bg"], edgecolor=b["color"], linewidth=1.6
        )
        ax.add_patch(r)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 4.5, b["title"],
                fontsize=9.5, fontweight="bold", ha="center", color=b["color"])
        ax.plot([b["x"] + 1.5, b["x"] + b["w"] - 1.5], [b["y"] + b["h"] - 7, b["y"] + b["h"] - 7],
                color="#ced4da", lw=0.8)
        yl = b["y"] + b["h"] - 11
        for line in b["lines"]:
            ax.text(b["x"] + b["w"]/2, yl, line, fontsize=8, color="#212529", ha="center")
            yl -= 5.5

    # Mũi tên liên kết
    ax.annotate("", xy=(26, 60), xytext=(22, 60), arrowprops=dict(arrowstyle="->", lw=1.8, color="#495057"))
    ax.annotate("", xy=(50, 69), xytext=(46, 60), arrowprops=dict(arrowstyle="->", lw=1.6, color="#495057"))
    ax.annotate("", xy=(50, 33), xytext=(46, 60), arrowprops=dict(arrowstyle="->", lw=1.6, color="#495057"))
    ax.annotate("", xy=(76, 60), xytext=(72, 69), arrowprops=dict(arrowstyle="->", lw=1.6, color="#495057"))
    ax.annotate("", xy=(76, 60), xytext=(72, 33), arrowprops=dict(arrowstyle="->", lw=1.6, color="#495057"))

    out_file = os.path.join(OUTPUT_DIR, "hinh_2_2_kien_truc_cowrie.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Đã tạo: {out_file}")


# ==============================================================================
# 3. HÌNH 2.3: VÒNG ĐỜI NIST SP 800-61 R2 TÍCH HỢP SOAR
# ==============================================================================
def generate_fig_2_3():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 94, "VÒNG ĐỜI XỬ LÝ SỰ CỐ AN NINH CHUẨN NIST SP 800-61 R2 TÍCH HỢP SOAR",
            fontsize=12, fontweight="bold", ha="center", color="#111111")
    ax.text(50, 89.5, "Tự động hóa 4 giai đoạn phản ứng sự cố: Thu hẹp thời gian MTTR từ hàng chục phút về mili-giây",
            fontsize=9.5, ha="center", color="#555555", style="italic")

    phases = [
        {"x": 6, "y": 52, "w": 41, "h": 32, "title": "1. CHUẨN BỊ (PREPARATION)",
         "color": "#1971c2", "bg": "#e7f5ff",
         "items": ["• Thiết lập cụm bẫy Honeynet phân tán (DMZ, Cloud, LAN)",
                   "• Cài cắm tài liệu mồi Honeytoken (.aws/credentials, db.sql)",
                   "• Thiết lập Playbook SOAR và định tuyến cổng an toàn"]},
        {"x": 53, "y": 52, "w": 41, "h": 32, "title": "2. PHÁT HIỆN & PHÂN TÍCH (DETECTION)",
         "color": "#e8590c", "bg": "#fff4e6",
         "items": ["• Streaming log cowrie.json thời gian thực qua Non-blocking Tail",
                   "• Thuật toán Cửa sổ Trượt nhận diện MITRE ATT&CK T1110",
                   "• Trinh sát ngược OSINT (AbuseIPDB, Shodan) & Quét VirusTotal"]},
        {"x": 6, "y": 14, "w": 41, "h": 32, "title": "4. HOẠT ĐỘNG SAU SỰ CỐ (POST-INCIDENT)",
         "color": "#099268", "bg": "#e6fcf5",
         "items": ["• Xuất bản danh sách đen đe dọa (STIX 2.1 & Snort Rules)",
                   "• Tự động gửi Thẻ Cảnh báo HTML tới Chuyên viên qua Telegram",
                   "• Đánh giá và cập nhật lại trọng số rủi ro IP (Feedback Loop)"]},
        {"x": 53, "y": 14, "w": 41, "h": 32, "title": "3. NGĂN CHẶN & TRIỆT TIÊU (CONTAINMENT)",
         "color": "#c2255c", "bg": "#fff0f6",
         "items": ["• Kích hoạt iptables DROP ngăn chặn địa chỉ IP vi phạm tức thì",
                   "• Chuyển hướng kết nối Botnet vào hố Tarpit làm kiệt quệ tài nguyên",
                   "• Cách ly tệp tin mã độc vào thư mục an toàn (chmod -x)"]}
    ]

    for p in phases:
        rect = patches.FancyBboxPatch(
            (p["x"], p["y"]), p["w"], p["h"],
            boxstyle="round,pad=0.8,rounding_size=1.2",
            facecolor=p["bg"], edgecolor=p["color"], linewidth=1.6
        )
        ax.add_patch(rect)
        ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 5, p["title"],
                fontsize=9.5, fontweight="bold", ha="center", color=p["color"])
        ax.plot([p["x"] + 2, p["x"] + p["w"] - 2], [p["y"] + p["h"] - 7.5, p["y"] + p["h"] - 7.5],
                color="#ced4da", lw=0.8)
        yi = p["y"] + p["h"] - 12
        for it in p["items"]:
            ax.text(p["x"] + 2, yi, it, fontsize=8.2, color="#212529", va="top")
            yi -= 6

    # Mũi tên tuần hoàn
    ax.annotate("", xy=(53, 68), xytext=(47, 68), arrowprops=dict(arrowstyle="->", lw=2, color="#1971c2"))
    ax.annotate("", xy=(73, 46), xytext=(73, 52), arrowprops=dict(arrowstyle="->", lw=2, color="#e8590c"))
    ax.annotate("", xy=(47, 30), xytext=(53, 30), arrowprops=dict(arrowstyle="->", lw=2, color="#c2255c"))
    ax.annotate("", xy=(26, 52), xytext=(26, 46), arrowprops=dict(arrowstyle="->", lw=2, color="#099268"))

    out_file = os.path.join(OUTPUT_DIR, "hinh_2_3_vong_doi_nist_soar.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Đã tạo: {out_file}")


# ==============================================================================
# 4. HÌNH 3.1: SƠ ĐỒ KIẾN TRÚC TỔNG THỂ 5 PHÂN LỚP
# ==============================================================================
def generate_fig_3_1():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 96, "SƠ ĐỒ KIẾN TRÚC TỔNG THỂ 5 PHÂN LỚP HỆ SINH THÁI ACTIVE DEFENSE & SOAR",
            fontsize=12, fontweight="bold", ha="center", color="#111111")
    ax.text(50, 92, "Thiết kế phân lớp tách rời đảm bảo tính mở rộng cao và khả năng phản ứng tự động theo thời gian thực",
            fontsize=9, ha="center", color="#555555", style="italic")

    layers = [
        {"y": 74, "title": "TẦNG 5: GIÁM SÁT & ĐIỀU KHIỂN TƯƠNG TÁC 2 CHIỀU (TELEGRAM SOAR BOT)",
         "desc": "Thẻ cảnh báo HTML chuyên nghiệp • Bàn phím nút bấm tương tác (Trinh sát OSINT, Chặn IP, Giam Tarpit, Mở Whitelist)",
         "color": "#7048e8", "bg": "#f3f0ff"},
        {"y": 58, "title": "TẦNG 4: THỰC THI PHẢN ỨNG TỰ ĐỘNG & NGĂN CHẶN CHỦ ĐỘNG (SOAR ENFORCEMENT)",
         "desc": "Động cơ Tarpit giam lỏng (Endlessh) • iptables / Windows Firewall Enforcement • Xuất bản STIX 2.1 & Snort Rules",
         "color": "#2b8a3e", "bg": "#ebfbee"},
        {"y": 42, "title": "TẦNG 3: TƯƠNG QUAN SỰ KIỆN & TÌNH BÁO TÁC CHIẾN (CORRELATION & THREAT INTEL)",
         "desc": "Thuật toán Cửa sổ trượt (Sliding Window) • Ánh xạ MITRE ATT&CK • Trinh sát ngược AbuseIPDB/Shodan • Quét mã độc VirusTotal",
         "color": "#d9480f", "bg": "#fff4e6"},
        {"y": 26, "title": "TẦNG 2: THU THẬP & STREAMING SỰ KIỆN THỜI GIAN THỰC (EVENT STREAMING)",
         "desc": "Non-blocking Asynchronous File Tail (cowrie.json) • Bộ lọc chuẩn hóa JSON • REST Ingestion API xác thực HMAC-SHA256",
         "color": "#1864ab", "bg": "#e7f5ff"},
        {"y": 10, "title": "TẦNG 1: CẢM BIẾN & ĐÁNH LỪA CHỦ ĐỘNG (ACTIVE DECEPTION & HONEYNET)",
         "desc": "Cowrie SSH/Telnet VFS • Decoy Credentials (.aws/credentials, db_backup.sql) • Canary Webhook Server • Distributed Edge Sensors",
         "color": "#c92a2a", "bg": "#fff5f5"}
    ]

    for lay in layers:
        r = patches.FancyBboxPatch(
            (6, lay["y"]), 88, 12.5,
            boxstyle="round,pad=0.8,rounding_size=1.2",
            facecolor=lay["bg"], edgecolor=lay["color"], linewidth=1.6
        )
        ax.add_patch(r)
        ax.text(50, lay["y"] + 8.5, lay["title"],
                fontsize=9.5, fontweight="bold", ha="center", color=lay["color"])
        ax.text(50, lay["y"] + 3.5, lay["desc"],
                fontsize=8.2, ha="center", color="#212529")

    # Mũi tên luồng thông tin 2 chiều
    ax.annotate("", xy=(3, 80), xytext=(3, 16),
                arrowprops=dict(arrowstyle="<->", lw=2, color="#495057"))
    ax.text(1.5, 48, "Luồng Tác chiến 2 chiều", rotation=90, va="center", ha="center", fontsize=8, color="#495057", fontweight="bold")

    out_file = os.path.join(OUTPUT_DIR, "hinh_3_1_kien_truc_5_phan_lop.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Đã tạo: {out_file}")


# ==============================================================================
# 5. HÌNH 3.4: GIAO DIỆN VÀ NÚT BẤM TELEGRAM SOAR BOT
# ==============================================================================
def generate_fig_3_4():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 95, "GIAO DIỆN THẺ CẢNH BÁO VÀ BÀN PHÍM TƯƠNG TÁC CỦA TELEGRAM SOAR BOT",
            fontsize=12, fontweight="bold", ha="center", color="#111111")
    ax.text(50, 91, "Cơ chế điều khiển tác chiến 2 chiều (Human-in-the-loop) hỗ trợ phản ứng sự cố tức thời",
            fontsize=9.5, ha="center", color="#555555", style="italic")

    # Khung điện thoại / Khung thẻ Telegram
    card_rect = patches.FancyBboxPatch(
        (15, 12), 70, 74,
        boxstyle="round,pad=1.0,rounding_size=1.5",
        facecolor="#f8f9fa", edgecolor="#0088cc", linewidth=2.0
    )
    ax.add_patch(card_rect)

    # Tiêu đề Thẻ Cảnh báo
    header_rect = patches.Rectangle((15.5, 74), 69, 11, facecolor="#0088cc")
    ax.add_patch(header_rect)
    ax.text(50, 79.5, "[ALERT] MINI-SOC: CẢNH BÁO SỰ CỐ AN NINH (CRITICAL)",
            fontsize=10.5, fontweight="bold", ha="center", color="#ffffff")

    # Thân nội dung thẻ
    content_lines = [
        ("Thời gian phát hiện:", "2026-10-15 14:32:10 UTC (Độ trễ phản ứng: 0.8s)"),
        ("Địa chỉ IP Tấn công:", "45.33.32.156 (NL - Hà Lan / Tor Exit Node)"),
        ("Kỹ thuật MITRE ATT&CK:", "T1078 (Valid Accounts) & T1552.001 (Canary Breached)"),
        ("Hành vi ghi nhận:", "Đăng nhập SSH bẫy thành công -> Đọc /root/.aws/credentials"),
        ("Khử ẩn danh (Real IP):", "14.161.42.88 (Việt Nam - Viettel / Máy thật Attacker)"),
        ("Đề xuất Tác chiến SOAR:", "Đã kích hoạt Tarpit giam lỏng. Chờ chuyên viên phê duyệt.")
    ]
    y_pos = 68
    for label, val in content_lines:
        ax.text(18, y_pos, label, fontsize=8.5, fontweight="bold", color="#1e3a8a")
        ax.text(45, y_pos, val, fontsize=8.5, color="#1f2937")
        y_pos -= 5.2

    # Đường phân cách
    ax.plot([18, 82], [34, 34], color="#cbd5e1", lw=1)

    # Các nút bấm Inline Keyboard Actions
    buttons = [
        {"x": 18, "y": 24, "w": 30, "h": 7, "text": "[OSINT] Trinh sát ngược", "color": "#0284c7"},
        {"x": 52, "y": 24, "w": 30, "h": 7, "text": "[BLOCK] Chặn Firewall tức thì", "color": "#dc2626"},
        {"x": 18, "y": 15, "w": 30, "h": 7, "text": "[TARPIT] Giam lỏng kết nối", "color": "#d97706"},
        {"x": 52, "y": 15, "w": 30, "h": 7, "text": "[ALLOW] Mở khóa Whitelist", "color": "#16a34a"},
    ]

    for btn in buttons:
        btn_patch = patches.FancyBboxPatch(
            (btn["x"], btn["y"]), btn["w"], btn["h"],
            boxstyle="round,pad=0.4,rounding_size=0.8",
            facecolor="#ffffff", edgecolor=btn["color"], linewidth=1.5
        )
        ax.add_patch(btn_patch)
        ax.text(btn["x"] + btn["w"]/2, btn["y"] + btn["h"]/2, btn["text"],
                fontsize=8.5, fontweight="bold", ha="center", va="center", color=btn["color"])

    out_file = os.path.join(OUTPUT_DIR, "hinh_3_4_telegram_bot_interface.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Đã tạo: {out_file}")


def main():
    print("[*] Bắt đầu sinh các sơ đồ minh họa còn thiếu cho báo cáo đồ án...")
    generate_fig_2_1()
    generate_fig_2_2()
    generate_fig_2_3()
    generate_fig_3_1()
    generate_fig_3_4()
    print("[+] Hoàn tất sinh toàn bộ 5 hình ảnh minh họa mới!")


if __name__ == "__main__":
    main()
