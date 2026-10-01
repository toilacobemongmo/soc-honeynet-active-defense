"""
Chapter 4: HIỆN THỰC HÓA VÀ MÃ NGUỒN CÁC PHÂN HỆ (8-10 trang)
Mô tả chi tiết cấu hình Honeypot, mã nguồn các module Python tự phát triển,
giải thích từng hàm, lớp, cấu trúc dữ liệu và sự phối hợp giữa các phân hệ.
"""

from docx.shared import Pt


def build_chapter4(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]
    add_code_snippet = helpers["add_code_snippet"]

    add_custom_heading(doc, "CHƯƠNG 4: HIỆN THỰC HÓA VÀ MÃ NGUỒN CÁC PHÂN HỆ", level=1)

    # 4.1
    add_custom_heading(doc, "4.1 Môi trường Triển khai và Cấu hình Tùy biến Cowrie Honeypot", level=2)
    add_body_paragraph(doc, "Hệ thống được triển khai trên nền tảng máy chủ Linux Ubuntu Server 22.04 LTS (64-bit). Nhằm biến Cowrie từ một máy bẫy mặc định dễ bị phát hiện thành một máy chủ sản xuất thực tế (Realistic Production Server), các cấu hình tùy biến chuyên sâu đã được thực hiện:")
    add_body_paragraph(doc, "1. Chuyển dịch Cổng Dịch vụ (Port Redirection): Cổng SSH thực tế dùng để quản trị máy chủ được đổi từ cổng 22 sang cổng bí mật 54322. Cổng mặc định 22 của hệ thống được chuyển hướng (NAT Port Forwarding) về cổng 2222 của Cowrie Honeypot bằng lệnh iptables:")
    add_code_snippet(doc, "iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222", caption="Lệnh iptables chuyển hướng lưu lượng SSH từ cổng 22 sang cổng bẫy 2222")
    add_body_paragraph(doc, "2. Cấu hình Tùy biến File 'cowrie.cfg': Thay đổi Hostname mặc định từ 'svr04' thành 'corp-db-master-01' và giả lập phiên bản OpenSSH chuẩn của Ubuntu (OpenSSH_8.9p1 Ubuntu-3ubuntu0.4) nhằm đánh lừa các công cụ quét chuyên nghiệp như Nmap OS detection:")
    add_code_snippet(doc, """[honeypot]
hostname = corp-db-master-01
log_path = var/log/cowrie
download_path = var/lib/cowrie/downloads
contents_path = share/cowrie/contents
txtcmds_path = share/cowrie/txtcmds

[ssh]
enabled = true
listen_endpoints = tcp:2222:interface=0.0.0.0
version = SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4

[output_json]
enabled = true
logfile = var/log/cowrie/cowrie.json""", caption="Trích đoạn cấu hình tùy biến máy bẫy trong tệp tin cowrie.cfg")

    # 4.2
    add_custom_heading(doc, "4.2 Chi tiết Mã nguồn Phân hệ Thu thập Log Streaming (cowrie_listener.py)", level=2)
    add_body_paragraph(doc, "Phân hệ 'CowrieLogListener' được hiện thực hóa với lớp đối tượng chuyên trách theo dõi sự thay đổi của tệp tin log 'cowrie.json'. Khi phát hiện có dòng dữ liệu mới, module lập tức chuyển đổi chuỗi JSON thành dictionary và gọi hàm callback bất đồng bộ:")
    add_code_snippet(doc, """class CowrieLogListener:
    def __init__(self, log_file_path: str, poll_interval: float = 0.5):
        self.log_file_path = log_file_path
        self.poll_interval = poll_interval
        self._running = False
        self._last_position = 0

    def start(self, callback: Callable[[dict], None]) -> None:
        self._running = True
        with open(self.log_file_path, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END) # Nhảy tới cuối tệp để đón log mới
            while self._running:
                line = f.readline()
                if not line:
                    time.sleep(self.poll_interval)
                    continue
                try:
                    event = json.loads(line.strip())
                    callback(event)
                except json.JSONDecodeError:
                    continue""", caption="Hiện thực hóa cơ chế Streaming Log Parser trong core/cowrie_listener.py")

    # 4.3
    add_custom_heading(doc, "4.3 Chi tiết Mã nguồn Động cơ Tương quan Sự kiện (correlation_engine.py)", level=2)
    add_body_paragraph(doc, "Lớp 'EventCorrelationEngine' cài đặt cấu trúc dữ liệu ThreatAlert cùng thuật toán Cửa sổ Thời gian Trượt. Module quản lý bộ đếm các lần đăng nhập thất bại theo từng IP nguồn và kiểm tra thời gian tồn tại trong danh sách để phát hiện tấn công brute-force chuẩn xác:")
    add_code_snippet(doc, """# Xử lý phát hiện Brute Force T1110.001
if eventid == "cowrie.login.failed":
    self.failed_logins[src_ip] = [
        t for t in self.failed_logins[src_ip] if now - t <= self.window_seconds
    ]
    self.failed_logins[src_ip].append(now)

    if len(self.failed_logins[src_ip]) >= self.brute_force_threshold:
        count = len(self.failed_logins[src_ip])
        self.failed_logins[src_ip].clear()
        return ThreatAlert(
            alert_id=f"ALT-BRUTE-{int(now)}",
            rule_name="Dò quét mật khẩu diện rộng (SSH Brute Force Attack)",
            mitre_technique_id="T1110.001",
            mitre_technique_name="Brute Force: Password Guessing",
            severity="HIGH",
            source_ip=src_ip,
            timestamp=timestamp,
            details={"failed_attempts": count, "target_user": username},
            recommended_action="tarpit_and_block",
        )""", caption="Đoạn mã thuật toán cửa sổ trượt trong core/correlation_engine.py")

    # 4.4
    add_custom_heading(doc, "4.4 Chi tiết Mã nguồn Phân hệ Trinh sát ngược Kẻ tấn công (reverse_intel.py)", level=2)
    add_body_paragraph(doc, "Lớp 'ReverseIntelligenceEngine' tổng hợp các hàm trinh sát đa nguồn: 'lookup_geoip', 'lookup_abuseipdb', 'lookup_shodan' và 'safe_reverse_port_scan'. Hàm quét cổng ngược sử dụng socket TCP với thời gian chờ 300ms, kết hợp hàm '_classify_threat' để suy luận hình thái đối thủ:")
    add_code_snippet(doc, """def safe_reverse_port_scan(self, ip: str, ports: Optional[List[int]] = None) -> List[int]:
    if ports is None:
        ports = [21, 22, 23, 80, 443, 1080, 3128, 3389, 8080, 8888]
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        try:
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
        except Exception:
            pass
        finally:
            s.close()
    return open_ports""", caption="Hiện thực hóa quét cổng ngược an toàn trong core/reverse_intel.py")

    # 4.5
    add_custom_heading(doc, "4.5 Chi tiết Mã nguồn Bẫy mồi Honeytoken & Khử ẩn danh (honeytoken_manager.py)", level=2)
    add_body_paragraph(doc, "Lớp 'HoneytokenManager' tự động sinh các tệp tin giả lập nhạy cảm có gắn mã nhận dạng duy nhất (UUID Canary Tokens). Khi kẻ tấn công kích hoạt Webhook, hàm 'process_beacon_callback' bóc tách các trường HTTP Header để lấy IP thật của kẻ tấn công:")
    add_code_snippet(doc, """def process_beacon_callback(self, token_id: str, request_headers: Dict, real_ip: str) -> Dict:
    token_info = self.active_tokens.get(token_id, {})
    token_info["status"] = "TRIGGERED"
    token_info["trigger_ip"] = real_ip
    token_info["user_agent"] = request_headers.get("User-Agent", "Unknown")

    return {
        "alert": "HONEYTOKEN_TRIGGERED",
        "severity": "CRITICAL",
        "message": f"Kẻ tấn công đã mang tài liệu bẫy ({token_info.get('type')}) về máy thật để mở!",
        "attacker_real_ip": real_ip,
        "attacker_fingerprint": request_headers.get("User-Agent"),
        "token_details": token_info,
    }""", caption="Hiện thực hóa cơ chế khử ẩn danh kẻ tấn công trong core/honeytoken_manager.py")

    # 4.6
    add_custom_heading(doc, "4.6 Chi tiết Mã nguồn Phân tích Mã độc & Tra cứu VirusTotal (payload_analyzer.py)", level=2)
    add_body_paragraph(doc, "Phân hệ 'PayloadAnalyzer' sử dụng thư viện hashlib để tính toán mã băm SHA256 và MD5, đồng thời sử dụng biểu thức chính quy (Regex) quét qua chuỗi nhị phân để trích xuất địa chỉ IP C2 và URL máy chủ tải mã độc giai đoạn 2:")
    add_code_snippet(doc, """def _extract_static_iocs(self, content: bytes) -> Dict[str, List[str]]:
    text = content.decode("utf-8", errors="ignore")
    ip_pattern = r"\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b"
    url_pattern = r"https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+[^\\s]*"
    
    ips = list(set(re.findall(ip_pattern, text)))
    urls = list(set(re.findall(url_pattern, text)))
    signatures = []
    if "xmrig" in text.lower():
        signatures.append("Cryptocurrency Miner (XMRig / Monero)")
    if "/bin/busybox" in text or "dvrHelper" in text or "mirai" in text.lower():
        signatures.append("IoT Botnet Variant (Mirai / Gafgyt)")
    return {"ips": ips, "urls": urls, "signatures": signatures}""", caption="Trích xuất IOCs tĩnh và chữ ký mã độc trong core/payload_analyzer.py")

    # 4.7
    add_custom_heading(doc, "4.7 Chi tiết Mã nguồn Động cơ SOAR Thực thi Phản ứng (soar_enforcer.py)", level=2)
    add_body_paragraph(doc, "Lớp 'SOAREnforcer' quản lý việc chặn IP trên Tường lửa và điều hướng kết nối vào Tarpit. Module hỗ trợ kiểm tra danh sách trắng (Whitelist) để chống tự khóa nhầm máy quản trị viên và tự động xuất bản Threat Feed:")
    add_code_snippet(doc, """def block_ip(self, ip: str, duration_sec: int = 3600, reason: str = "Brute Force") -> Dict:
    if ip in self.whitelist:
        return {"status": "skipped", "message": "IP nằm trong Whitelist an toàn"}
    if "linux" in self.os_type:
        subprocess.run(["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"], check=True)
    self.blocked_ips[ip] = time.time() + duration_sec
    self._append_to_ioc_feed(ip, reason)
    return {"status": "success", "action": "FIREWALL_BLOCK", "ip": ip}

def tarpit_ip(self, ip: str) -> Dict:
    if "linux" in self.os_type:
        cmd = f"iptables -t nat -A PREROUTING -p tcp -s {ip} --dport 2222 -j REDIRECT --to-ports 22222"
        subprocess.run(cmd.split(), capture_output=True)
    return {"status": "success", "action": "TARPIT_RESOURCE_EXHAUSTION", "ip": ip}""", caption="Hiện thực hóa cơ chế chặn Firewall và Tarpit trong core/soar_enforcer.py")

    # 4.8
    add_custom_heading(doc, "4.8 Chi tiết Mã nguồn Telegram SOAR Bot tương tác 2 chiều (telegram_soar_bot.py)", level=2)
    add_body_paragraph(doc, "Khác với các script thông báo một chiều, Telegram SOAR Bot được cài đặt luồng chạy nền (Background Polling Thread) để đón nhận các sự kiện bấm nút 'callback_query' từ phía Chuyên viên SOC và phản hồi kết quả tức thì:")
    add_code_snippet(doc, """reply_markup = {
    "inline_keyboard": [
        [
            {"text": "🔍 Trinh sát ngược OSINT", "callback_data": f"recon:{ip}"},
            {"text": "⏳ Đưa vào Tarpit", "callback_data": f"tarpit:{ip}"},
        ],
        [
            {"text": "⛔ Chặn Firewall tức thì", "callback_data": f"block:{ip}"},
            {"text": "🔓 Mở khóa IP", "callback_data": f"unblock:{ip}"},
        ],
    ]
}
payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "HTML", "reply_markup": json.dumps(reply_markup)}""", caption="Xây dựng giao diện nút bấm tương tác Inline Keyboard trong core/telegram_soar_bot.py")

    # 4.9
    add_custom_heading(doc, "4.9 Tích hợp Hệ thống qua Phân hệ Điều phối Trung tâm (main.py)", level=2)
    add_body_paragraph(doc, "Tệp tin 'main.py' đóng vai trò là Orchestrator trung tâm, nạp tệp tin cấu hình YAML, liên kết toàn bộ 7 phân hệ với nhau và điều phối dữ liệu từ sự kiện log tới hành động SOAR.")
    add_body_paragraph(doc, "Bảng 4.1 tổng kết trách nhiệm và sự liên kết giữa các module trong hệ sinh thái:")

    modules_headers = ["Module Tệp tin", "Trách nhiệm Kỹ thuật Cốt lõi", "Thư viện / Giao thức Chính Sử dụng"]
    modules_data = [
        ["core/cowrie_listener.py", "Theo dõi và phân tích luồng JSON thời gian thực từ cowrie.json", "json, os, time, threading"],
        ["core/correlation_engine.py", "Thuật toán cửa sổ trượt, tương quan sự kiện và ánh xạ MITRE ATT&CK", "dataclasses, collections, datetime"],
        ["core/reverse_intel.py", "Trinh sát ngược OSINT, tra cứu GeoIP, AbuseIPDB, Shodan và quét cổng", "socket, requests, ip-api, AbuseIPDB API"],
        ["core/honeytoken_manager.py", "Sinh file bẫy mồi (AWS, Bash, SQL) và xử lý khử ẩn danh Hacker", "uuid, os, hashlib, HTTP Webhook"],
        ["core/payload_analyzer.py", "Phân tích tĩnh mã độc, trích xuất IOCs IP/URL và tra cứu VirusTotal", "hashlib, re, VirusTotal v3 API"],
        ["core/soar_enforcer.py", "Thực thi chặn iptables/nftables, điều hướng Tarpit và quản lý Whitelist", "subprocess, platform, iptables, nat"],
        ["core/telegram_soar_bot.py", "Gửi thẻ cảnh báo và xử lý tương tác nút bấm 2 chiều từ điện thoại", "Telegram Bot API, inline_keyboard, threading"],
        ["main.py", "Khởi tạo, nạp cấu hình YAML và điều phối luồng xử lý toàn hệ thống", "pyyaml, sys, logging"],
    ]
    add_styled_table(doc, modules_headers, modules_data, caption="Bảng 4.1: Danh sách các Module mã nguồn và Trách nhiệm xử lý trong Hệ sinh thái")

    doc.add_page_break()
