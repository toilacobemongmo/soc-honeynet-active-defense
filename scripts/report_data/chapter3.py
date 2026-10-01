"""
Chapter 3: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-SOC ACTIVE DEFENSE (8-10 trang)
Thiết kế kiến trúc phân lớp, các luồng dữ liệu, thuật toán tương quan cửa sổ trượt,
sơ đồ khối phân hệ trinh sát ngược, honeytokens, sandbox và Telegram SOAR bot.
"""

from docx.shared import Pt


def build_chapter3(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]

    add_custom_heading(doc, "CHƯƠNG 3: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-SOC ACTIVE DEFENSE", level=1)

    # 3.1
    add_custom_heading(doc, "3.1 Yêu cầu Bài toán và Thiết kế Kiến trúc Phân lớp Tổng thể", level=2)
    add_body_paragraph(doc, "Để giải quyết toàn diện bài toán phòng thủ chủ động và vượt qua giới hạn của việc cài đặt ứng dụng đơn thuần, hệ thống được thiết kế theo mô hình Kiến trúc Phân lớp Mini-SOC 5 tầng (5-Layer Architecture). Mỗi tầng đảm nhiệm một vai trò chuyên biệt, độc lập và giao tiếp với nhau thông qua các giao diện lập trình hướng sự kiện (Event-driven Interfaces):")
    add_body_paragraph(doc, "• Tầng 1: Lớp Cảm biến & Đánh lừa Chủ động (Active Deception & Honeypot Layer) - Đóng vai trò là tuyến đầu tiếp nhận tấn công, gồm Cowrie Honeypot tùy biến, hệ thống tệp tin giả lập và các tệp tin mồi nhử Honeytoken có nhúng Webhook Beacon.")
    add_body_paragraph(doc, "• Tầng 2: Lớp Thu thập & Xử lý Luồng Sự kiện (Event Ingestion & Streaming Layer) - Chịu trách nhiệm theo dõi tệp tin nhật ký cowrie.json theo cơ chế stream thời gian thực, chuẩn hóa các trường dữ liệu và bóc tách các tham số IP, tài khoản, câu lệnh và băm tệp tin.")
    add_body_paragraph(doc, "• Tầng 3: Lớp Tương quan & Định danh Tác chiến (Correlation & Threat Intelligence Layer) - 'Bộ não' của hệ thống, chứa thuật toán cửa sổ trượt (Sliding Window Algorithm) để phát hiện Brute-force, tự động ánh xạ sự kiện sang chuẩn MITRE ATT&CK và kích hoạt phân hệ Trinh sát ngược (Reverse Reconnaissance).")
    add_body_paragraph(doc, "• Tầng 4: Lớp Thực thi Phản ứng Tự động (SOAR Enforcement & Active Counter-measure Layer) - Chứa các cơ chế phản đòn hợp pháp: Giam lỏng kết nối vào Tarpit để khóa cứng luồng quét của hacker, tự động cập nhật iptables/nftables để ngăn chặn xâm nhập và xuất bản danh sách đen IOCs.")
    add_body_paragraph(doc, "• Tầng 5: Lớp Giám sát & Điều khiển Tương tác 2 Chiều (Bidirectional Command & Monitoring Layer) - Cung cấp giao diện trực quan thông qua Telegram SOAR Bot với các nút bấm tương tác (Inline Buttons), cho phép chuyên viên SOC can thiệp và kích hoạt các hành động phòng thủ chỉ bằng một chạm.")

    # 3.2
    add_custom_heading(doc, "3.2 Thiết kế Tầng Thu thập & Streaming Sự kiện thời gian thực (Cowrie Event Collector)", level=2)
    add_body_paragraph(doc, "Trong môi trường tác chiến thực tế, một đợt tấn công brute-force có thể tạo ra hàng trăm lượt đăng nhập mỗi giây. Nếu đọc log theo kiểu tuần tự (Polling/Batch), hệ thống sẽ gặp phải độ trễ lớn và tiêu tốn bộ nhớ I/O. Phân hệ Event Collector được thiết kế theo cơ chế Non-blocking Asynchronous Stream:")
    add_body_paragraph(doc, "1. Cơ chế Quản lý Con trỏ Tệp tin (File Pointer Tracking): Module duy trì vị trí con trỏ cuối cùng (offset seek) của file 'cowrie.json'. Khi có dòng log mới được Cowrie ghi xuống đĩa, tiến trình chỉ đọc chính xác phần dung lượng mới sinh ra mà không cần nạp lại toàn bộ file.")
    add_body_paragraph(doc, "2. Bộ đệm & Lọc Nhiễu (Filter & Sanitize): Chuyển đổi định dạng chuỗi JSON thô thành đối tượng Python Dictionary có cấu trúc, kiểm tra tính toàn vẹn của gói tin và bỏ qua các bản ghi bị phân mảnh hoặc lỗi cú pháp.")
    add_body_paragraph(doc, "3. Cơ chế Tự phục hồi Kết nối (Self-healing & Log Rotation): Khi file log bị hệ điều hành xoay vòng (Logrotate) hoặc khi dịch vụ Cowrie khởi động lại, Event Collector tự động phát hiện sự thay đổi Inode của file và mở lại luồng lắng nghe mà không làm gián đoạn hệ thống.")

    # 3.3
    add_custom_heading(doc, "3.3 Thiết kế Động cơ Tương quan Sự kiện và Ánh xạ MITRE ATT&CK (Correlation Engine)", level=2)
    add_body_paragraph(doc, "Động cơ Tương quan Sự kiện (Correlation Engine) là linh hồn kỹ thuật của đồ án, chịu trách nhiệm chuyển hóa các dòng log kỹ thuật rời rạc thành các Cảnh báo An ninh Có ý nghĩa (Actionable Security Alerts). Thuật toán hoạt động dựa trên nguyên lý Cửa sổ Thời gian Trượt (Sliding Time Window):")
    add_body_paragraph(doc, "Gọi W là độ rộng của cửa sổ thời gian (mặc định W = 60 giây) và T là ngưỡng số lần đăng nhập thất bại tối đa cho phép (mặc định T = 5 lần). Với mỗi địa chỉ IP nguồn S_ip gửi sự kiện 'cowrie.login.failed' tại thời điểm t_now, thuật toán thực hiện:")
    add_body_paragraph(doc, "Bước 1: Lấy danh sách lịch sử các mốc thời gian thất bại của S_ip: L = {t_1, t_2, ..., t_k}.")
    add_body_paragraph(doc, "Bước 2: Loại bỏ toàn bộ các mốc thời gian đã trượt ra ngoài cửa sổ thời gian: L' = {t ∈ L | t_now - t ≤ W}.")
    add_body_paragraph(doc, "Bước 3: Thêm t_now vào L'. Nếu kích thước |L'| ≥ T, lập tức kích hoạt Cảnh báo Tấn công Dò quét Mật khẩu diện rộng (MITRE T1110.001) và xóa danh sách L' để ngăn chặn hiện tượng spam cảnh báo liên tục.")
    add_body_paragraph(doc, "Bên cạnh đó, Correlation Engine tự động phân loại các sự kiện đặc biệt khác và ánh xạ vào ma trận MITRE ATT&CK được mô tả chi tiết trong Bảng 3.1 dưới đây:")

    mitre_map_headers = ["Mã Sự kiện Cowrie", "Kỹ thuật MITRE ATT&CK", "Tên Kỹ thuật Chuẩn", "Mức độ Nguy hại", "Hành động SOAR Khuyến nghị"]
    mitre_map_data = [
        ["cowrie.login.failed (đạt ngưỡng)", "T1110.001", "Brute Force: Password Guessing", "HIGH", "Tarpit giam lỏng + Chặn Firewall"],
        ["cowrie.login.success", "T1078", "Valid Accounts: Initial Access", "CRITICAL", "Trinh sát ngược tức thì + Kích hoạt bẫy"],
        ["cowrie.command.input (uname, whoami)", "T1082", "System Information Discovery", "MEDIUM", "Ghi nhật ký telemetry + Giám sát phiên"],
        ["cowrie.command.input (đọc canary file)", "T1552.001", "Unsecured Credentials In Files", "CRITICAL", "Khử ẩn danh Real IP + Cô lập phiên"],
        ["cowrie.session.file_download", "T1105", "Ingress Tool Transfer", "CRITICAL", "Cách ly Sandbox + Quét VirusTotal"],
        ["cowrie.command.input (iptables -F)", "T1562.001", "Impair Defenses: Disable Tools", "HIGH", "Gửi cảnh báo khẩn cấp cho SOC"],
    ]
    add_styled_table(doc, mitre_map_headers, mitre_map_data, caption="Bảng 3.1: Bảng ánh xạ các Sự kiện Cowrie sang Ma trận Kỹ thuật MITRE ATT&CK")

    # 3.4
    add_custom_heading(doc, "3.4 Thiết kế Phân hệ Trinh sát ngược Kẻ tấn công (Reverse Intelligence Engine)", level=2)
    add_body_paragraph(doc, "Khác với cách tiếp cận phòng thủ thụ động truyền thống (chỉ nhìn thấy IP mà không biết thông tin đối phương), Phân hệ Trinh sát ngược (Reverse Intelligence) được thiết kế để tự động thực thi chu trình điều tra tình báo nguồn mở (OSINT Pipeline) ngay trong mili-giây đầu tiên khi phát hiện IP tấn công:")
    add_body_paragraph(doc, "1. Phân giải Địa lý & Nhà mạng (GeoIP & ASN Profiling): Truy vấn dịch vụ phân giải địa chỉ IP để xác định quốc gia, thành phố, tọa độ địa lý, mã hệ thống tự trị (ASN) và tổ chức sở hữu dải mạng (ISP). Điều này giúp phân biệt ngay lập tức giữa các máy chủ đặt tại Datacenter (AWS, DigitalOcean, OVH) với các dải mạng người dùng băng thông rộng dân dụng.")
    add_body_paragraph(doc, "2. Tra cứu Cơ sở Dữ liệu Danh tính Mã độc Toàn cầu (AbuseIPDB Reputation API): Gửi truy vấn kiểm tra lịch sử vi phạm của IP trong vòng 90 ngày gần nhất. Hệ thống trích xuất chỉ số 'Abuse Confidence Score' (từ 0 đến 100%). Nếu điểm số > 40%, IP được tự động gán nhãn là 'Known Cybercrime Infrastructure'.")
    add_body_paragraph(doc, "3. Tra cứu Thiết bị & Lỗ hổng Mở (Shodan Host Intelligence API): Kết nối Shodan API để thu thập danh sách các cổng dịch vụ mở (Open Ports), các lỗ hổng CVE chưa được vá và hệ điều hành ước tính của máy chủ tấn công.")
    add_body_paragraph(doc, "4. Kỹ thuật Quét cổng Ngược An toàn (Safe Reverse Port Probing): Module chủ động thực hiện kiểm tra bắt tay TCP 3 bước (TCP SYN Connect) tới 10 cổng then chốt của IP tấn công (21, 22, 23, 80, 443, 1080, 3128, 3389, 8080, 8888) với thời gian timeout cực ngắn (300ms). Dựa trên kết quả trả về, hệ thống phân loại chính xác hình thái đối thủ:")
    add_body_paragraph(doc, "• Nếu mở cổng 23 (Telnet) hoặc 80 (Web camera): Phân loại là 'Compromised IoT / Botnet Node (Mirai variant)'.")
    add_body_paragraph(doc, "• Nếu mở cổng 1080, 3128, 8080: Phân loại là 'Anonymized Proxy / Tor Node'.")
    add_body_paragraph(doc, "• Nếu điểm AbuseIPDB > 75%: Phân loại là 'Automated Scanner Infrastructure'.")

    # 3.5
    add_custom_heading(doc, "3.5 Thiết kế Phân hệ Đánh lừa & Bẫy Mồi Khử ẩn danh (Active Honeytoken Deception Engine)", level=2)
    add_body_paragraph(doc, "Nhằm đối phó với những kẻ tấn công chuyên nghiệp sử dụng mạng ẩn danh (VPN, Tor, Proxy) để che giấu nguồn gốc khi SSH vào Honeypot, Phân hệ Active Deception Engine được thiết kế với nhiệm vụ kiến tạo một môi trường 'mồi nhử hoàn hảo' (Realistic Honey Environment):")
    add_body_paragraph(doc, "Hệ thống tự động sinh ra và cài cắm 3 lớp tài liệu mồi nhử (Decoy Breadcrumbs):")
    add_body_paragraph(doc, "1. Fake AWS Credentials ('/root/.aws/credentials'): Giả lập tệp tin cấu hình tài khoản Amazon Web Services có quyền quản trị cao nhất đối với cụm máy chủ sao lưu cơ sở dữ liệu. Trong tệp tin này, một URL kiểm tra ngầm (Canary Endpoint) được nhúng khéo léo vào phần chú thích mã nguồn.")
    add_body_paragraph(doc, "2. Fake Bash History ('/root/.bash_history'): Giả lập lịch sử thao tác dòng lệnh của người quản trị máy chủ, trong đó chứa một câu lệnh tải bản vá bảo mật khẩn cấp (curl -s http://.../patch.sh | bash) trỏ tới máy chủ Webhook của Blue Team.")
    add_body_paragraph(doc, "3. Fake Database Dump ('/var/backups/db_backup_2026.sql'): Giả lập tệp tin sao lưu cơ sở dữ liệu MySQL chứa các bảng tài khoản người dùng, mật khẩu quản trị và đường link truy cập vào cổng quản trị nội bộ (SSO Authentication Portal).")
    add_body_paragraph(doc, "Nguyên lý Khử ẩn danh: Khi kẻ tấn công đánh cắp các tệp tin này và mang về máy tính cá nhân để khai thác, việc click vào đường link hoặc chạy lệnh sẽ kích hoạt một Webhook HTTP Request gửi thẳng từ máy thật của hacker về máy chủ SOC. Lúc này, toàn bộ lớp vỏ bọc VPN/Proxy mà hacker dùng để SSH vào Honeypot trước đó sẽ bị vô hiệu hóa hoàn toàn, để lộ địa chỉ IP thật và thông số hệ thống của thủ phạm.")

    # 3.6
    add_custom_heading(doc, "3.6 Thiết kế Phân hệ Phân tích và Cách ly Mã độc (Malware Sandbox & Staging Pipeline)", level=2)
    add_body_paragraph(doc, "Khi kẻ tấn công sử dụng các công cụ truyền tệp tin (wget, curl, tftp, sftp) để đưa mã độc vào máy bẫy, Phân hệ Malware Staging tự động kích hoạt chu trình phân tích gồm 4 pha:")
    add_body_paragraph(doc, "• Pha 1 - Tự động Cách ly (Automated Quarantine): Mã độc được di chuyển ngay lập tức vào thư mục cô lập an toàn, gắn cờ quyền chỉ đọc (Read-only) và vô hiệu hóa quyền thực thi (chmod -x) để ngăn chặn mã độc tự kích hoạt ngoài ý muốn.")
    add_body_paragraph(doc, "• Pha 2 - Tính toán Mã băm Toàn vẹn (Cryptographic Hashing): Tính toán băm MD5 và SHA256 của tệp tin để tạo ra mã nhận dạng duy nhất (Unique IOC Identifier).")
    add_body_paragraph(doc, "• Pha 3 - Trích xuất Chuỗi Tĩnh (Static String Extraction & Regex Pattern Matching): Quét toàn bộ nội dung tệp tin để tìm kiếm các địa chỉ IP máy chủ C2, các tên miền độc hại, các câu lệnh tạo backdoor và nhận diện chữ ký của các dòng họ mã độc nổi tiếng (như chữ ký của Mirai botnet, Gafgyt, hoặc XMRig Miner).")
    add_body_paragraph(doc, "• Pha 4 - Tích hợp Tình báo VirusTotal API: Tự động gửi mã băm SHA256 lên nền tảng VirusTotal để tra cứu tỷ lệ nhận diện độc hại (Detection Ratio), tên phân loại mã độc theo tiêu chuẩn của các hãng diệt virus hàng đầu thế giới (Kaspersky, Microsoft, CrowdStrike).")

    # 3.7
    add_custom_heading(doc, "3.7 Thiết kế Động cơ Thực thi Phản ứng SOAR (Firewall Enforcer & Tarpitting)", level=2)
    add_body_paragraph(doc, "Động cơ Thực thi SOAR (SOAR Enforcer) chuyển đổi các quyết định phân tích thành hành động tác chiến cụ thể trên hạ tầng mạng:")
    add_body_paragraph(doc, "1. Thực thi Chặn Tường lửa Động (Dynamic Firewall Enforcement): Hỗ trợ tích hợp đa nền tảng. Trên máy chủ Linux, module trực tiếp gọi tiện ích 'iptables' hoặc 'nftables' để chèn luật chặn gói tin ở mức nhân hệ điều hành: 'iptables -I INPUT -s <IP> -j DROP'. Trên môi trường Windows, module sử dụng 'netsh advfirewall'. Hệ thống có cơ chế kiểm tra Whitelist (danh sách trắng) để bảo vệ an toàn cho các địa chỉ IP quản trị của nhà trường/doanh nghiệp.")
    add_body_paragraph(doc, "2. Động cơ Giam lỏng Tarpit (Connection Tarpitting Engine): Khi phát hiện kẻ tấn công là một botnet quét tự động, thay vì ngắt kết nối (khiến botnet chuyển sang quét mục tiêu khác), SOAR Enforcer sử dụng cơ chế NAT chuyển hướng gói tin: 'iptables -t nat -A PREROUTING -p tcp -s <IP> --dport 2222 -j REDIRECT --to-ports 22222'. Tại cổng 22222, dịch vụ Endlessh Tarpit sẽ giam giữ kết nối của kẻ tấn công bằng cách truyền từng byte dữ liệu banner cách nhau 10 giây, khóa cứng tiến trình của hacker và làm kiệt quệ tài nguyên máy tấn công.")
    add_body_paragraph(doc, "3. Xuất bản Danh sách đen Đe dọa (Threat Feed Export): Mọi địa chỉ IP bị chặn đều được tự động đồng bộ ra tệp tin chuẩn 'data/threat_intel_feed.txt' để chia sẻ cho các hệ thống tường lửa biên khác trong mạng nội bộ.")

    # 3.8
    add_custom_heading(doc, "3.8 Thiết kế Giao diện Giám sát & Điều khiển Tương tác 2 Chiều (Telegram SOAR Bot)", level=2)
    add_body_paragraph(doc, "Một điểm nhấn quan trọng giúp đồ án vượt xa các ứng dụng gửi thông báo thông thường là thiết kế Telegram SOAR Bot tương tác 2 chiều (Bidirectional Interactive Bot):")
    add_body_paragraph(doc, "• Giao diện Cảnh báo Trực quan: Thay vì gửi văn bản thô, Bot xuất bản các Thẻ Cảnh báo (Incident Cards) định dạng HTML chuyên nghiệp với icon mức độ nguy hại, thông tin chi tiết về kẻ tấn công, mã kỹ thuật MITRE ATT&CK và kết quả trinh sát nhanh.")
    add_body_paragraph(doc, "• Bàn phím Hành động Tức thì (Inline Keyboard Actions): Mỗi thông báo sự cố đều đi kèm một cụm 4 nút bấm tương tác:")
    add_body_paragraph(doc, "  - [🔍 Trinh sát ngược OSINT]: Kích hoạt lệnh quét sâu và gửi lại báo cáo tình báo chi tiết về IP.")
    add_body_paragraph(doc, "  - [⛔ Chặn Firewall tức thì]: Ra lệnh cho SOAR Enforcer khóa IP trên Tường lửa ngay lập tức.")
    add_body_paragraph(doc, "  - [⏳ Đưa vào Tarpit]: Điều hướng IP vào hố nhựa đường Tarpit để làm tiêu hao tài nguyên đối phương.")
    add_body_paragraph(doc, "  - [🔓 Mở khóa IP]: Giải phóng IP khỏi danh sách chặn nếu xác định đây là kết nối nhầm lẫn hợp lệ.")
    add_body_paragraph(doc, "Cơ chế này giúp chuyên viên SOC có thể điều hành tác chiến từ bất kỳ đâu thông qua điện thoại thông minh mà không cần phải mở máy tính và đăng nhập vào máy chủ.")

    doc.add_page_break()
