"""
Script: generate_distributed_honeynet_bw_diagram.py
Mục đích: Vẽ sơ đồ kiến trúc Hệ thống Honeynet Phân tán (Distributed Honeynet Architecture).
Phong cách: CHUẨN ĐEN TRẮNG HỌC THUẬT (Monochrome / Black & White Academic Style).
           Không màu mè, bố cục phân tầng mạch lạc, không chồng lấn văn bản.
Đầu ra: reports/images/so_do_honeynet_phan_tan_bw.png
"""

import os
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.abspath("./reports/images")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "so_do_honeynet_phan_tan_bw.png")

# Thiết lập font và trục đồ thị
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans", "Tahoma"]
plt.rcParams["axes.edgecolor"] = "#000000"
plt.rcParams["axes.linewidth"] = 1.2

COLOR_WHITE = "#FFFFFF"
COLOR_LIGHT_GRAY = "#F8F8F8"
COLOR_MID_GRAY = "#EFEFEF"
COLOR_BORDER_GRAY = "#888888"
COLOR_DARK_TEXT = "#111111"
COLOR_BLACK = "#000000"


def draw_card(ax, x, y, w, h, title, subtitle=None, items=None, fill_color=COLOR_WHITE,
              edge_color=COLOR_BLACK, lw=1.3, ls="-", title_size=9.5, item_size=8.2):
    """Vẽ thẻ khối kiến trúc chuẩn khoa học với lề và căn chỉnh chính xác."""
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        facecolor=fill_color,
        edgecolor=edge_color,
        linewidth=lw,
        linestyle=ls,
        transform=ax.transAxes
    )
    ax.add_patch(rect)

    cur_y = y + h - 0.030
    if title:
        ax.text(x + 0.012, cur_y, title, fontsize=title_size, fontweight="bold",
                color=COLOR_BLACK, ha="left", va="center", transform=ax.transAxes)
        cur_y -= 0.024

    if subtitle:
        ax.text(x + 0.012, cur_y, subtitle, fontsize=item_size, fontstyle="italic",
                color="#444444", ha="left", va="center", transform=ax.transAxes)
        cur_y -= 0.024

    if items:
        # Đường kẻ phân cách nhẹ giữa tiêu đề và nội dung
        ax.plot([x + 0.01, x + w - 0.01], [cur_y + 0.008, cur_y + 0.008],
                color=COLOR_BORDER_GRAY, lw=0.6, linestyle=":", transform=ax.transAxes)
        cur_y -= 0.014

        n = len(items)
        avail = cur_y - y - 0.010
        step = min(0.027, avail / max(n, 1))
        for it in items:
            ax.text(x + 0.012, cur_y, f"• {it}", fontsize=item_size, color=COLOR_DARK_TEXT,
                    ha="left", va="center", transform=ax.transAxes)
            cur_y -= step


def draw_section_boundary(ax, x, y, w, h, header_text):
    """Vẽ khung phân vùng logic nét đứt bao quanh một cụm chức năng."""
    boundary = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.01,rounding_size=0.01",
        facecolor="none",
        edgecolor=COLOR_BORDER_GRAY,
        linewidth=1.0,
        linestyle="--",
        transform=ax.transAxes
    )
    ax.add_patch(boundary)
    ax.text(x + 0.015, y + h - 0.022, header_text, fontsize=9.2, fontweight="bold",
            color="#222222", ha="left", va="center",
            bbox=dict(boxstyle="square,pad=0.15", facecolor=COLOR_WHITE, edgecolor="none"),
            transform=ax.transAxes)


def draw_arrow(ax, x1, y1, x2, y2, label=None, label_pos=0.5, label_dy=0.02, ls="-", lw=1.2):
    """Vẽ đường liên kết mũi tên đơn sắc chuẩn mực."""
    ax.annotate(
        "",
        xy=(x2, y2), xycoords="axes fraction",
        xytext=(x1, y1), textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="-|>",
            color=COLOR_BLACK,
            lw=lw,
            linestyle=ls,
            mutation_scale=14
        )
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos
        ly = y1 + (y2 - y1) * label_pos + label_dy
        ax.text(
            lx, ly, label,
            fontsize=7.8,
            fontweight="semibold",
            color=COLOR_BLACK,
            ha="center",
            va="center",
            bbox=dict(boxstyle="square,pad=0.18", facecolor=COLOR_WHITE, edgecolor=COLOR_BORDER_GRAY, lw=0.6),
            transform=ax.transAxes
        )


