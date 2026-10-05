"""
Script: generate_architecture_images.py
Mục đích: Tự động vẽ 4 ảnh infographic minh họa chi tiết 4 giai đoạn của hệ thống Active Honeypot & SOAR.
Định dạng: Hình ảnh phân giải cao (2800x1700, 200 DPI), phong cách Cyber Dark Hiện Đại.
"""

import os
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Tạo thư mục lưu ảnh
OUTPUT_DIR = os.path.abspath("./reports/images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cấu hình chung giao diện Cyber Dark
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'Tahoma']
plt.rcParams['axes.edgecolor'] = '#30363d'
plt.rcParams['axes.linewidth'] = 1.2

BG_COLOR = "#0d1117"        # Đen xanh GitHub Dark
CARD_BG = "#161b22"         # Màu thẻ xám tối
BORDER_COLOR = "#30363d"    # Viền xám
TEXT_WHITE = "#f0f6fc"      # Chữ trắng sáng
TEXT_MUTED = "#8b949e"      # Chữ xám mờ
CYAN = "#58a6ff"            # Xanh dương neon
GREEN = "#3fb950"           # Xanh lá neon
RED = "#f85149"             # Đỏ cảnh báo
GOLD = "#d29922"            # Vàng bẫy mồi
PURPLE = "#bc8cff"          # Tím khử ẩn danh
TERMINAL_BG = "#030712"     # Đen tuyệt đối cho cửa sổ terminal


def draw_card(ax, x, y, w, h, title, subtitle, items, border_color=BORDER_COLOR, card_bg=CARD_BG, title_color=TEXT_WHITE):
    """Vẽ một thẻ khối kiến trúc phong cách cyber modern."""
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        facecolor=card_bg, edgecolor=border_color, linewidth=1.8,
        transform=ax.transAxes
    )
    ax.add_patch(rect)
    
    # Tiêu đề thẻ
    ax.text(x + 0.02, y + h - 0.045, title, fontsize=12, fontweight='bold', color=title_color, transform=ax.transAxes)
    header_space = 0.075
    if subtitle:
        ax.text(x + 0.02, y + h - 0.075, subtitle, fontsize=9.2, color=TEXT_MUTED, transform=ax.transAxes)
        header_space = 0.115
    
    # Các dòng nội dung bên trong thẻ: tính bước nhảy tự động để không bao giờ bị chạm đáy
    avail_h = h - header_space - 0.025
    n = max(len(items), 1)
    step = min(0.040, avail_h / n)
    font_size = 9.5 if n <= 5 else 8.8
    
    start_y = y + h - header_space - 0.012
    for idx, item in enumerate(items):
        item_y = start_y - (idx * step)
        ax.text(x + 0.02, item_y, f"• {item}", fontsize=font_size, color=TEXT_WHITE, transform=ax.transAxes)


def draw_terminal(ax, x, y, w, h, title, lines):
    """Vẽ một cửa sổ console / terminal giả lập."""
    # Khung terminal
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        facecolor=TERMINAL_BG, edgecolor="#484f58", linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(rect)
    
    # Thanh tiêu đề terminal
    header = patches.FancyBboxPatch(
        (x, y + h - 0.045), w, 0.045,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor="#21262d", edgecolor="#484f58", linewidth=1.0,
        transform=ax.transAxes
    )
    ax.add_patch(header)
    
    # 3 nút đèn Mac/Linux (đỏ, vàng, xanh)
    circle_colors = ["#ff5f56", "#ffbd2e", "#27c93f"]
    for i, c in enumerate(circle_colors):
        circ = patches.Circle((x + 0.018 + i * 0.016, y + h - 0.022), 0.0055, facecolor=c, transform=ax.transAxes)
        ax.add_patch(circ)
        
    ax.text(x + 0.075, y + h - 0.028, title, fontsize=9.2, fontweight='bold', color=TEXT_MUTED, transform=ax.transAxes)
    
    # Dòng chữ lệnh console
    avail_h = h - 0.065
    n = max(len(lines), 1)
    step = min(0.034, avail_h / n)
    font_size = 9.2 if n <= 8 else 8.4
    
    line_y = y + h - 0.072
    for text, color in lines:
        ax.text(x + 0.02, line_y, text, fontsize=font_size, fontfamily='Consolas', color=color, transform=ax.transAxes)
        line_y -= step


