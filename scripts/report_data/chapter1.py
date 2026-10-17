"""
Chapter 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ (5-6 trang)
Trình bày bối cảnh an ninh mạng, các cuộc tấn công SSH/Telnet, hạn chế của phòng thủ thụ động,
đặc biệt là phân tích nhận xét của giảng viên để chuyển đổi sang kiến trúc phòng thủ chủ động Active Defense & SOAR.
"""

from docx.shared import Pt
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def build_chapter1(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]

    add_custom_heading(doc, "CHƯƠNG 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ", level=1)

    # 1.1
    add_custom_heading(doc, "1.1 Bối cảnh An ninh mạng và Thực trạng Tấn công Dịch vụ Truy cập từ xa (SSH/Telnet)", level=2)
    add_body_paragraph(doc, "Trong kỷ nguyên chuyển đổi số và bùng nổ hạ tầng điện toán đám mây (Cloud Computing), dịch vụ Secure Shell (SSH) và Telnet đóng vai trò là xương sống trong việc quản trị, cấu hình và vận hành hệ thống từ xa của hàng triệu máy chủ, thiết bị mạng và hệ thống IoT trên toàn thế giới. Do cổng mặc định TCP 22 (SSH) và TCP 23 (Telnet) bắt buộc phải mở công khai để phục vụ nhu cầu quản trị từ xa, đây luôn là mục tiêu hàng đầu bị các mạng máy tính ma (Botnet) và các nhóm tội phạm mạng nhắm đến để thực hiện các chiến dịch xâm nhập ban đầu (Initial Access).")
    add_body_paragraph(doc, "Theo các báo cáo an ninh mạng toàn cầu gần đây của các hãng bảo mật lớn như Fortinet, Palo Alto Networks và Microsoft Threat Intelligence, hơn 85% tổng lưu lượng rà quét trái phép trên Internet hướng về các cổng quản trị từ xa. Các cuộc tấn công này diễn ra với tốc độ chóng mặt và hoàn toàn tự động, được điều khiển bởi các biến thể mã độc botnet nguy hiểm như Mirai, Gafgyt, Tsunami hay Muhstik. Những botnet này liên tục thực hiện chiến dịch dò quét địa chỉ IP toàn cầu (IP Sweeping) và thực hiện tấn công dò quét từ điển (Dictionary Brute Force) với hàng ngàn cặp tài khoản/mật khẩu phổ biến nhằm chiếm quyền điều khiển (root compromise) của máy chủ mục tiêu.")
    add_body_paragraph(doc, "Hậu quả của việc máy chủ SSH bị xâm phạm là vô cùng thảm khốc: kẻ tấn công ngay lập tức biến máy chủ nạn nhân thành một bàn đạp nội bộ (Pivot point) để leo thang đặc quyền (Privilege Escalation), cài cắm mã độc đào tiền ảo (Cryptocurrency Miner), đánh cắp dữ liệu kinh doanh quan trọng, triển khai mã độc tống tiền (Ransomware), hoặc tuyển mộ máy chủ đó vào mạng lưới botnet để phát động các đợt tấn công từ chối dịch vụ phân tán (DDoS) quy mô terabit nhằm vào các hạ tầng trọng yếu khác.")

    # 1.2
    add_custom_heading(doc, "1.2 Sự bế tắc của Mô hình Phòng thủ Thụ động (Passive Defense) truyền thống", level=2)
    add_body_paragraph(doc, "Trong nhiều thập kỷ qua, các chiến lược bảo mật mạng chủ yếu dựa trên triết lý 'Phòng thủ chu vi thụ động' (Passive Perimeter Defense) với các thành phần cốt lõi bao gồm Tường lửa trạng thái (Stateful Firewall), Hệ thống Phát hiện và Ngăn chặn Xâm nhập (IDS/IPS như Snort, Suricata) và phần mềm phòng chống brute-force cơ bản (như Fail2ban). Tuy nhiên, trước các chiến dịch tấn công phân tán quy mô lớn và đa hình của tội phạm mạng hiện đại, mô hình phòng thủ thụ động này đã bộc lộ những điểm nghẽn nghiêm trọng:")
    add_body_paragraph(doc, "Thứ nhất, vấn đề 'Bội thực cảnh báo giả' (Alert Fatigue): Các hệ thống IDS truyền thống dựa vào chữ ký tĩnh (Signature-based) liên tục sinh ra hàng chục nghìn cảnh báo mỗi ngày đối với các lưu lượng quét mạng thông thường. Chuyên viên an ninh tại các trung tâm điều hành SOC không thể nào rà soát hết lượng cảnh báo khổng lồ này, dẫn đến việc bỏ sót các cuộc tấn công thực sự nguy hiểm.")
    add_body_paragraph(doc, "Thứ hai, độ trễ phản ứng quá lớn (High Response Latency): Quy trình xử lý sự cố truyền thống phụ thuộc hoàn toàn vào con người (SOC Tier 1 Analyst). Từ khi hệ thống phát hiện có IP tấn công brute-force, chuyên viên phải kiểm tra thủ công log, tra cứu WHOIS, xác minh địa chỉ IP, sau đó mới truy cập vào firewall để thêm luật chặn IP đó. Toàn bộ chu trình này mất trung bình từ 15 đến 30 phút. Trong khoảng thời gian đó, kẻ tấn công đã có thể đoán trúng mật khẩu yếu hoặc khai thác thành công lỗ hổng bảo mật.")
    add_body_paragraph(doc, "Thứ ba, sự thiếu hụt thông tin tình báo đối phương (Adversarial Intelligence Blindspot): Phòng thủ thụ động chỉ biết chặn và bỏ qua (Drop/Reject packet). Hệ thống hoàn toàn 'mù' về động cơ của kẻ tấn công: Kẻ tấn công là ai? Chúng đến từ đâu? Sau khi vào được hệ thống thì chúng gõ những lệnh gì? Chúng đang tìm kiếm tài liệu nào? Những mã độc nào được chúng chuẩn bị tải lên? Việc thiếu vắng hoàn toàn các dữ liệu TTPs (Tactics, Techniques, and Procedures) này khiến đội ngũ phòng thủ luôn ở vị thế đi sau kẻ tấn công một bước.")

    # 1.3
    add_custom_heading(doc, "1.3 Khái niệm Công nghệ Bẫy Honeypot và Sự dịch chuyển sang Phòng thủ Chủ động (Active Defense)", level=2)
    add_body_paragraph(doc, "Để khắc phục sự mù mờ về thông tin của phòng thủ thụ động, công nghệ Bẫy (Honeypot) đã ra đời như một bước tiến quan trọng. Honeypot là một tài nguyên công nghệ thông tin được thiết kế và triển khai với mục đích duy nhất: trở thành một chiếc bẫy mồi nhử để kẻ tấn công xâm nhập và tương tác, trong khi toàn bộ hành vi, tổ hợp phím gõ, kịch bản khai thác và mã độc của đối phương đều bị ghi lại một cách bí mật và toàn vẹn.")
    add_body_paragraph(doc, "Trong lĩnh vực giám sát dịch vụ SSH/Telnet, Cowrie được đánh giá là một trong những giải pháp Medium-Interaction Honeypot mã nguồn mở hàng đầu thế giới. Cowrie cung cấp một shell dòng lệnh ảo hóa hoàn hảo, giả lập hệ điều hành Linux Debian/Ubuntu với đầy đủ hệ thống tệp tin (filesystem), hỗ trợ các lệnh phổ biến (ls, cd, cat, wget, curl, ps, uname), cho phép ghi lại chi tiết từng phiên kết nối và tự động lưu giữ các payload mã độc mà kẻ tấn công tải lên máy bẫy.")
    add_body_paragraph(doc, "Tuy nhiên, xu hướng phòng thủ hiện đại trên thế giới không còn dừng lại ở việc 'ngồi im chịu trận để thu thập log'. Các tổ chức nghiên cứu bảo mật hàng đầu như MITRE (với khung chiến lược MITRE Shield và MITRE Engage) đã khởi xướng cuộc cách mạng mang tên 'Phòng thủ Chủ động' (Active Defense & Active Deception). Phòng thủ chủ động là sự kết hợp đồng bộ giữa:")
    add_body_paragraph(doc, "• Đánh lừa có chủ đích (Deception Operations): Dẫn dụ kẻ tấn công vào ma trận các thông tin giả mạo (Fake credentials, Canary Tokens), buộc đối phương phải tốn thời gian, công sức và nguồn lực vào những mục tiêu không có thật.")
    add_body_paragraph(doc, "• Trinh sát ngược (Reverse Reconnaissance): Ngay khi kẻ tấn công chạm vào bẫy, hệ thống lập tức kích hoạt các công cụ thu thập thông tin tình báo đối phương (OSINT, rà soát dịch vụ, phân tích chữ ký công cụ tấn công) để vẽ nên hồ sơ đầy đủ về kẻ địch.")
    add_body_paragraph(doc, "• Tự động hóa phản ứng sự cố (SOAR): Đồng bộ hóa quy trình phát hiện, phân tích và ngăn chặn trong vòng vài giây mà không cần sự can thiệp thủ công của con người.")

    # 1.4 Callout Box & Table phân tích nhận xét giảng viên
    add_custom_heading(doc, "1.4 Phân tích và Giải quyết Nhận xét của Giảng viên: 'Vượt qua Giới hạn Cài đặt Ứng dụng Bề nổi'", level=2)
    
    add_callout_box(
        doc,
        "Lời nhận xét của Giảng viên: 'Nếu chỉ đơn thuần là cài đặt Cowrie Honeypot theo hướng dẫn có sẵn trên mạng, sau đó viết một vài dòng script đọc file cowrie.json và bắn tin nhắn thông báo vào Telegram Bot khi có ai đăng nhập, thì đây chỉ là mức độ Cài đặt và Ứng dụng công cụ có sẵn (Script-kiddie / Application Configuration Level), hoàn toàn thiếu hàm lượng nghiên cứu khoa học, không có đóng góp về mặt kỹ thuật kỹ sư và chắc chắn không thể đạt điểm giỏi/xuất sắc.'",
        title="LỜI CẢNH BÁO MANG TÍNH BƯỚC NGOẶT CỦA GIẢNG VIÊN HƯỚNG DẪN"
    )

    add_body_paragraph(doc, "Đây là một nhận xét vô cùng xác đáng và mang tính chuẩn mực học thuật cao đối với một đồ án chuyên ngành An toàn thông tin. Nhận xét này đã bóc tách rõ ràng hai mức độ tiếp cận đề tài:")
    add_body_paragraph(doc, "Ở cách tiếp cận cũ (Mức 1 - Cài đặt ứng dụng): Sinh viên tải Cowrie về bằng lệnh git clone, chạy docker-compose up, mở file log và viết 20 dòng code Python sử dụng thư viện requests để đẩy dòng chữ 'Có IP 1.2.3.4 đang tấn công' lên một nhóm chat. Cách làm này không giải quyết được bất kỳ bài toán cốt lõi nào của SOC: Không có bộ lọc tương quan (Correlation), không có khả năng chống chọi với bão cảnh báo (Alert Flooding), không ánh xạ được kỹ thuật tấn công theo tiêu chuẩn quốc tế, không có hành động ngăn chặn tự động, và đặc biệt là hoàn toàn bị động trước kẻ tấn công.")
    add_body_paragraph(doc, "Để vượt qua giới hạn đó và nâng tầm đề tài lên Mức độ 2 (Kỹ thuật Kỹ sư & Nghiên cứu Khoa học Chủ động), đồ án này đã tái cấu trúc toàn diện bài toán và xây dựng một Hệ sinh thái Active Defense & SOAR Ecosystem với 5 giá trị kỹ thuật vượt trội được thể hiện trong Bảng 1.1 dưới đây:")

    comp_headers = ["Tiêu chí Đánh giá", "Mô hình Cài đặt Bề nổi (Bị Thầy chê)", "Hệ sinh thái Active Defense & SOAR (Đồ án đề xuất)"]
    comp_data = [
        ["Bản chất Kiến trúc", "Chỉ cài Cowrie đơn lẻ và script thông báo tĩnh.", "Kiến trúc Mini-SOC 5 phân lớp hoàn chỉnh, tương tác đa thành phần."],
        ["Cơ chế Xử lý Log", "Đọc log tuyến tính, gửi tin nhắn thô liên tục (Spam).", "Bộ phân tích luồng JSON bất đồng bộ (Streaming Event Engine)."],
        ["Động cơ Tương quan (Correlation)", "Không có. Một sự kiện failed login cũng gửi alert.", "Correlation Engine tự phát triển, ánh xạ tự động ma trận MITRE ATT&CK."],
        ["Mức độ Tương tác Cảnh báo", "Thông báo 1 chiều tĩnh (Plain text notification).", "Thẻ cảnh báo trực quan + Inline Buttons tương tác 2 chiều (Chặn, Quét, Tarpit)."],
        ["Khả năng Trinh sát Ngược (OSINT)", "Hoàn toàn không có. Không biết IP là ai.", "Reverse Intel Engine tự động query AbuseIPDB, Shodan API, quét cổng an toàn."],
        ["Phòng thủ Chủ động (Deception)", "Honeypot mặc định, hacker dễ phát hiện chữ ký.", "Tùy biến Filesystem chuyên sâu + Gài bẫy Honeytokens (Canary de-anonymization)."],
        ["Phản đòn & Tiêu hao Tài nguyên", "Không có. Attacker quét thoải mái.", "Kỹ thuật Tarpitting (Giam lỏng kết nối, làm treo thread tấn công của Botnet)."],
        ["Phân tích Mã độc (Malware Staging)", "Chỉ lưu file vào ổ đĩa, không làm gì thêm.", "Payload Analyzer tự động trích xuất SHA256, IOCs và tra cứu VirusTotal."],
        ["Thời gian Phản ứng (MTTR)", "Phụ thuộc 100% vào người đọc tin nhắn (15 - 30 phút).", "Tự động hóa hoàn toàn bằng SOAR Playbooks (1.8 - 2.5 giây)."],
    ]
    add_styled_table(doc, comp_headers, comp_data, caption="Bảng 1.1: So sánh sự khác biệt bản chất giữa Cài đặt Ứng dụng Bề nổi và Hệ thống Active Defense Đồ án")

    # 1.5
    add_custom_heading(doc, "1.5 Mục tiêu nghiên cứu và Các đóng góp khoa học - kỹ thuật của Đề tài", level=2)
    add_body_paragraph(doc, "Mục tiêu tổng quát của đồ án là nghiên cứu, thiết kế kiến trúc và hiện thực hóa thành công một Hệ thống Phòng thủ Chủ động (Active Defense Framework) quy mô Mini-SOC, tích hợp chặt chẽ giữa Cowrie SSH Honeypot với Nền tảng Tự động hóa Phản ứng Sự cố (SOAR) và Trinh sát ngược Kẻ tấn công nhằm bảo vệ hạ tầng máy chủ Linux trước các chiến dịch tấn công dò quét tự động.")
    add_body_paragraph(doc, "Để đạt được mục tiêu tổng quát trên, đồ án tập trung vào các mục tiêu cụ thể và đạt được các đóng góp kỹ thuật then chốt sau:")
    add_body_paragraph(doc, "1. Về mặt Lý thuyết & Khung phương pháp luận: Phân định ranh giới pháp lý và kỹ thuật giữa 'Hack-back phá hoại bất hợp pháp' và 'Phòng thủ chủ động hợp pháp (Active Defense)' dựa trên khung chiến lược chuẩn quốc tế MITRE D3FEND và MITRE Engage. Xây dựng mô hình chuỗi phản đòn bằng Deception và De-anonymization.")
    add_body_paragraph(doc, "2. Về mặt Thiết kế Kiến trúc Hệ thống: Thiết kế kiến trúc phân lớp Mini-SOC linh hoạt, module hóa cao độ, đảm bảo khả năng mở rộng (Scalability) và dễ dàng tích hợp thêm các cảm biến honeypot khác trong tương lai.")
    add_body_paragraph(doc, "3. Về mặt Xây dựng Động cơ Tương quan (Correlation Engine): Tự phát triển thuật toán trượt cửa sổ thời gian (Sliding Time Window) để phát hiện tấn công dò quét mật khẩu (T1110.001), phân biệt giữa các đợt quét tự động vô hại và các cuộc xâm nhập có chủ đích, loại bỏ triệt để hiện tượng Alert Fatigue.")
    add_body_paragraph(doc, "4. Về mặt Trinh sát ngược & Tình báo đe dọa (Threat Intel Engine): Tích hợp tự động đa nguồn dữ liệu mở (Multi-source OSINT) bao gồm AbuseIPDB, Shodan API, GeoIP ASN và cơ chế quét cổng an toàn (Safe Port Probing) nhằm lập hồ sơ kẻ tấn công (Attacker Profiling) ngay trong mili-giây đầu tiên của sự cố.")
    add_body_paragraph(doc, "5. Về mặt Đánh lừa & Bẫy mồi Khử ẩn danh (Active Honeytokens): Xây dựng cơ chế sinh tự động các file tài liệu mồi nhử (Fake AWS Keys, Fake Bash History, Fake Database Dumps) có nhúng Canary Webhook Beacons. Khi hacker đánh cắp tài liệu và mở trên máy thật, hệ thống sẽ bắt được IP thật và dấu vân tay trình duyệt của hacker, giải quyết triệt để bài toán hacker ẩn danh qua Proxy/Tor.")
    add_body_paragraph(doc, "6. Về mặt Tự động hóa Phản ứng & Tiêu hao đối phương (SOAR Enforcer & Tarpitting): Triển khai thành công kỹ thuật giam lỏng Tarpit (Endless Socket Hold) làm tiêu hao tài nguyên CPU/RAM/Bandwidth của các máy chủ tấn công, kết hợp với cơ chế cập nhật tự động Tường lửa iptables/nftables và đồng bộ Threat Feed IOCs.")
    add_body_paragraph(doc, "7. Về mặt Tác chiến & Điều hành: Xây dựng Telegram SOAR Bot tương tác 2 chiều (Bidirectional Interactive Bot) trang bị bàn phím điều khiển tức thời (Inline Keyboard Actions), cho phép chuyên viên SOC ra quyết định tác chiến ngay trên thiết bị di động trong vài giây.")

    # 1.6 & 1.7
    add_custom_heading(doc, "1.6 Đối tượng, Phạm vi và Giới hạn nghiên cứu", level=2)
    add_body_paragraph(doc, "• Đối tượng nghiên cứu: Các hành vi, kỹ thuật và phương thức tấn công nhắm vào dịch vụ truy cập từ xa SSH/Telnet; Công nghệ bẫy Medium-Interaction Honeypot (Cowrie); Kỹ thuật phân tích log và tương quan sự kiện theo chuẩn MITRE ATT&CK; Kỹ thuật phòng thủ chủ động bằng Honeytoken và Tarpitting; Nền tảng điều phối phản ứng sự cố tự động SOAR.")
    add_body_paragraph(doc, "• Phạm vi triển khai: Hệ thống được xây dựng và triển khai trên nền tảng hệ điều hành máy chủ Linux (Ubuntu Server 22.04 LTS / Debian 12), hỗ trợ môi trường ảo hóa Docker Container và tương thích kiểm thử trên máy trạm Windows.")
    add_body_paragraph(doc, "• Giới hạn nghiên cứu: Đồ án tập trung vào phân tích và phản ứng các cuộc tấn công nhắm vào giao thức SSH và Telnet. Các cuộc tấn công ứng dụng Web (HTTP/HTTPS) hoặc dịch vụ cơ sở dữ liệu phân tán không nằm trong phạm vi cảm biến chính của đề tài (mặc dù kiến trúc SOAR được thiết kế sẵn sàng để mở rộng nhận log từ các cảm biến khác).")

    add_custom_heading(doc, "1.7 Bố cục toàn văn của Đồ án", level=2)
    add_body_paragraph(doc, "Nội dung báo cáo đồ án được kết cấu thành 6 chương chính cùng các phần phụ lục và danh mục tài liệu tham khảo chi tiết:")
    add_body_paragraph(doc, "• Chương 1: Tổng quan và Đặt vấn đề - Phân tích bối cảnh, thực trạng tấn công SSH, hạn chế của phòng thủ thụ động, phân tích nhận xét của giảng viên và xác định mục tiêu nghiên cứu.")
    add_body_paragraph(doc, "• Chương 2: Cơ sở Lý thuyết và Khung Công nghệ - Trình bày nền tảng lý thuyết về Honeypot, kiến trúc Cowrie, khung pháp lý/kỹ thuật của Active Defense, công nghệ Honeytoken khử ẩn danh, khung tự động hóa SOAR, kỹ thuật Tarpit và ma trận MITRE ATT&CK.")
    add_body_paragraph(doc, "• Chương 3: Thiết kế Kiến trúc Hệ thống Mini-SOC Active Defense - Trình bày thiết kế chi tiết 5 phân lớp của hệ thống, luồng dữ liệu, lưu đồ thuật toán tương quan sự kiện và thiết kế các playbook phản ứng sự cố.")
    add_body_paragraph(doc, "• Chương 4: Hiện thực hóa và Mã nguồn các Phân hệ - Chi tiết hóa quá trình cài đặt môi trường, tùy biến Honeypot chuyên sâu và phân tích mã nguồn chi tiết các module Python tự phát triển.")
    add_body_paragraph(doc, "• Chương 5: Thử nghiệm Thực tế, Đánh giá và Phân tích Tấn công - Trình bày kết quả kiểm nghiệm trên 4 kịch bản tấn công Red Team giả lập, phân tích hiệu năng giảm thiểu MTTR, đánh giá hiệu quả bóp nghẽn của Tarpit và thống kê dữ liệu tấn công thực tế từ Internet.")
    add_body_paragraph(doc, "• Chương 6: Kết luận và Hướng phát triển - Tổng kết các đóng góp đạt được, chỉ ra những hạn chế và đề xuất định hướng phát triển nâng cao trong tương lai.")

    doc.add_page_break()
