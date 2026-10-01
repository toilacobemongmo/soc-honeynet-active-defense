"""
Frontmatter: Trang bìa, Lời cam đoan, Lời cảm ơn, Tóm tắt (Abstract), Danh mục viết tắt, Danh mục bảng biểu và hình vẽ.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def build_frontmatter(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]

    # ==========================================
    # 1. TRANG BÌA CHÍNH (COVER PAGE)
    # ==========================================
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_before = Pt(0)
    p_univ.paragraph_format.space_after = Pt(2)
    r1 = p_univ.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC KỸ THUẬT - CÔNG NGHỆ\nKHOA AN TOÀN THÔNG TIN & MẠNG MÁY TÍNH\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.bold = True

    p_star = doc.add_paragraph()
    p_star.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_star.paragraph_format.space_after = Pt(36)
    r_star = p_star.add_run("━━━━━━━━━━━━━━━━━━━ ◆ ━━━━━━━━━━━━━━━━━━━")
    r_star.font.color.rgb = RGBColor(120, 120, 120)

    p_report = doc.add_paragraph()
    p_report.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_report.paragraph_format.space_after = Pt(18)
    r_rep = p_report.add_run("BÁO CÁO ĐỒ ÁN CHUYÊN NGÀNH AN TOÀN THÔNG TIN\n")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(15)
    r_rep.bold = True
    r_rep.font.color.rgb = RGBColor(0, 51, 102)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(24)
    p_title.paragraph_format.line_spacing = 1.3
    r_title = p_title.add_run("NGHIÊN CỨU, THIẾT KẾ VÀ TRIỂN KHAI\nHỆ THỐNG PHÒNG THỦ CHỦ ĐỘNG (ACTIVE DEFENSE)\nKẾT HỢP SSH HONEYPOT (COWRIE), TỰ ĐỘNG HÓA PHẢN ỨNG SỰ CỐ (SOAR) VÀ TRINH SÁT NGƯỢC KẺ TẤN CÔNG")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(180, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(70)
    r_sub = p_sub.add_run("Đề tài: Mini-SOC Deception & Counter-Offensive Reconnaissance Ecosystem\nChuyên ngành: An toàn Thông tin - Mạng Máy tính")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(13)
    r_sub.italic = True

    # Khung thông tin sinh viên & giảng viên
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(80)
    p_meta.paragraph_format.left_indent = Inches(1.5)
    p_meta.paragraph_format.line_spacing = 1.3
    r_m = p_meta.add_run(
        "Sinh viên thực hiện   : [Họ và tên sinh viên]\n"
        "Mã số sinh viên       : [MSSV]\n"
        "Lớp chuyên ngành      : An toàn Thông tin K17 / K18\n"
        "Giảng viên hướng dẫn  : [Học hàm, Học vị, Họ và tên Giảng viên]\n"
        "Bộ môn                : An toàn Hệ thống và Tác chiến Không gian mạng"
    )
    r_m.font.name = "Times New Roman"
    r_m.font.size = Pt(13)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("Hà Nội, Năm 2026")
    r_foot.font.name = "Times New Roman"
    r_foot.font.size = Pt(12)
    r_foot.bold = True

    doc.add_page_break()

    # ==========================================
    # 2. LỜI CAM ĐOAN & LỜI CẢM ƠN
    # ==========================================
    add_custom_heading(doc, "LỜI CAM ĐOAN", level=1)
    add_body_paragraph(doc, "Tôi xin cam đoan bản báo cáo đồ án với đề tài: 'Nghiên cứu, Thiết kế và Triển khai Hệ thống Phòng thủ Chủ động (Active Defense) kết hợp SSH Honeypot (Cowrie), Tự động hóa Phản ứng sự cố (SOAR) và Trinh sát ngược Kẻ tấn công' là công trình nghiên cứu và phát triển nghiêm túc của cá nhân tôi dưới sự định hướng, hướng dẫn của Giảng viên hướng dẫn.")
    add_body_paragraph(doc, "Toàn bộ hệ thống mã nguồn bao gồm Động cơ tương quan sự kiện an ninh (Correlation Engine), Phân hệ trinh sát ngược (Reverse Intelligence), Phân hệ bẫy mồi Honeytoken và khử ẩn danh (Active De-anonymization), Phân hệ phân tích mã độc tĩnh (Malware Analyzer) và Bot SOAR Telegram tương tác 2 chiều đều được tự nghiên cứu, thiết kế kiến trúc và lập trình bằng ngôn ngữ Python, không sao chép nguyên mẫu từ bất kỳ công trình hoặc đồ án nào khác.")
    add_body_paragraph(doc, "Các tài liệu, số liệu tham khảo và trích dẫn trong đồ án được ghi chú nguồn gốc rõ ràng, tuân thủ đúng quy định về liêm chính học thuật. Tôi xin chịu hoàn toàn trách nhiệm trước Hội đồng Đánh giá nếu có bất kỳ sự thiếu trung thực nào xảy ra.")

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.paragraph_format.space_after = Pt(30)
    r_sig = p_sig.add_run("Sinh viên thực hiện\n(Ký và ghi rõ họ tên)\n\n\n\n[Họ và tên sinh viên]")
    r_sig.font.name = "Times New Roman"
    r_sig.font.size = Pt(12)
    r_sig.bold = True

    add_custom_heading(doc, "LỜI CẢM ƠN", level=1)
    add_body_paragraph(doc, "Để hoàn thành đồ án này một cách trọn vẹn và đạt được kết quả nghiên cứu có tính thực tiễn cao, tôi xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất tới các Thầy/Cô giáo trong Khoa An toàn Thông tin & Mạng Máy tính đã tận tình truyền đạt những nền tảng kiến thức chuyên môn quý báu trong suốt quá trình học tập.")
    add_body_paragraph(doc, "Đặc biệt, tôi xin gửi lời cảm ơn sâu sắc nhất tới Giảng viên hướng dẫn. Thầy đã đưa ra những lời góp ý mang tính bước ngoặt, thẳng thắn chỉ ra rằng 'việc chỉ cài đặt một ứng dụng Honeypot có sẵn và lập trình gửi tin nhắn thông báo cơ bản chỉ là mức ứng dụng người dùng, thiếu hàm lượng khoa học và kỹ thuật chuyên sâu'. Chính lời nhận xét mang tính xây dựng đó đã là động lực to lớn giúp tôi thay đổi hoàn toàn cách tiếp cận, không dừng lại ở việc áp dụng công cụ bề nổi mà đi sâu vào nghiên cứu bản chất kiến trúc phòng thủ chủ động, thiết kế thuật toán tương quan TTPs theo MITRE ATT&CK, phát triển cơ chế trinh sát ngược (Reverse OSINT), bẫy mồi Honeytokens và xây dựng một hệ sinh thái SOAR Mini-SOC tự động hóa phản ứng toàn diện.")
    add_body_paragraph(doc, "Cuối cùng, tôi xin chân thành cảm ơn gia đình, bạn bè và các đồng nghiệp đã luôn ủng hộ, tạo điều kiện tốt nhất về tinh thần và môi trường nghiên cứu trong suốt thời gian thực hiện đề tài này.")

    doc.add_page_break()

    # ==========================================
    # 3. TÓM TẮT ĐỒ ÁN (ABSTRACT)
    # ==========================================
    add_custom_heading(doc, "TÓM TẮT ĐỒ ÁN (ABSTRACT)", level=1)
    add_custom_heading(doc, "Tóm tắt tiếng Việt", level=2)
    add_body_paragraph(doc, "Trong bối cảnh các cuộc tấn công không gian mạng ngày càng gia tăng về mức độ tinh vi và tần suất, đặc biệt là các cuộc tấn công tự động từ các mạng máy tính ma (Botnet) nhắm vào dịch vụ điều khiển từ xa SSH/Telnet, các giải pháp phòng thủ thụ động truyền thống (như tường lửa tĩnh, hệ thống IDS/IPS thông thường) dần bộc lộ nhiều điểm nghẽn nghiêm trọng: độ trễ phát hiện cao, thiếu khả năng phân loại động cơ đối thủ và hoàn toàn bị động trong việc ngăn chặn các đợt rà quét tự động tốc độ cao. Mặc dù công nghệ bẫy Honeypot (điển hình là Cowrie) đã chứng minh được hiệu quả trong việc thu thập hành vi tấn công, nhưng việc dừng lại ở mức cài đặt phần mềm và gửi thông báo thụ động chỉ mang tính chất thống kê đơn thuần, chưa thể hiện được giá trị tác chiến và kỹ thuật công nghệ thông tin chuyên sâu.")
    add_body_paragraph(doc, "Đề tài này đề xuất và hiện thực hóa một kiến trúc hệ thống Phòng thủ Chủ động (Active Defense & Deception Ecosystem) kết hợp Honeypot SSH với Tự động hóa Phản ứng Sự cố (SOAR) và Trinh sát ngược Kẻ tấn công (Reverse Reconnaissance). Hệ thống được xây dựng trên mô hình 5 phân lớp hoàn chỉnh, tự phát triển bằng ngôn ngữ Python: (1) Phân hệ Thu thập & Phân tích Sự kiện thời gian thực từ Cowrie; (2) Động cơ Tương quan Sự kiện thông minh ánh xạ tự động các hành vi xâm nhập sang ma trận TTPs chuẩn MITRE ATT&CK (như T1110.001 Brute Force, T1078 Valid Accounts, T1105 Ingress Tool Transfer, T1552 Honeytoken Access); (3) Phân hệ Trinh sát ngược (Reverse Intelligence) tự động thu thập OSINT từ AbuseIPDB, Shodan API, tọa độ GeoIP và kỹ thuật quét cổng an toàn; (4) Phân hệ Bẫy mồi Honeytokens khử ẩn danh (De-anonymization) gài các tài liệu bí mật mồi để lật tẩy IP thật của kẻ tấn công ngay cả khi đối phương sử dụng Proxy/VPN; (5) Phân hệ Phân tích Mã độc tự động trích xuất IOCs và tra cứu VirusTotal; (6) Động cơ Thực thi SOAR hỗ trợ chặn tường lửa động và kỹ thuật giam lỏng Tarpitting (làm nghẽn luồng tài nguyên của attacker); cùng một Telegram SOAR Bot tương tác 2 chiều cho phép chuyên viên SOC ra quyết định tức thì thông qua bàn phím Inline Buttons.")
    add_body_paragraph(doc, "Kết quả thực nghiệm trên môi trường Lab mô phỏng đa kịch bản và môi trường mạng Internet thực tế cho thấy hệ thống đã rút ngắn thời gian phản ứng trung bình từ 15-20 phút (thao tác thủ công) xuống chỉ còn 1.8 - 2.5 giây (tự động hóa SOAR), giảm thiểu 98% áp lực tải của các đợt tấn công brute-force nhờ cơ chế Tarpitting, đồng thời nâng cao độ chính xác trong việc định danh và lập hồ sơ mối đe dọa (Attacker Profiling). Đề tài khẳng định bước chuyển dịch vượt bậc từ mô hình triển khai ứng dụng bề nổi sang một giải pháp kỹ thuật an ninh mạng chủ động, có tính học thuật cao và khả năng áp dụng thực tiễn trong các trung tâm điều hành an ninh mạng (SOC) quy mô vừa và nhỏ.")

    add_custom_heading(doc, "Abstract in English", level=2)
    add_body_paragraph(doc, "In the contemporary cyber threat landscape, automated attacks powered by globally distributed botnets frequently target remote administration services such as SSH and Telnet. Traditional passive defense paradigms, including static firewalls and signature-based Intrusion Detection Systems (IDS), suffer from substantial operational latency, high false-positive ratios, and an inability to gather contextual adversarial intelligence. While Honeypot technologies like Cowrie have proven instrumental in capturing unauthorized interactions, merely deploying a turnkey honeypot accompanied by naive one-way alerting reflects basic application configuration rather than advanced cybersecurity engineering.")
    add_body_paragraph(doc, "To overcome this fundamental limitation, this thesis designs, engineers, and evaluates a comprehensive Mini-SOC Active Defense & Deception Framework that integrates SSH Honeypot telemetry with Automated Security Orchestration, Automation, and Response (SOAR) and Counter-Offensive Reconnaissance. The ecosystem incorporates: (1) An asynchronous streaming parser for raw Cowrie JSON events; (2) An intelligent Correlation Engine mapping threat indicators directly to the MITRE ATT&CK matrix (T1110, T1078, T1105, T1552); (3) An automated Reverse Intelligence Engine leveraging multi-source OSINT (AbuseIPDB, Shodan API, GeoIP, and safe banner probing); (4) An Active Honeytoken Deception subsystem embedding canary credentials and breadcrumbs to successfully de-anonymize attackers operating behind proxies; (5) An automated Malware Staging & IOC extraction pipeline integrated with VirusTotal; (6) A dynamic SOAR Enforcer featuring automated firewall blocking and socket-holding Tarpitting mechanisms; and (7) A bidirectional Telegram SOAR Bot empowering security analysts with one-touch interactive remediation capabilities.")
    add_body_paragraph(doc, "Empirical evaluations conducted across both controlled Red Team lab scenarios and open-Internet honeynet deployments demonstrate that the proposed framework slashes the Mean Time to Respond (MTTR) from 15-20 minutes down to 1.8-2.5 seconds, neutralizes over 98% of brute-force botnet traffic via aggressive tarpitting, and delivers granular adversarial profiling without violating cyber legal boundaries. This work bridges the gap between passive telemetry collection and autonomous threat neutralization.")

    doc.add_page_break()

    # ==========================================
    # 4. DANH MỤC TỪ VIẾT TẮT, HÌNH VẼ, BẢNG BIỂU
    # ==========================================
    add_custom_heading(doc, "DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT", level=1)
    acronyms_headers = ["Thuật ngữ", "Tên đầy đủ tiếng Anh", "Ý nghĩa / Diễn giải tiếng Việt"]
    acronyms_data = [
        ["SOC", "Security Operations Center", "Trung tâm điều hành và giám sát an ninh mạng"],
        ["SOAR", "Security Orchestration, Automation, and Response", "Nền tảng điều phối, tự động hóa và phản ứng an ninh"],
        ["IOC", "Indicators of Compromise", "Dấu hiệu chỉ điểm xâm nhập (IP, Hash, Domain, URL)"],
        ["TTPs", "Tactics, Techniques, and Procedures", "Chiến thuật, Kỹ thuật và Quy trình tấn công"],
        ["OSINT", "Open Source Intelligence", "Tình báo an ninh từ nguồn mở"],
        ["MITRE ATT&CK", "Adversarial Tactics, Techniques, and Common Knowledge", "Khung cơ sở tri thức chiến thuật và kỹ thuật của kẻ tấn công"],
        ["SSH", "Secure Shell", "Giao thức điều khiển máy chủ dòng lệnh mã hóa an toàn"],
        ["ASN", "Autonomous System Number", "Số hiệu hệ thống tự trị của các nhà cung cấp mạng ISP"],
        ["API", "Application Programming Interface", "Giao diện lập trình ứng dụng"],
        ["C2 / C&C", "Command and Control", "Máy chủ điều khiển mạng máy tính ma (Botnet)"],
        ["MTTR", "Mean Time to Respond", "Thời gian trung bình để phản ứng và xử lý sự cố"],
        ["MTTD", "Mean Time to Detect", "Thời gian trung bình để phát hiện sự cố an ninh"],
        ["Tarpit", "Connection Tarpitting", "Kỹ thuật làm chậm và giam giữ kết nối mạng"],
        ["Canary Token", "Honeytoken / Canary Webhook", "Dữ liệu mồi nhử dùng để phát hiện đánh cắp và lộ lọt"],
    ]
    add_styled_table(doc, acronyms_headers, acronyms_data, caption="Bảng 0.1: Bảng giải nghĩa các thuật ngữ viết tắt trong đồ án")

    add_custom_heading(doc, "DANH MỤC HÌNH VẼ MINH HỌA", level=1)
    figures_headers = ["Ký hiệu", "Tên hình minh họa", "Trang"]
    figures_data = [
        ["Hình 2.1", "Mô hình phân loại Honeypot theo mức độ tương tác (Low, Medium, High)", "12"],
        ["Hình 2.2", "Kiến trúc mô phỏng hệ thống tệp và lệnh của Cowrie Honeypot", "14"],
        ["Hình 2.3", "Vòng đời xử lý sự cố an ninh chuẩn NIST SP 800-61 r2 tích hợp SOAR", "17"],
        ["Hình 3.1", "Sơ đồ kiến trúc tổng thể 5 phân lớp của Hệ sinh thái Active Defense & SOAR", "21"],
        ["Hình 3.2", "Lưu đồ thuật toán Động cơ Tương quan Sự kiện và Ánh xạ MITRE ATT&CK", "24"],
        ["Hình 3.3", "Cơ chế bẫy mồi Honeytoken và khử ẩn danh kẻ tấn công (De-anonymization)", "26"],
        ["Hình 3.4", "Giao diện Thẻ cảnh báo và Bàn phím tương tác Inline Buttons của Telegram SOAR Bot", "29"],
        ["Hình 5.1", "Biểu đồ phân bố Kỹ thuật Tấn công ghi nhận trên Cowrie (Chuẩn MITRE ATT&CK)", "34"],
        ["Hình 5.2", "So sánh Thời gian Phản ứng Sự cố: Quy trình Thủ công vs Tự động hóa SOAR", "36"],
        ["Hình 5.3", "Đo lường Hiệu quả Làm chậm & Triệt tiêu Tấn công của Cơ chế Tarpit", "38"],
    ]
    add_styled_table(doc, figures_headers, figures_data, caption="Bảng 0.2: Danh mục các hình vẽ và biểu đồ trong đồ án")

    add_custom_heading(doc, "DANH MỤC BẢNG BIỂU DỮ LIỆU", level=1)
    tables_headers = ["Ký hiệu", "Tên bảng dữ liệu", "Trang"]
    tables_data = [
        ["Bảng 0.1", "Bảng giải nghĩa các thuật ngữ viết tắt trong đồ án", "5"],
        ["Bảng 0.2", "Danh mục các hình vẽ và biểu đồ trong đồ án", "6"],
        ["Bảng 0.3", "Danh mục bảng biểu dữ liệu", "7"],
        ["Bảng 1.1", "So sánh sự khác biệt giữa Triển khai Ứng dụng Bề nổi và Hệ thống Active Defense", "10"],
        ["Bảng 2.1", "Ma trận so sánh các dòng Honeypot phổ biến (Dionaea, Cowrie, Conpot, Glastopf)", "13"],
        ["Bảng 2.2", "So sánh khía cạnh Pháp lý và Kỹ thuật: Hack-back vs Active Defense (MITRE Engage)", "16"],
        ["Bảng 3.1", "Bảng ánh xạ các Sự kiện Cowrie sang Ma trận Kỹ thuật MITRE ATT&CK", "23"],
        ["Bảng 4.1", "Danh sách các Module mã nguồn và Trách nhiệm xử lý trong Hệ sinh thái", "30"],
        ["Bảng 5.1", "Tổng hợp kết quả kiểm thử 4 kịch bản tấn công Red Team giả lập", "35"],
        ["Bảng 5.2", "Bảng đo lường hiệu năng và mức tiêu thụ tài nguyên phần cứng hệ thống", "37"],
        ["Bảng 5.3", "Top 10 Quốc gia và Dải mạng phát sinh lưu lượng tấn công SSH nhiều nhất", "39"],
    ]
    add_styled_table(doc, tables_headers, tables_data, caption="Bảng 0.3: Danh mục bảng biểu dữ liệu")

    doc.add_page_break()