def draw_arrow(ax, x1, y1, x2, y2, label="", color=CYAN):
    """Vẽ mũi tên luồng dữ liệu kèm nhãn."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(facecolor=color, edgecolor=color, width=2.5, headwidth=9, headlength=9, shrink=0.05),
        xycoords='axes fraction', textcoords='axes fraction'
    )
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.025
        ax.text(mid_x, mid_y, label, fontsize=9.5, fontweight='bold', color=color, ha='center', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_COLOR, edgecolor=color, alpha=0.9))


# ==============================================================================
# ẢNH 1: GIAI ĐOẠN 1 - MÔ PHỎNG LỪA NHỬ & ĐỘT NHẬP (DECEPTION & INTRUSION)
# ==============================================================================
def create_image_1():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header
    ax.text(0.04, 0.94, "GIAI ĐOẠN 1: MÔ PHỎNG LỪA NHỬ & ĐỘT NHẬP (DECEPTION & INTRUSION)",
            fontsize=17, fontweight='bold', color=CYAN, transform=ax.transAxes)
    ax.text(0.04, 0.90, "Cơ chế: Mở cổng SSH 2222, Giả mạo Ubuntu 22.04 LTS, Xác thực giả lập và giam lỏng vào VFS",
            fontsize=11, color=TEXT_MUTED, transform=ax.transAxes)
    
    # Badge MITRE
    ax.text(0.82, 0.93, "MITRE ATT&CK: T1110 / T1046", fontsize=10, fontweight='bold', color=RED,
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="#3d1214", edgecolor=RED))

    # Khối 1: Attacker
    draw_card(
        ax, 0.04, 0.48, 0.27, 0.38,
        title="1. Kẻ tấn công (Attacker)",
        subtitle="IP: 192.168.10.1 (Windows/Kali)",
        items=[
            "Quét cổng mạng (Nmap / Shodan)",
            "Phát hiện cổng SSH 2222 đang mở",
            "Chạy Brute-force từ điển (Hydra/Script)",
            "Thử tài khoản: root/root, ubuntu/123456",
            "Mục tiêu: Đột nhập chiếm quyền điều khiển"
        ],
        border_color=RED,
        title_color=RED
    )

    # Mũi tên 1 -> 2
    draw_arrow(ax, 0.31, 0.67, 0.38, 0.67, label="SSH Connection\nPort 2222", color=RED)

    # Khối 2: Mini SSH Honeypot
    draw_card(
        ax, 0.38, 0.48, 0.28, 0.38,
        title="2. Mini SSH Honeypot",
        subtitle="Dịch vụ mồi nhử ảo (Paramiko Core)",
        items=[
            "Lắng nghe tại 0.0.0.0:2222",
            "Trình diễn giao thức chuẩn SSHv2",
            "Cơ chế Chấp thuận giả (Fake Auth):",
            "  -> Mọi mật khẩu hợp lệ đều mở phiên",
            "Ghi nhật ký tương tác: cowrie.json",
            "Bắn sự kiện tức thời về SOAR Engine"
        ],
        border_color=CYAN,
        title_color=CYAN
    )

    # Mũi tên 2 -> 3
    draw_arrow(ax, 0.66, 0.67, 0.72, 0.67, label="Chuyển vào VFS\n(Virtual Jail)", color=GREEN)

    # Khối 3: VFS Sandbox
    draw_card(
        ax, 0.72, 0.48, 0.24, 0.38,
        title="3. Nhà tù ảo (VFS Jail)",
        subtitle="Hệ thống tệp tin ảo độc lập",
        items=[
            "Không ảnh hưởng tới OS thật",
            "Cấu trúc thư mục: /root, /etc, /var",
            "Mô phỏng 100% lệnh: cd, ls, cat",
            "Gợi ý phím TAB & History",
            "Kẻ tấn công tin là máy thật!"
        ],
        border_color=GREEN,
        title_color=GREEN
    )

    # Cửa sổ Terminal minh họa bên dưới
    terminal_lines = [
        ("attacker@kali:~$ ssh root@192.168.10.130 -p 2222", TEXT_WHITE),
        ("root@192.168.10.130's password: ********", TEXT_MUTED),
        ("Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)", CYAN),
        ("Last login: Fri Oct  2 08:44:12 2026 from 192.168.1.100", TEXT_MUTED),
        ("root@ubuntu-srv:~# id", GREEN),
        ("uid=0(root) gid=0(root) groups=0(root)", TEXT_WHITE),
        ("root@ubuntu-srv:~# uname -a", GREEN),
        ("Linux ubuntu-srv 5.15.0-89-generic #99-Ubuntu SMP x86_64 GNU/Linux", TEXT_WHITE)
    ]
    draw_terminal(ax, 0.04, 0.07, 0.52, 0.36, "Terminal Hacker (Bị đánh lừa 100%)", terminal_lines)

    # Khối ghi chú cơ chế kỹ thuật
    draw_card(
        ax, 0.58, 0.07, 0.38, 0.36,
        title="Ý nghĩa Phòng thủ Chủ động (Active Defense):",
        subtitle="Mô hình phòng thủ 'Chủ động Đánh lừa' (Active Deception)",
        items=[
            "Tách biệt hoàn toàn: Tấn công chỉ xảy ra trong RAM ảo",
            "Hấp thu xung lực: Giữ chân hacker khỏi hạ tầng nghiệp vụ thật",
            "Thu thập thông tin: Ghi nhận công cụ, kỹ thuật của đối thủ",
            "Dọn đường: Chuẩn bị kích hoạt bẫy khử ẩn danh ở bước tiếp theo!"
        ],
        border_color=GOLD,
        title_color=GOLD
    )

    plt.tight_layout()
    img_path = os.path.join(OUTPUT_DIR, "01_deception_intrusion.png")
    plt.savefig(img_path, facecolor=BG_COLOR)
    plt.close()
    print(f"[+] Đã tạo ảnh 1: {img_path}")


# ==============================================================================
# ẢNH 2: GIAI ĐOẠN 2 - BẪY MỒI TÀI KHOẢN (HONEYTOKENS & BREADCRUMBS)
# ==============================================================================
def create_image_2():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header
    ax.text(0.04, 0.94, "GIAI ĐOẠN 2: BẪY MỒI TÀI KHOẢN & DẪN DỤ HÀNH VI (HONEYTOKENS)",
            fontsize=17, fontweight='bold', color=GOLD, transform=ax.transAxes)
    ax.text(0.04, 0.90, "Cơ chế: Gài sẵn AWS credentials, Lịch sử lệnh bí mật và Database Dump chứa Canary Webhook URL",
            fontsize=11, color=TEXT_MUTED, transform=ax.transAxes)
    
    # Badge MITRE
    ax.text(0.81, 0.93, "MITRE ATT&CK: T1082 / T1552.001", fontsize=10, fontweight='bold', color=GOLD,
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="#3a2e12", edgecolor=GOLD))

    # Khối 1: Hành vi dò quét của hacker
    draw_card(
        ax, 0.04, 0.48, 0.27, 0.38,
        title="1. Dò tìm tài liệu nhạy cảm",
        subtitle="Hacker tìm kiếm dữ liệu có giá trị",
        items=[
            "Chạy lệnh tìm tệp: ls -la",
            "Kiểm tra thư mục ẩn: /root/.aws",
            "Kiểm tra bản sao lưu: /var/backups",
            "Mở xem bằng lệnh: cat / nano",
            "Mục tiêu: Đánh cắp Secret Keys / DB"
        ],
        border_color=RED,
        title_color=RED
    )

    draw_arrow(ax, 0.31, 0.67, 0.38, 0.67, label="Đọc trúng\nFile bẫy", color=GOLD)

    # Khối 2: 3 Bẫy Honeytoken chiến lược
    draw_card(
        ax, 0.38, 0.48, 0.32, 0.38,
        title="2. Ba lớp bẫy Honeytokens mồi",
        subtitle="Gài sẵn trong hệ thống tệp tin ảo VFS",
        items=[
            "Bẫy 1: /root/.aws/credentials",
            "  -> Chứa AWS Access Key & Endpoint xác thực",
            "Bẫy 2: /root/.bash_history",
            "  -> Chứa lệnh tải patch bí mật qua curl",
            "Bẫy 3: /var/backups/db_backup.sql",
            "  -> Chứa Hash mật khẩu Admin & Link SSO"
        ],
        border_color=GOLD,
        title_color=GOLD
    )

    draw_arrow(ax, 0.70, 0.67, 0.76, 0.67, label="Kích hoạt\nCảnh báo", color=CYAN)

    # Khối 3: Correlation Engine cảnh báo sớm
    draw_card(
        ax, 0.76, 0.48, 0.20, 0.38,
        title="3. Phát hiện sớm",
        subtitle="Correlation Engine",
        items=[
            "Bắt sự kiện đọc file",
            "Tạo Alert T1552",
            "Mức độ: CRITICAL",
            "Chuẩn bị bẫy Khử",
            "ẩn danh khi hacker",
            "dùng URL ra ngoài!"
        ],
        border_color=CYAN,
        title_color=CYAN
    )

    # Cửa sổ Terminal minh họa nội dung file mồi
    terminal_lines = [
        ("root@ubuntu-srv:~# cd /root/.aws && ls -la", GREEN),
        ("total 8", TEXT_MUTED),
        ("-rw------- 1 root root 280 Oct  2 10:00 credentials", TEXT_WHITE),
        ("root@ubuntu-srv:~/.aws# cat credentials", GREEN),
        ("[default]", CYAN),
        ("aws_access_key_id = AKIAIOSFODNN7CANARYAWS", GOLD),
        ("aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", GOLD),
        ("# Honeytoken Canary Beacon (HTTP Verification Endpoint):", TEXT_MUTED),
        ("# http://192.168.10.130:8080/canary/aws_verify?token=canary_aws_8892", RED),
        ("region = ap-southeast-1", CYAN)
    ]
    draw_terminal(ax, 0.04, 0.07, 0.58, 0.36, "Nội dung bẫy mồi Canary Honeytoken", terminal_lines)

    # Khối phân tích tâm lý đối thủ
    draw_card(
        ax, 0.64, 0.07, 0.32, 0.36,
        title="Đòn tâm lý với Hacker:",
        subtitle="Khai thác tính hiếu kỳ & trục lợi",
        items=[
            "Hacker tin rằng vừa tìm thấy kho báu",
            "Hacker copy link đem ra máy thật kiểm tra",
            "Thay vì tấn công tiếp trên shell, hacker",
            "dùng trình duyệt Chrome/Edge truy cập",
            "==> Bước vào cái bẫy chết người ở Bước 3!"
        ],
        border_color=PURPLE,
        title_color=PURPLE
    )

    plt.tight_layout()
    img_path = os.path.join(OUTPUT_DIR, "02_honeytokens_breadcrumbs.png")
    plt.savefig(img_path, facecolor=BG_COLOR)
    plt.close()
    print(f"[+] Đã tạo ảnh 2: {img_path}")


# ==============================================================================
# ẢNH 3: GIAI ĐOẠN 3 - BẪY CANARY KHỬ ẨN DANH (ACTIVE DE-ANONYMIZATION)
# ==============================================================================
def create_image_3():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header
    ax.text(0.04, 0.94, "GIAI ĐOẠN 3: BẪY CANARY KHỬ ẨN DANH & LẬT TẨY IP THẬT",
            fontsize=17, fontweight='bold', color=PURPLE, transform=ax.transAxes)
    ax.text(0.04, 0.90, "Cơ chế: Webhook Port 8080 đón lõng HTTP Request, tước bỏ VPN/Proxy, định danh máy thật của Hacker",
            fontsize=11, color=TEXT_MUTED, transform=ax.transAxes)
    
    # Badge MITRE
    ax.text(0.79, 0.93, "MITRE ATT&CK: T1552.001 (De-cloaking)", fontsize=10, fontweight='bold', color=PURPLE,
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="#351a42", edgecolor=PURPLE))

    # Khối 1: Hacker mở link trên máy thật
    draw_card(
        ax, 0.04, 0.48, 0.28, 0.38,
        title="1. Hacker dính bẫy Canary",
        subtitle="Thực hiện truy cập ngoài đường hầm",
        items=[
            "Hacker mở Chrome/Edge trên máy vật lý",
            "Dán URL: http://192.168.10.130:8080/...",
            "Request HTTP đi thẳng từ IP thật!",
            "Không đi qua Proxy / VPN ẩn danh",
            "Mục tiêu: Kích hoạt khóa AWS / DB SSO"
        ],
        border_color=RED,
        title_color=RED
    )

    draw_arrow(ax, 0.32, 0.67, 0.39, 0.67, label="HTTP GET\nPort 8080", color=PURPLE)

    # Khối 2: Canary Webhook Server
    draw_card(
        ax, 0.39, 0.48, 0.30, 0.38,
        title="2. Canary Webhook Server",
        subtitle="Máy chủ bẫy mồi lắng nghe port 8080",
        items=[
            "Tiếp nhận kết nối TCP từ trình duyệt",
            "Trích xuất IP NGUỒN THẬT (Real IP):",
            "  -> client_address[0] = 192.168.10.1",
            "Trích xuất User-Agent thật của hacker",
            "Xác định chính xác loại Token bị lộ",
            "Gửi tín hiệu khẩn cấp về SOAR Enforcer"
        ],
        border_color=PURPLE,
        title_color=PURPLE
    )

    draw_arrow(ax, 0.69, 0.67, 0.76, 0.67, label="Trả về trang giả\n403 Forbidden", color=GREEN)

    # Khối 3: Đánh lừa phản hồi (Deceptive Camouflage)
    draw_card(
        ax, 0.76, 0.48, 0.20, 0.38,
        title="3. Ngụy trang phản hồi",
        subtitle="Đánh lạc hướng hacker",
        items=[
            "Trả mã phản hồi HTTP 200/403",
            "Hiển thị trang Corporate SSO",
            "Báo lỗi 'Cert Invalid'",
            "Hacker tin là lỗi kết nối",
            "Không hề biết mình đã lộ IP!"
        ],
        border_color=GREEN,
        title_color=GREEN
    )

    # Cửa sổ Console hiển thị kết quả khử ẩn danh
    terminal_lines = [
        ("=======================================================================", RED),
        ("[!] [SOAR ACTIVE DEFENSE - KHU AN DANH THANH CONG!]", GREEN),
        ("[-] Loai bay: Khoa AWS Credentials trong /root/.aws/credentials (T1552.001)", GOLD),
        ("[*] IP THAT CUA HACKER (Real IP): 192.168.10.1", RED),
        ("[*] Cong cu / User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0", CYAN),
        ("[*] Duong dan bi goi: /canary/aws_verify?token=canary_aws_8892", TEXT_WHITE),
        ("[+] Trang thai: DA VO HIEU HOA HOAN TOAN LOP VO BOC VPN/PROXY CUA HACKER!", GREEN),
        ("=======================================================================", RED)
    ]
    draw_terminal(ax, 0.04, 0.07, 0.62, 0.36, "Console SOAR Server: Bat tron danh tinh thuc", terminal_lines)

    # Khối giải thích điểm đột phá
    draw_card(
        ax, 0.68, 0.07, 0.28, 0.36,
        title="Ưu thế tuyệt đối:",
        subtitle="Vượt qua mọi lớp che giấu",
        items=[
            "Hacker có thể fake IP khi SSH",
            "Nhưng khi verify Token ngoài web,",
            "hacker sẽ để lộ IP vật lý thật!",
            "Cung cấp bằng chứng pháp lý",
            "và IP mục tiêu chuẩn xác cho",
            "hệ thống phòng thủ SOAR!"
        ],
        border_color=CYAN,
        title_color=CYAN
    )

    plt.tight_layout()
    img_path = os.path.join(OUTPUT_DIR, "03_deanonymization_canary.png")
    plt.savefig(img_path, facecolor=BG_COLOR)
    plt.close()
    print(f"[+] Đã tạo ảnh 3: {img_path}")


# ==============================================================================
# ẢNH 4: GIAI ĐOẠN 4 - PHẢN ỨNG SOAR & TCP TARPIT (ACTIVE CONTAINMENT)
# ==============================================================================
def create_image_4():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header
    ax.text(0.04, 0.94, "GIAI ĐOẠN 4: SOAR PHẢN ỨNG CHỦ ĐỘNG, TCP TARPIT & ĐIỀU TRA",
            fontsize=17, fontweight='bold', color=GREEN, transform=ax.transAxes)
    ax.text(0.04, 0.90, "Cơ chế: Giam lỏng Socket Tarpit (3s/byte), Trinh sát ngược AbuseIPDB/Shodan và đẩy nút chặn Telegram",
            fontsize=11, color=TEXT_MUTED, transform=ax.transAxes)
    
    # Badge SOAR
    ax.text(0.80, 0.93, "SOAR AUTOMATED RESPONSE", fontsize=10, fontweight='bold', color=GREEN,
            transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="#13381e", edgecolor=GREEN))

    # Khối 1: Giam lỏng TCP Tarpit
    draw_card(
        ax, 0.04, 0.48, 0.28, 0.38,
        title="1. Giam lỏng TCP Tarpit",
        subtitle="Socket-Level Active Defense",
        items=[
            "Kích hoạt khi phát hiện hành vi nguy cấp",
            "Bóp nghẽn socket: gửi 3 giây / 1 byte",
            "Treo đứng phiên làm việc của hacker",
            "Hacker không gõ lệnh được, không thoát được",
            "Tiêu hao CPU, băng thông & thời gian của bot"
        ],
        border_color=RED,
        title_color=RED
    )

    draw_arrow(ax, 0.32, 0.67, 0.39, 0.67, label="Kích hoạt song song\nOSINT & Sandbox", color=CYAN)

    # Khối 2: Trinh sát ngược & Phân tích Payload
    draw_card(
        ax, 0.39, 0.48, 0.30, 0.38,
        title="2. Trinh sát ngược & Cách ly",
        subtitle="Automated Threat Intelligence",
        items=[
            "Tra cứu AbuseIPDB: Tính điểm độc hại",
            "Tra cứu Shodan: Quét các cổng hacker mở",
            "GeoIP: Định vị vị trí địa lý & ISP",
            "Sandbox Quarantine: Thu hồi malware,",
            "tước quyền thực thi (0444) & quét VT"
        ],
        border_color=CYAN,
        title_color=CYAN
    )

    draw_arrow(ax, 0.69, 0.67, 0.76, 0.67, label="Đẩy cảnh báo\nInteractive API", color=GREEN)

    # Khối 3: Telegram SOAR Bot
    draw_card(
        ax, 0.76, 0.48, 0.20, 0.38,
        title="3. SOC Telegram Bot",
        subtitle="Trợ lý phản ứng 1-Click",
        items=[
            "Bắn thông báo tức thì",
            "Gửi kèm các nút bấm:",
            "  [ Chặn IP 3600s ]",
            "  [ Trinh sát OSINT ]",
            "  [ Bỏ qua cảnh báo ]",
            "Chuyên viên SOC xử lý",
            "ngay trên điện thoại!"
        ],
        border_color=GREEN,
        title_color=GREEN
    )

    # Cửa sổ Telegram giả lập
    telegram_lines = [
        ("[!] [CANH BAO TINH BAO SOAR] PHAT HIEN SU CO AN NINH", RED),
        ("[-] Ma su co: INC-CANARY-8892 | Muc do: CRITICAL", GOLD),
        ("[*] Hanh vi: Hacker sap bay Canary Khu an danh (T1552.001)", TEXT_WHITE),
        ("[*] IP THAT: 192.168.10.1 (Local Host) | ISP: Private Subnet", CYAN),
        ("[*] Diem doc hai (AbuseIPDB): 100% | Phan loai: Advanced Attacker", RED),
        ("[+] Bien phap da thi hanh: Da kich hoat TCP Tarpit giam long socket", GREEN),
        ("----------------------------------------------------------------", TEXT_MUTED),
        ("[>>] [CHAN IP 3600S]    [>>] [TRINH SAT NGUOC OSINT]    [>>] [BO QUA]", PURPLE)
    ]
    draw_terminal(ax, 0.04, 0.07, 0.64, 0.36, "Telegram SOC Bot Alert (Giao diện điều hành an ninh)", telegram_lines)

    # Khối tổng kết giá trị đồ án
    draw_card(
        ax, 0.70, 0.07, 0.26, 0.36,
        title="Giá trị cốt lõi:",
        subtitle="Đồ án Active Defense Honeynet",
        items=[
            "Tự động hóa 100% từ Bẫy ->",
            "Khử ẩn danh -> Điều tra ->",
            "Giam lỏng -> Phản ứng.",
            "Biến thế bị động thành",
            "thế chủ động dẫn dắt đối thủ",
            "trong trận địa phòng thủ an ninh!"
        ],
        border_color=GOLD,
        title_color=GOLD
    )

    plt.tight_layout()
    img_path = os.path.join(OUTPUT_DIR, "04_soar_tarpit_response.png")
    plt.savefig(img_path, facecolor=BG_COLOR)
    plt.close()
    print(f"[+] Đã tạo ảnh 4: {img_path}")


if __name__ == "__main__":
    print("[*] Đang khởi tạo và vẽ 4 ảnh kiến trúc Active Honeypot...")
    create_image_1()
    create_image_2()
    create_image_3()
    create_image_4()
    print("[+] Hoàn thành toàn bộ 4 ảnh tại:", OUTPUT_DIR)