def generate_bw_diagram():
    fig, ax = plt.subplots(figsize=(16, 9.8), dpi=220)
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)
    ax.axis("off")

    # 1. TIÊU ĐỀ BÁO CÁO KHOA HỌC
    fig.text(0.5, 0.965, "SƠ ĐỒ KIẾN TRÚC MẠNG BẪY MỒI PHÂN TÁN (DISTRIBUTED HONEYNET)",
             fontsize=14.5, fontweight="bold", ha="center", color=COLOR_BLACK)
    fig.text(0.5, 0.942, "Mô hình Cảm biến Biên Đa phân vùng (Edge Sensors) & Trung tâm Thu thập - Phản ứng SOAR",
             fontsize=10.0, fontstyle="italic", ha="center", color="#333333")

    # CỘT 1: NGUỒN ĐE DỌA INTERNET (x = 0.02 .. 0.20, w = 0.18)
    draw_section_boundary(ax, 0.02, 0.14, 0.18, 0.77, "I. KHÔNG GIAN INTERNET & NGUỒN TẤN CÔNG")

    draw_card(ax, 0.03, 0.54, 0.16, 0.33,
              title="Tác nhân Tấn công (Threat Actors)",
              subtitle="Nguồn gốc từ Internet / WAN",
              items=[
                  "Hacker / Nhóm tấn công APT",
                  "Mạng Botnet quét tự động",
                  "Các nút Tor Exit & Anonymizer",
                  "Mã độc lây lan tự động (Worm)"
              ],
              fill_color=COLOR_LIGHT_GRAY, lw=1.2)

    draw_card(ax, 0.03, 0.17, 0.16, 0.33,
              title="Hành vi & Kỹ thuật Xâm nhập",
              subtitle="Chuẩn danh mục MITRE ATT&CK",
              items=[
                  "Dò quét cổng diện rộng (T1046)",
                  "Brute-force SSH liên tục (T1110)",
                  "Truy vết tệp cấu hình AWS (T1552)",
                  "Dò tìm Database nhạy cảm",
                  "Leo thang di chuyển ngang (Lateral)"
              ],
              fill_color=COLOR_LIGHT_GRAY, lw=1.2)

    # CỘT 2: CÁC CẢM BIẾN BIÊN PHÂN TÁN (x = 0.23 .. 0.50, w = 0.27)
    draw_section_boundary(ax, 0.22, 0.14, 0.28, 0.77, "II. HẠ TẦNG CẢM BIẾN BIÊN (EDGE SENSORS)")

    # Sensor DMZ
    draw_card(ax, 0.235, 0.67, 0.25, 0.20,
              title="CẢM BIẾN 1: sensor-dmz-01",
              subtitle="Vùng mạng DMZ Public (192.168.10.0/24)",
              items=[
                  "Dịch vụ: Cowrie SSH Honeypot (Port 2222)",
                  "Bẫy Canary HTTP Webhook (Port 8080)",
                  "Mồi nhử: /root/.bash_history, db_backup.sql",
                  "Thẻ phân vùng: subnet = dmz-public"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # Sensor Cloud AWS
    draw_card(ax, 0.235, 0.43, 0.25, 0.20,
              title="CẢM BIẾN 2: sensor-cloud-aws-02",
              subtitle="VPC Điện toán Đám mây (10.0.1.0/24)",
              items=[
                  "Dịch vụ: Decoy SSH Gateway & Cloud Shell",
                  "Mồi nhử: /root/.aws/credentials",
                  "Honeytoken AWS IAM Access Key & Secret",
                  "Thẻ phân vùng: subnet = cloud-vpc"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # Sensor Internal LAN
    draw_card(ax, 0.235, 0.17, 0.25, 0.20,
              title="CẢM BIẾN 3: sensor-internal-lan-03",
              subtitle="Mạng Nội bộ Doanh nghiệp (172.16.0.0/16)",
              items=[
                  "Dịch vụ: Decoy Lateral Movement (SSH/SMB)",
                  "Giám sát thăm dò nội bộ trái phép",
                  "Active Directory Honeytoken SPN",
                  "Thẻ phân vùng: subnet = internal-corp"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # CỘT 3: KÊNH TRUYỀN DẪN VÀ XÁC THỰC BẢO MẬT (x = 0.52 .. 0.68, w = 0.16)
    draw_section_boundary(ax, 0.515, 0.14, 0.175, 0.77, "III. KÊNH KẾT NỐI BẢO MẬT")

    draw_card(ax, 0.525, 0.56, 0.155, 0.31,
              title="Giao thức REST Ingestion",
              subtitle="Chuẩn truyền tin bảo mật",
              items=[
                  "Giao thức: HTTPS / TLS 1.3",
                  "Header: X-Honeynet-Token",
                  "Kiểm tra tính hợp lệ bằng HMAC",
                  "Endpoint POST: /api/v1/sensor/event",
                  "Endpoint POST: /api/v1/sensor/heartbeat"
              ],
              fill_color=COLOR_MID_GRAY, lw=1.1, ls="-")

    draw_card(ax, 0.525, 0.17, 0.155, 0.35,
              title="Độ tin cậy & Sẵn sàng",
              subtitle="Cơ chế chống thất thoát dữ liệu",
              items=[
                  "Nhịp tim định kỳ (Heartbeat 30s)",
                  "Tự động cảnh báo khi Sensor Offline",
                  "Hàng đợi đệm sự kiện phía Sensor",
                  "Cơ chế Exponential Backoff Retry",
                  "Bảo vệ tính toàn vẹn sự kiện nhật ký"
              ],
              fill_color=COLOR_MID_GRAY, lw=1.1, ls="-")

    # CỘT 4: TRUNG TÂM PHÂN TÍCH & SOAR TRUNG TÂM (x = 0.71 .. 0.98, w = 0.27)
    draw_section_boundary(ax, 0.705, 0.14, 0.275, 0.77, "IV. TRUNG TÂM PHÂN TÍCH & ĐIỀU PHỐI SOAR")

    # Khối 1: Collector
    draw_card(ax, 0.72, 0.67, 0.245, 0.20,
              title="Central Honeynet Collector",
              subtitle="Cổng thu thập dữ liệu tập trung (Port 9090)",
              items=[
                  "Sổ đăng ký Node Registry & Trạng thái sống",
                  "Bóc tách & Chuẩn hóa định dạng JSON",
                  "Deduplication (Khử trùng lặp bản tin)",
                  "Bộ đệm bộ nhớ theo dõi IP tấn công đa vùng"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # Khối 2: Correlation Engine
    draw_card(ax, 0.72, 0.43, 0.245, 0.20,
              title="Động cơ Tương quan Sự kiện",
              subtitle="Định danh TTPs & Phát hiện Cross-Subnet",
              items=[
                  "Luật ALT-DISTRIB (MITRE T1046 Cross Scan)",
                  "Cộng dồn điểm rủi ro: +35 Risk Delta",
                  "Truy vấn tình báo nguồn mở OSINT tự động",
                  "Khử ẩn danh khi kích hoạt Webhook Canary"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # Khối 3: SOAR Enforcer
    draw_card(ax, 0.72, 0.17, 0.245, 0.20,
              title="Động cơ Thực thi SOAR Phân tán",
              subtitle="Phản ứng Chủ động Toàn hệ thống",
              items=[
                  "Tự động chặn IP trên Tường lửa (iptables/netsh)",
                  "Giam lỏng kết nối quét vào Tarpit chậm",
                  "Đồng bộ STIX 2.1 & Tập luật Snort IDS",
                  "Gửi thẻ cảnh báo 2 chiều Telegram SOAR Bot"
              ],
              fill_color=COLOR_WHITE, lw=1.3)

    # CÁC MŨI TÊN KẾT NỐI CHÍNH XÁC (KHÔNG CHỒNG LẤN)
    # 1. Từ Internet quét vào 3 Sensor
    draw_arrow(ax, 0.19, 0.77, 0.235, 0.77, label="SSH Probing", label_pos=0.5, label_dy=0.016)
    draw_arrow(ax, 0.19, 0.53, 0.235, 0.53, label="Cloud Recon", label_pos=0.5, label_dy=0.016)
    draw_arrow(ax, 0.19, 0.27, 0.235, 0.27, label="Lateral Sweep", label_pos=0.5, label_dy=0.016)

    # 2. Từ 3 Sensor gửi về Cột Kênh truyền
    draw_arrow(ax, 0.485, 0.77, 0.525, 0.72, label="POST Event", label_pos=0.45, label_dy=0.016)
    draw_arrow(ax, 0.485, 0.53, 0.525, 0.62)
    draw_arrow(ax, 0.485, 0.27, 0.525, 0.32, label="Heartbeat (30s)", label_pos=0.5, label_dy=0.016)

    # 3. Từ Kênh truyền sang Collector Trung tâm
    draw_arrow(ax, 0.68, 0.72, 0.72, 0.77, label="Token Validated", label_pos=0.5, label_dy=0.016)

    # 4. Luồng xử lý nội bộ tại Trung tâm SOC
    draw_arrow(ax, 0.84, 0.67, 0.84, 0.63, lw=1.4)
    draw_arrow(ax, 0.84, 0.43, 0.84, 0.37, lw=1.4)

    # 5. Phản hồi SOAR (Feedback loop ở đáy biểu đồ, vẽ hoàn toàn thông thoáng ở vùng đáy y = 0.08)
    ax.annotate(
        "Chỉ thị Phản ứng SOAR Toàn cục (Chặn IP Tường lửa Biên + Điều hướng Tarpit)",
        xy=(0.11, 0.14), xycoords="axes fraction",
        xytext=(0.84, 0.07), textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="-|>",
            color=COLOR_BLACK,
            lw=1.3,
            linestyle="-.",
            connectionstyle="arc3,rad=-0.12",
            mutation_scale=14
        ),
        fontsize=8.2,
        fontweight="bold",
        color=COLOR_BLACK,
        ha="center",
        va="center",
        bbox=dict(boxstyle="square,pad=0.2", facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, lw=0.8)
    )

    # CHÚ THÍCH KỸ THUẬT CUỐI TRANG
    caption_text = (
        "Quy ước: Nét liền đại diện cho luồng kết nối TCP/IP & gói tin mạng; "
        "Nét đứt đại diện cho ranh giới phân vùng; "
        "Nét gạch chấm (-.) đại diện cho chu trình phản hồi phòng thủ chủ động SOAR."
    )
    fig.text(0.5, 0.018, caption_text, fontsize=8.6, fontstyle="italic", ha="center", color="#333333")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUTPUT_FILE, dpi=220, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK)
    plt.close()
    print(f"[OK] Sơ đồ đen trắng đã được vẽ thành công và tối ưu bố cục: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_bw_diagram()
