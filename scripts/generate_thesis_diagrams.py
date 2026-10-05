"""
Script: generate_thesis_diagrams.py
Mục đích: Tạo 4 sơ đồ học thuật chuyên sâu chuẩn báo cáo đồ án tốt nghiệp theo yêu cầu:
1. Sơ đồ cơ chế Cửa sổ thời gian trượt (Sliding Time Window Diagram)
2. Lưu đồ giải thuật Động cơ Tương quan (Correlation Engine Flowchart - ISO/UML Activity)
3. Sơ đồ chu trình bẫy mồi và Khử ẩn danh (Sequence Diagram - UML Tuần tự)
4. Sơ đồ máy trạng thái phản xạ SOAR & Tarpit (State Machine Diagram)
Độ phân giải: 300 DPI, chuẩn in ấn & chèn slide luận văn.
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

# Cấu hình font và thư mục xuất ảnh
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'Tahoma']
OUTPUT_DIR = os.path.abspath("./reports/images")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# SƠ ĐỒ 1: CƠ CHẾ CỬA SỔ THỜI GIAN TRƯỢT (SLIDING TIME WINDOW)
# ==============================================================================
def draw_sliding_window():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300, facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề
    ax.text(50, 93, "SƠ ĐỒ THUẬT TOÁN CỬA SỔ THỜI GIAN TRƯỢT (SLIDING TIME WINDOW)",
            fontsize=14, fontweight='bold', ha='center', color='#111111')
    ax.text(50, 88, "Phát hiện tấn công dò quét mật khẩu (SSH Brute-force: T1110.001) trong correlation_engine.py",
            fontsize=10, ha='center', color='#555555')

    # Trục thời gian nằm ngang (t)
    ax.annotate("", xy=(94, 52), xytext=(6, 52),
                arrowprops=dict(arrowstyle="-|>", color="#212529", lw=2.2, mutation_scale=15))
    ax.text(95, 52, "Thời gian (t)", fontsize=10, fontweight='bold', va='center', color='#111111')

    # Các mốc thời gian sự kiện t1 đến t7
    # t1=15 (bị loại), t2=23 (bị loại), t3=42, t4=50, t5=58, t6=68, t7=78
    events = [
        (15, "t1", False, "10:00:05\nFail #1"),
        (23, "t2", False, "10:00:18\nFail #2"),
        (42, "t3", True, "10:01:05\nFail #3"),
        (51, "t4", True, "10:01:14\nFail #4"),
        (60, "t5", True, "10:01:25\nFail #5"),
        (70, "t6", True, "10:01:38\nFail #6"),
        (80, "t7", True, "10:01:52\nFail #7 (Hiện tại)")
    ]

    # Vẽ vạch và điểm mốc sự kiện
    for x_pos, label, is_inside, desc in events:
        color = "#0d6efd" if is_inside else "#adb5bd"
        dot_color = "#dc3545" if is_inside else "#ced4da"
        
        # Vạch đứng trên trục t
        ax.plot([x_pos, x_pos], [49, 55], color=color, lw=1.8)
        
        # Điểm tròn sự kiện
        circle = patches.Circle((x_pos, 52), 1.2, facecolor=dot_color, edgecolor=color, lw=1.5, zorder=5)
        ax.add_patch(circle)
        
        # Nhãn t_i
        ax.text(x_pos, 45, label, fontsize=9.5, fontweight='bold', ha='center', color=color)
        ax.text(x_pos, 39, desc, fontsize=8, ha='center', color="#495057", linespacing=1.2)

    # KHUNG CỬA SỔ THỜI GIAN TRƯỢT W = 60s (Từ x=36 đến x=86)
    win_box = patches.FancyBboxPatch(
        (35, 33), 51, 38,
        boxstyle="round,pad=0.5,rounding_size=1.5",
        facecolor="#e7f1ff", edgecolor="#0d6efd", lw=2.2, linestyle="--", alpha=0.85
    )
    ax.add_patch(win_box)

    # Nhãn kích thước cửa sổ trượt
    ax.text(60.5, 74, "KHUNG CỬA SỔ TRƯỢT (W = 60 Giây)", fontsize=11, fontweight='bold', ha='center', color='#084298')
    ax.text(60.5, 68, "Bộ đệm lưu vết: deque([t3, t4, t5, t6, t7])", fontsize=9.2, ha='center', color='#052c65')

    # Vùng bị loại bỏ bên ngoài cửa sổ (Bên trái)
    ax.text(19, 65, "[ VÙNG BỊ LOẠI BỎ ]", fontsize=9.5, fontweight='bold', ha='center', color='#6c757d')
    ax.text(19, 60, "Điều kiện: (t_hiện_tại - t_i) > 60s\n-> popleft() giải phóng bộ đệm", 
            fontsize=8.5, ha='center', color='#6c757d')
    # Mũi tên gạch chéo loại bỏ
    ax.annotate("", xy=(23, 56), xytext=(15, 63),
                arrowprops=dict(arrowstyle="->", color="#dc3545", lw=1.5, linestyle=":"))

    # ĐIỀU KIỆN KÍCH HOẠT VƯỢT NGƯỠNG (THRESHOLD T = 5)
    alert_box = patches.FancyBboxPatch(
        (40, 10), 41, 15,
        boxstyle="round,pad=0.5,rounding_size=1.0",
        facecolor="#fff5f5", edgecolor="#dc3545", lw=1.8
    )
    ax.add_patch(alert_box)

    # Mũi tên từ cửa sổ trượt xuống hộp Alert
    ax.annotate(
        "", xy=(60.5, 25), xytext=(60.5, 33),
        arrowprops=dict(facecolor="#dc3545", edgecolor="#dc3545", width=2.0, headwidth=7, headlength=7)
    )
    
    ax.text(60.5, 21, "ĐIỀU KIỆN THOẢ MÃN: Count(Failed Logins) = 5 >= Threshold (T=5)", 
            fontsize=9.2, fontweight='bold', ha='center', color='#b02a37')
    ax.text(60.5, 14, "-> KÍCH HOẠT ALERT MITRE ATT&CK: T1110.001 (Brute Force)\n-> Gửi tín hiệu sang SOAR Enforcer & Xóa bộ đệm (Reset Window)", 
            fontsize=8.5, ha='center', color='#333333', linespacing=1.3)

    # Khung bao viền trang nhã
    outer = patches.Rectangle((2, 3), 96, 94, facecolor="none", edgecolor="#dee2e6", lw=1.2)
    ax.add_patch(outer)

    img_path = os.path.join(OUTPUT_DIR, "01_sliding_time_window.png")
    plt.tight_layout()
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"[+] Đã vẽ xong Sơ đồ 1: {img_path}")


# ==============================================================================
# SƠ ĐỒ 2: LƯU ĐỒ GIẢI THUẬT ĐỘNG CƠ TƯƠNG QUAN (CORRELATION ENGINE FLOWCHART)
# ==============================================================================
def draw_correlation_flowchart():
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300, facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề
    ax.text(50, 96, "LƯU ĐỒ GIẢI THUẬT ĐỘNG CƠ TƯƠNG QUAN (CORRELATION ENGINE FLOWCHART)",
            fontsize=14, fontweight='bold', ha='center', color='#111111')
    ax.text(50, 92.5, "Chuẩn UML Activity / ISO thể hiện logic rẽ nhánh xử lý sự kiện trong correlation_engine.py",
            fontsize=9.5, ha='center', color='#555555')

    def draw_box(x, y, w, h, text, bg="#f8f9fa", border="#212529", font_size=8.5, font_bold=False):
        b = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.3,rounding_size=0.8",
            facecolor=bg, edgecolor=border, lw=1.4
        )
        ax.add_patch(b)
        weight = 'bold' if font_bold else 'normal'
        ax.text(x + w/2, y + h/2, text, fontsize=font_size, fontweight=weight, ha='center', va='center', color='#111111')

    def draw_diamond(cx, cy, w, h, text, bg="#fff3cd", border="#ffc107"):
        # Vẽ hình thoi quyết định
        diamond = patches.Polygon(
            [[cx, cy + h/2], [cx + w/2, cy], [cx, cy - h/2], [cx - w/2, cy]],
            closed=True, facecolor=bg, edgecolor=border, lw=1.6
        )
        ax.add_patch(diamond)
        ax.text(cx, cy, text, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#664d03')

    # 1. Start Node
    draw_box(40, 83, 20, 6, "START: Nhận sự kiện\nEvent JSON từ Honeypot", bg="#e8f5e9", border="#2e7d32", font_bold=True)

    # Mũi tên xuống Hình thoi kiểm tra
    ax.annotate("", xy=(50, 75), xytext=(50, 83),
                arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.8, mutation_scale=12))

    # 2. Khối quyết định chính (Hình thoi)
    draw_diamond(50, 69, 26, 12, "Loại sự kiện\neventid là gì?")

    # 4 NHÁNH RẼ: login.failed | login.success | command.input | file_download
    xs = [14, 38, 62, 86]
    labels = [
        "cowrie.login.failed",
        "cowrie.login.success",
        "cowrie.command.input",
        "cowrie.session.file_download"
    ]

    # Kẻ mũi tên từ hình thoi ra 4 nhánh
    # Nhánh 1: sang trái (x=14)
    ax.plot([37, 14, 14], [69, 69, 58], color="#212529", lw=1.5)
    ax.annotate("", xy=(14, 57), xytext=(14, 58), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.5))
    ax.text(23, 70.5, "1. login.failed", fontsize=8, fontweight='bold', color="#dc3545")

    # Nhánh 2: x=38
    ax.plot([43, 38, 38], [63, 63, 58], color="#212529", lw=1.5)
    ax.annotate("", xy=(38, 57), xytext=(38, 58), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.5))
    ax.text(35, 64, "2. login.success", fontsize=8, fontweight='bold', color="#0d6efd")

    # Nhánh 3: x=62
    ax.plot([57, 62, 62], [63, 63, 58], color="#212529", lw=1.5)
    ax.annotate("", xy=(62, 57), xytext=(62, 58), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.5))
    ax.text(63, 64, "3. command.input", fontsize=8, fontweight='bold', color="#d63384")

    # Nhánh 4: sang phải (x=86)
    ax.plot([63, 86, 86], [69, 69, 58], color="#212529", lw=1.5)
    ax.annotate("", xy=(86, 57), xytext=(86, 58), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.5))
    ax.text(76, 70.5, "4. file_download", fontsize=8, fontweight='bold', color="#fd7e14")

    # XỬ LÝ NHÁNH 1 (login.failed)
    draw_box(4, 47, 20, 10, "Tính Cửa sổ trượt W=60s\nLoại bỏ sự kiện quá hạn\nĐếm Count(IP)", bg="#f8f9fa")
    draw_diamond(14, 38, 16, 8, "Count >= 5?", bg="#fff3cd", border="#ffc107")
    ax.annotate("", xy=(14, 42), xytext=(14, 47), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))
    
    draw_box(4, 23, 20, 9, "Sinh ThreatAlert:\nT1110.001 Brute-Force\nMức độ: HIGH\nReset bộ đệm", bg="#fff5f5", border="#dc3545", font_bold=True)
    ax.annotate("", xy=(14, 32), xytext=(14, 34), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))
    ax.text(16, 33, "Đúng", fontsize=7.5, color="#dc3545", fontweight='bold')

    # XỬ LÝ NHÁNH 2 (login.success)
    draw_box(28, 47, 20, 10, "Ghi nhận chiếm quyền\n(Initial Access)\nĐổi trạng thái:\nSilent Monitoring", bg="#f0f7ff")
    draw_box(28, 23, 20, 9, "Sinh ThreatAlert:\nT1078 Valid Accounts\nMức độ: MEDIUM\nTheo dõi phiên VFS", bg="#f0f7ff", border="#0d6efd", font_bold=True)
    ax.annotate("", xy=(38, 32), xytext=(38, 47), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))

    # XỬ LÝ NHÁNH 3 (command.input)
    draw_box(52, 47, 20, 10, "Kiểm tra Regex:\ncat / nano / grep\ntrên file Honeytoken?", bg="#fdf2f8")
    draw_diamond(62, 38, 18, 8, "Trúng file mồi?", bg="#fff3cd", border="#ffc107")
    ax.annotate("", xy=(62, 42), xytext=(62, 47), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))

    draw_box(52, 23, 20, 9, "Sinh ThreatAlert:\nT1552.001 Credentials\nMức độ: CRITICAL\nBật bẫy Canary Webhook", bg="#fdf2f8", border="#d63384", font_bold=True)
    ax.annotate("", xy=(62, 32), xytext=(62, 34), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))
    ax.text(64, 33, "Đúng", fontsize=7.5, color="#d63384", fontweight='bold')

    # XỬ LÝ NHÁNH 4 (file_download)
    draw_box(76, 47, 20, 10, "Thu hồi file tải về\nChuyển sang Sandbox\nBăm SHA256", bg="#fff9f2")
    draw_box(76, 23, 20, 9, "Sinh ThreatAlert:\nT1105 Ingress Tool\nMức độ: HIGH\nQuét VirusTotal API", bg="#fff9f2", border="#fd7e14", font_bold=True)
    ax.annotate("", xy=(86, 32), xytext=(86, 47), arrowprops=dict(arrowstyle="-|>", color="#212529", lw=1.2))

    # HỘP KẾT THÚC (END NODE - SOAR ENFORCER)
    draw_box(25, 7, 50, 9, "END: Đóng gói đối tượng ThreatAlert(id, mitre, severity, ip)\n-> Gửi sang SOAR Enforcer thực thi phản ứng", 
             bg="#e8f5e9", border="#2e7d32", font_bold=True, font_size=9.5)

    # Kẻ đường gom 4 nhánh vào END
    for x_out in [14, 38, 62, 86]:
        ax.plot([x_out, x_out, 50], [23, 19, 19], color="#2e7d32", lw=1.2)
    ax.annotate("", xy=(50, 16), xytext=(50, 19), arrowprops=dict(arrowstyle="-|>", color="#2e7d32", lw=1.5))

    # Khung bao viền
    outer = patches.Rectangle((2, 3), 96, 94, facecolor="none", edgecolor="#dee2e6", lw=1.2)
    ax.add_patch(outer)

    img_path = os.path.join(OUTPUT_DIR, "02_correlation_engine_flowchart.png")
    plt.tight_layout()
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"[+] Đã vẽ xong Sơ đồ 2: {img_path}")


# ==============================================================================
# SƠ ĐỒ 3: SƠ ĐỒ TUẦN TỰ KHỬ ẨN DANH (SEQUENCE DIAGRAM)
# ==============================================================================
def draw_sequence_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300, facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề
    ax.text(50, 95, "SƠ ĐỒ TUẦN TỰ KHỬ ẨN DANH CANARY TOKEN (UML SEQUENCE DIAGRAM)",
            fontsize=14, fontweight='bold', ha='center', color='#111111')
    ax.text(50, 91.5, "Chuẩn UML Sequence mô tả 4 bước lật tẩy IP thật của Hacker sử dụng lớp vỏ bọc VPN/Proxy",
            fontsize=9.5, ha='center', color='#555555')

    # 4 Thực thể tham gia theo hàng ngang
    entities = [
        (15, "Attacker\n(Máy thật - Real PC)", "#dc3545", "#fdf2f2"),
        (38, "Attacker\n(VPN / Tor Proxy)", "#6c757d", "#f8f9fa"),
        (63, "Cowrie Honeypot\n(Port 2222)", "#0d6efd", "#f0f7ff"),
        (88, "Canary Webhook\nServer (Port 8080)", "#6f42c1", "#f8f5fc")
    ]

    # Vẽ hộp thực thể và đường Lifeline
    for x_pos, name, border, fill in entities:
        # Hộp thực thể trên cùng
        box = patches.FancyBboxPatch(
            (x_pos - 10, 81), 20, 7.5,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor=fill, edgecolor=border, lw=1.6
        )
        ax.add_patch(box)
        ax.text(x_pos, 84.7, name, fontsize=8.8, fontweight='bold', ha='center', va='center', color='#111111')

        # Lifeline (đường nét đứt dọc)
        ax.plot([x_pos, x_pos], [12, 81], color="#adb5bd", lw=1.2, linestyle="--", zorder=1)

    # BƯỚC 1: VPN -> Cowrie Honeypot (SSH Login & Cat Credentials)
    y1 = 70
    ax.annotate(
        "", xy=(63, y1), xytext=(38, y1),
        arrowprops=dict(arrowstyle="-|>", color="#dc3545", lw=1.8, mutation_scale=12)
    )
    ax.text(50.5, y1 + 2.0, "Bước 1: SSH (Port 2222) qua VPN -> cat /root/.aws/credentials", 
            fontsize=8.5, fontweight='bold', ha='center', color='#b02a37')
    ax.text(50.5, y1 - 2.8, "[Honeypot chỉ nhìn thấy IP giả: 185.220.101.5]", 
            fontsize=7.8, ha='center', color='#6c757d', style='italic')

    # BƯỚC 2: Cowrie -> VPN (Trả về File mồi chứa Token URL)
    y2 = 56
    ax.annotate(
        "", xy=(38, y2), xytext=(63, y2),
        arrowprops=dict(arrowstyle="-|>", color="#0d6efd", lw=1.8, linestyle="--", mutation_scale=12)
    )
    ax.text(50.5, y2 + 2.0, "Bước 2: Trả về nội dung credentials giả nhúng link bẫy:", 
            fontsize=8.5, fontweight='bold', ha='center', color='#084298')
    ax.text(50.5, y2 - 2.8, "http://192.168.10.130:8080/canary/aws_verify?token=canary_aws_8892", 
            fontsize=7.8, ha='center', color='#084298', fontfamily='Consolas')

    # BƯỚC 3: Máy thật -> Webhook Server (Bỏ qua VPN, mở thẳng Chrome)
    y3 = 40
    # Đường kết nối từ x=15 tới x=88 (Vượt mặt VPN!)
    ax.annotate(
        "", xy=(88, y3), xytext=(15, y3),
        arrowprops=dict(arrowstyle="-|>", color="#6f42c1", lw=2.2, mutation_scale=14)
    )
    ax.text(51.5, y3 + 2.5, "Bước 3: Hacker mở Chrome trên Máy thật bấm link -> Gửi HTTP GET trực tiếp (Không qua VPN!)", 
            fontsize=9.0, fontweight='bold', ha='center', color='#59359a')
    ax.text(51.5, y3 - 2.8, "[Kết nối xuất phát trực tiếp từ địa chỉ IP vật lý của máy tấn công]", 
            fontsize=8.0, ha='center', color='#6f42c1', style='italic')

    # BƯỚC 4: Webhook Server xử lý & Chú thích định danh
    y4 = 23
    # Khung chú thích tại Lifeline của Webhook Server
    note_box = patches.FancyBboxPatch(
        (65, y4 - 10), 32, 17,
        boxstyle="round,pad=0.4,rounding_size=0.8",
        facecolor="#f8f5fc", edgecolor="#6f42c1", lw=1.5
    )
    ax.add_patch(note_box)
    ax.text(81, y4 + 5.0, "Bước 4: BÓC TRẦN DANH TÍNH TẠI WEBHOOK", fontsize=8.8, fontweight='bold', ha='center', va='center', color='#59359a')
    ax.plot([66.5, 95.5], [y4 + 3.2, y4 + 3.2], color='#d0c2e8', lw=1.0)
    ax.text(81, y4 + 2.0, "• Real Source IP: 192.168.10.1 (IP Thật)\n• User-Agent: Chrome 120 / Windows 11\n• Phản hồi ngụy trang: 403 Forbidden SSO\n• Gửi tín hiệu kích hoạt khẩn cấp tới SOAR", 
            fontsize=8.0, ha='center', va='top', color='#333333', linespacing=1.35)

    # Đường phản hồi 403 Forbidden về lại Máy thật
    y_ret = y4 - 5.5
    ax.annotate(
        "", xy=(15, y_ret), xytext=(65, y_ret),
        arrowprops=dict(arrowstyle="-|>", color="#198754", lw=1.6, linestyle="--", mutation_scale=11)
    )
    ax.text(40, y_ret + 1.8, "HTTP 200/403 (Đánh lạc hướng, hacker không biết bị lộ)", 
            fontsize=8.2, color='#198754', ha='center', fontweight='bold')

    # Khung bao viền
    outer = patches.Rectangle((2, 3), 96, 94, facecolor="none", edgecolor="#dee2e6", lw=1.2)
    ax.add_patch(outer)

    img_path = os.path.join(OUTPUT_DIR, "03_deanonymization_sequence.png")
    plt.tight_layout()
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"[+] Đã vẽ xong Sơ đồ 3: {img_path}")


# ==============================================================================
# SƠ ĐỒ 4: SƠ ĐỒ MÁY TRẠNG THÁI SOAR & TARPIT (STATE MACHINE DIAGRAM)
# ==============================================================================
def draw_state_machine():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300, facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề
    ax.text(50, 95, "SƠ ĐỒ MÁY TRẠNG THÁI PHẢN XẠ SOAR & TARPIT (UML STATE MACHINE)",
            fontsize=14, fontweight='bold', ha='center', color='#111111')
    ax.text(50, 91.5, "Chuẩn UML Statechart mô tả thuật toán điều phối luồng mạng và mức độ rủi ro tại soar_enforcer.py",
            fontsize=9.5, ha='center', color='#555555')

    def draw_state(x, y, w, h, state_name, subtitle, details, bg, border, title_color):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.2",
            facecolor=bg, edgecolor=border, lw=1.8
        )
        ax.add_patch(rect)
        
        # Tiêu đề trạng thái
        ax.text(x + w/2, y + h - 3.8, state_name, fontsize=10.5, fontweight='bold', ha='center', color=title_color)
        ax.text(x + w/2, y + h - 7.0, subtitle, fontsize=8.2, ha='center', color='#6c757d')
        ax.plot([x + 1.5, x + w - 1.5], [y + h - 8.8, y + h - 8.8], color=border, lw=0.8, alpha=0.5)
        
        for i, d in enumerate(details):
            ax.text(x + 2.5, y + h - 12 - (i * 3.4), f"• {d}", fontsize=8.2, color='#333333')

    # Trạng thái 1: NORMAL
    draw_state(
        x=5, y=52, w=25, h=30,
        state_name="STATE 1: NORMAL",
        subtitle="(Khách vãng lai / Lưu lượng mới)",
        details=[
            "Chưa có tiền sử vi phạm",
            "Mặc định: Cổng 22 được NAT",
            "sang Port 2222 (Cowrie)",
            "Ghi nhật ký tương tác cơ bản",
            "Trạng thái: Cho phép kết nối"
        ],
        bg="#f8f9fa", border="#6c757d", title_color="#495057"
    )

    # Trạng thái 2: SUSPICIOUS
    draw_state(
        x=38, y=52, w=25, h=30,
        state_name="STATE 2: SUSPICIOUS",
        subtitle="(Nghi vấn / Dò mật khẩu)",
        details=[
            "Tích lũy login.failed trong",
            "cửa sổ trượt W = 60 giây",
            "Đang dò quét chưa vượt ngưỡng",
            "Bật chế độ Silent Monitoring",
            "Tăng điểm Abuse Score nội bộ"
        ],
        bg="#fff9f2", border="#fd7e14", title_color="#c45d07"
    )

    # Trạng thái 3: TARPITTED
    draw_state(
        x=71, y=52, w=25, h=30,
        state_name="STATE 3: TARPITTED",
        subtitle="(Giam lỏng / Bóp nghẹt Socket)",
        details=[
            "Kích hoạt khi vượt ngưỡng Brute",
            "hoặc sập bẫy Canary Honeytoken",
            "NAT sang Tarpit (Port 22222)",
            "Gửi nhỏ giọt 3 giây / 1 byte",
            "Treo cứng terminal của hacker"
        ],
        bg="#fff5f5", border="#dc3545", title_color="#b02a37"
    )

    # Trạng thái 4: DROPPED
    draw_state(
        x=38, y=8, w=25, h=30,
        state_name="STATE 4: DROPPED",
        subtitle="(Cách ly tuyệt đối / Chặn IP)",
        details=[
            "Chèn luật Linux Tường lửa:",
            "iptables -I INPUT -s <IP> -j DROP",
            "Từ chối mọi gói tin từ IP thật",
            "Thiết lập TTL Timeout (3600s)",
            "Tự động gỡ bỏ sau khi hết hạn"
        ],
        bg="#f0fdf4", border="#198754", title_color="#146c43"
    )

    # CÁC MŨI TÊN CHUYỂN TRẠNG THÁI (TRANSITIONS)
    # 1 -> 2: Phát hiện thất bại
    ax.annotate(
        "", xy=(38, 67), xytext=(30, 67),
        arrowprops=dict(arrowstyle="-|>", color="#fd7e14", lw=1.8, mutation_scale=12)
    )
    ax.text(34, 69, "Login fail\n(Count < 5)", fontsize=7.8, fontweight='bold', ha='center', color="#c45d07")

    # 2 -> 3: Vượt ngưỡng Brute-force hoặc Canary breached
    ax.annotate(
        "", xy=(71, 67), xytext=(63, 67),
        arrowprops=dict(arrowstyle="-|>", color="#dc3545", lw=1.8, mutation_scale=12)
    )
    ax.text(67, 69, "Count >= 5\nhoặc Canary hit", fontsize=7.8, fontweight='bold', ha='center', color="#b02a37")

    # 3 -> 4: Chuyên viên SOC bấm nút Telegram Block hoặc Auto Policy
    ax.annotate(
        "", xy=(53, 38), xytext=(78, 52),
        arrowprops=dict(arrowstyle="-|>", color="#198754", lw=2.0, mutation_scale=14)
    )
    ax.text(69, 44, "Nút bấm Telegram:\n[ Chặn IP 3600s ]\nhoặc SOAR Rule", 
            fontsize=8.0, fontweight='bold', ha='center', color="#146c43",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#ffffff", edgecolor="#198754", lw=1.0, alpha=0.95))

    # 2 -> 4: Chặn thẳng từ Suspicious nếu điểm AbuseIPDB > 90%
    ax.annotate(
        "", xy=(48, 38), xytext=(48, 52),
        arrowprops=dict(arrowstyle="-|>", color="#dc3545", lw=1.5, mutation_scale=12)
    )
    ax.text(43.5, 45, "AbuseIPDB\n> 90%", fontsize=7.8, fontweight='bold', ha='right', color="#b02a37")

    # 4 -> 1: Hết hạn Timeout (3600s) -> Quay về Normal
    ax.plot([38, 17, 17], [23, 23, 52], color="#6c757d", lw=1.4, linestyle=":")
    ax.annotate(
        "", xy=(17, 52), xytext=(17, 50),
        arrowprops=dict(arrowstyle="-|>", color="#6c757d", lw=1.4, mutation_scale=10)
    )
    ax.text(25, 25, "Hết thời gian chặn (TTL Timeout 3600s)\n-> Gỡ iptables, hoàn nguyên Normal", 
            fontsize=7.8, color="#6c757d", ha='center', style='italic')

    # Khung bao viền
    outer = patches.Rectangle((2, 3), 96, 94, facecolor="none", edgecolor="#dee2e6", lw=1.2)
    ax.add_patch(outer)

    img_path = os.path.join(OUTPUT_DIR, "04_soar_tarpit_state_machine.png")
    plt.tight_layout()
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"[+] Đã vẽ xong Sơ đồ 4: {img_path}")


if __name__ == "__main__":
    print("[*] Đang khởi tạo 4 sơ đồ học thuật chuyên sâu...")
    draw_sliding_window()
    draw_correlation_flowchart()
    draw_sequence_diagram()
    draw_state_machine()
    print("[+] Hoàn tất toàn bộ 4 sơ đồ tại:", OUTPUT_DIR)
