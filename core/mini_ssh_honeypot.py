"""
Module: mini_ssh_honeypot.py
Mục đích: SSH Honeypot tương tác thật (Live Interactive SSH Honeypot) chạy trên port 2222.
Cho phép giảng viên, chuyên viên bảo mật hoặc Red Team kết nối SSH thật:
- Đăng nhập SSH bằng lệnh: ssh root@127.0.0.1 -p 2222
- Tương tác với Linux Bash Shell giả lập (Interactive Shell).
- Cung cấp bẫy mồi Honeytoken (.aws/credentials, db_passwords).
- Tự động ghi nhận nhật ký chuẩn Cowrie JSON để kích hoạt luồng SOAR theo thời gian thực.
"""

from datetime import datetime, timezone
import json
import os
import socket
import sys
import threading
import time
from typing import Optional
import paramiko


class HoneypotSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip: str, log_callback, is_ip_blocked_func):
        self.client_ip = client_ip
        self.log_callback = log_callback
        self.is_ip_blocked_func = is_ip_blocked_func
        self.event = threading.Event()
        self.authenticated_user = ""
        self.session_id = f"sess_{int(time.time() * 1000) % 100000}"

    def check_auth_password(self, username, password):
        print(f"\n[*] [SSH Honeypot] Attacker IP {self.client_ip} vừa thử đăng nhập | User: '{username}' | Password: '{password}'")

        # Kiểm tra xem IP có đang bị SOAR Firewall chặn không
        if self.is_ip_blocked_func(self.client_ip):
            print(f"[-] [SSH Honeypot] TỪ CHỐI IP {self.client_ip} do đang bị SOAR Firewall khóa cứng!")
            return paramiko.AUTH_FAILED

        # Chấp nhận một số mật khẩu phổ biến để hacker vào bẫy, các mật khẩu khác tính là thất bại (brute force)
        acceptable_passwords = ["root", "123456", "password", "admin", "toor", "root123", "12345"]
        if password in acceptable_passwords or username in ("root", "admin", "ubuntu"):
            print(f"[+] [SSH Honeypot] Đăng nhập THÀNH CÔNG (Cấp shell giả lập cho IP {self.client_ip})")
            self.authenticated_user = username
            self.log_callback({
                "eventid": "cowrie.login.success",
                "src_ip": self.client_ip,
                "username": username,
                "password": password,
                "session": self.session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return paramiko.AUTH_SUCCESSFUL
        else:
            print(f"[-] [SSH Honeypot] Đăng nhập THẤT BẠI cho IP {self.client_ip} (Ghi nhận hành vi Brute Force)")
            self.log_callback({
                "eventid": "cowrie.login.failed",
                "src_ip": self.client_ip,
                "username": username,
                "password": password,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


class MiniSSHHoneypot:
    def __init__(self, host: str = "0.0.0.0", port: int = 2222, log_file: str = "./data/cowrie.json", soar_enforcer=None, event_callback=None):
        self.host = host
        self.port = port
        self.log_file = log_file
        self.soar_enforcer = soar_enforcer
        self.event_callback = event_callback
        self.is_running = False
        self.server_socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None

        # Tạo hoặc nạp Host Key bí mật cho SSH Server
        self.host_key = self._get_or_create_host_key()

    def _get_or_create_host_key(self):
        key_path = "./data/honeypot_rsa.key"
        os.makedirs(os.path.dirname(os.path.abspath(key_path)), exist_ok=True)
        if os.path.exists(key_path):
            try:
                return paramiko.RSAKey(filename=key_path)
            except Exception:
                pass
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(key_path)
        return key

    def is_ip_blocked(self, ip: str) -> bool:
        if self.soar_enforcer and hasattr(self.soar_enforcer, "blocked_ips"):
            return ip in self.soar_enforcer.blocked_ips
        return False

    def log_event(self, event: dict):
        """Ghi sự kiện vào file cowrie.json chuẩn format và gọi callback lập tức."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.log_file)), exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
                f.flush()
        except Exception as e:
            print(f"[-] Lỗi ghi log honeypot: {e}")

        if self.event_callback:
            try:
                self.event_callback(event)
            except Exception as e:
                print(f"[-] Lỗi callback event: {e}")

    def handle_client(self, client_socket, addr):
        ip, port = addr
        print(f"\n[🔌 KẾT NỐI MỚI] Kẻ tấn công từ IP {ip}:{port} vừa kết nối SSH vào Honeypot!")
        if self.is_ip_blocked(ip):
            print(f"[!] [SOAR Active Defense] Phát hiện kết nối từ IP bị chặn Firewall: {ip}. Đóng kết nối lập tức!")
            client_socket.close()
            return

        # Kiểm tra nếu IP đang bị đưa vào Tarpit giam lỏng
        if self.soar_enforcer and hasattr(self.soar_enforcer, "is_tarpitted") and self.soar_enforcer.is_tarpitted(ip):
            print(f"\n[⏳ SOAR TARPIT KÍCH HOẠT] IP {ip} đang bị giam lỏng trong hố Tarpit! Gửi dữ liệu chậm cực độ để làm treo đối phương...")
            banner = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4\r\n"
            try:
                for byte in banner:
                    client_socket.send(bytes([byte]))
                    time.sleep(3)
                while True:
                    client_socket.send(b"\r\n")
                    time.sleep(5)
            except Exception:
                pass
            finally:
                client_socket.close()
            return

        transport = None
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            server = HoneypotSSHServer(ip, self.log_event, self.is_ip_blocked)

            try:
                transport.start_server(server=server)
            except paramiko.SSHException:
                return

            channel = transport.accept(20)
            if channel is None:
                return

            server.event.wait(10)
            if not server.event.is_set():
                channel.close()
                return

            # Gửi banner Linux chào mừng
            banner = (
                "\r\nWelcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n"
                " * Documentation:  https://help.ubuntu.com\r\n"
                " * Management:     https://landscape.canonical.com\r\n"
                " * Support:        https://ubuntu.com/advantage\r\n\r\n"
                f"System information as of {datetime.now().strftime('%a %b %d %H:%M:%S UTC %Y')}\r\n"
                "  System load:  0.08, 0.03, 0.01      Processes:           112\r\n"
                "  Usage of /:   18.4% of 38.70GB      Users logged in:     1\r\n"
                "  Memory usage: 22%                   IPv4 address for eth0: 10.0.3.15\r\n\r\n"
                "Last login: Fri Oct  2 08:44:12 2026 from 192.168.1.100\r\n"
            )
            channel.send(banner)

            # Shell tương tác
            prompt = f"{server.authenticated_user or 'root'}@ubuntu-srv:~# "
            channel.send(prompt)

            cmd_buffer = ""
            while channel.active:
                data = channel.recv(1024)
                if not data:
                    break

                for b in data:
                    char = chr(b)
                    if char in ("\r", "\n"):
                        channel.send("\r\n")
                        cmd = cmd_buffer.strip()
                        cmd_buffer = ""

                        if cmd:
                            # Ghi nhận lệnh gõ vào log Cowrie
                            self.log_event({
                                "eventid": "cowrie.command.input",
                                "src_ip": ip,
                                "session": server.session_id,
                                "input": cmd,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })

                            # Xử lý lệnh giả lập
                            response = self._execute_mock_command(cmd, ip, server.session_id)
                            if response == "__EXIT__":
                                channel.close()
                                return
                            if response:
                                channel.send(response)

                        channel.send(prompt)
                    elif char == "\x03":  # Ctrl+C
                        channel.send("^C\r\n")
                        cmd_buffer = ""
                        channel.send(prompt)
                    elif char in ("\x08", "\x7f"):  # Backspace
                        if cmd_buffer:
                            cmd_buffer = cmd_buffer[:-1]
                            channel.send("\b \b")
                    else:
                        cmd_buffer += char
                        channel.send(char)  # Echo ký tự

        except Exception as e:
            pass
        finally:
            if transport:
                transport.close()
            client_socket.close()

    def _execute_mock_command(self, cmd: str, ip: str, session_id: str) -> str:
        cmd_lower = cmd.lower().strip()
        parts = cmd_lower.split()
        base = parts[0] if parts else ""

        if base in ("exit", "logout", "quit"):
            return "__EXIT__"
        elif base == "clear":
            return "\033[H\033[2J"
        elif base in ("help", "?"):
            return (
                "Mini-SOC Honeypot Interactive Bash Environment\r\n"
                "Available commands: whoami, id, uname, pwd, ls, cat, ps, ifconfig, ip, history, wget, curl, ping, clear, exit\r\n"
                "Honeytoken Decoy targets: cat /root/.aws/credentials, cat db_backup.sql\r\n"
            )
        elif base == "sudo":
            if len(parts) > 1:
                return self._execute_mock_command(" ".join(parts[1:]), ip, session_id)
            return "usage: sudo command\r\n"
        elif base == "whoami":
            return "root\r\n"
        elif base == "id":
            return "uid=0(root) gid=0(root) groups=0(root)\r\n"
        elif base == "pwd":
            return "/root\r\n"
        elif base == "uname":
            return "Linux ubuntu-srv 5.15.0-89-generic #99-Ubuntu SMP Mon Oct 30 20:49:19 UTC 2023 x86_64 GNU/Linux\r\n"
        elif base == "ls":
            return (
                ".aws  .bash_history  .bashrc  .profile  db_backup.sql\r\n"
            )
        elif base in ("ifconfig", "ip"):
            return (
                "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\r\n"
                "        inet 192.168.1.150  netmask 255.255.255.0  broadcast 192.168.1.255\r\n"
                "        inet6 fe80::a00:27ff:fe4e:66b1  prefixlen 64  scopeid 0x20<link>\r\n"
                "        ether 08:00:27:4e:66:b1  txqueuelen 1000  (Ethernet)\r\n"
            )
        elif base == "history":
            return (
                "    1  cd /var/backups\r\n"
                "    2  ls -la\r\n"
                "    3  cat db_backup.sql\r\n"
                "    4  curl http://internal-vault.corp/keys\r\n"
                "    5  history\r\n"
            )
        elif base == "echo":
            return " ".join(parts[1:]) + "\r\n"
        elif base == "ping":
            target_host = parts[1] if len(parts) > 1 else "8.8.8.8"
            return (
                f"PING {target_host} ({target_host}) 56(84) bytes of data.\r\n"
                f"64 bytes from {target_host}: icmp_seq=1 ttl=116 time=14.2 ms\r\n"
                f"64 bytes from {target_host}: icmp_seq=2 ttl=116 time=14.5 ms\r\n"
            )
        elif "cat" in base or (len(parts) > 1 and parts[0] == "cat"):
            target = parts[1] if len(parts) > 1 else ""
            if "aws" in target or "credentials" in target:
                return (
                    "[default]\r\n"
                    "aws_access_key_id = AKIAIOSFODNN7CANARYAWS\r\n"
                    "aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\r\n"
                    "# Honeytoken Canary Beacon (HTTP Verification Endpoint):\r\n"
                    "# http://127.0.0.1:8080/canary/aws_verify?token=canary_aws_8892\r\n"
                )
            elif "history" in target:
                return (
                    "ls -la\r\n"
                    "cd /var/backups\r\n"
                    "cat db_backup.sql\r\n"
                    "# Download emergency hotfix patch for critical zero-day:\r\n"
                    "curl -s http://127.0.0.1:8080/canary/patch.sh | bash\r\n"
                    "history -c\r\n"
                )
            elif "pass" in target or "backup" in target or "db" in target or "sql" in target:
                return (
                    "-- Production Database Backup 2026\r\n"
                    "CREATE DATABASE enterprise_core;\r\n"
                    "INSERT INTO users VALUES ('superadmin', '$2a$12$e8rO2zM4vL1kH...', 'admin@corp.internal');\r\n"
                    "-- Internal Single-Sign-On (SSO) Portal:\r\n"
                    "-- http://127.0.0.1:8080/canary/db_verify?token=canary_sql_9941\r\n"
                )
            elif "passwd" in target:
                return (
                    "root:x:0:0:root:/root:/bin/bash\r\n"
                    "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\r\n"
                    "bin:x:2:2:bin:/bin:/usr/sbin/nologin\r\n"
                    "ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash\r\n"
                )
            elif "cpuinfo" in target:
                return "model name : Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz\r\ncpu MHz : 2400.046\r\n"
            else:
                return f"cat: {target}: No such file or directory\r\n"
        elif base in ("wget", "curl"):
            url = parts[1] if len(parts) > 1 else "http://malicious.c2/dropper.sh"
            # Ghi nhận tải mã độc
            mock_file = os.path.abspath("./data/downloads/mirai_payload.sh")
            self.log_event({
                "eventid": "cowrie.session.file_download",
                "src_ip": ip,
                "session": session_id,
                "url": url,
                "outfile": mock_file,
                "shasum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return f"Downloading {url} ... 100% [===================>] Done.\r\n"
        elif base == "ps":
            return (
                "  PID TTY          TIME CMD\r\n"
                "    1 ?        00:00:01 systemd\r\n"
                "  842 ?        00:00:00 sshd\r\n"
                "  912 pts/0    00:00:00 bash\r\n"
                "  950 pts/0    00:00:00 ps\r\n"
            )
        else:
            return f"bash: {cmd}: command not found\r\n"

    def start(self):
        """Khởi động socket lắng nghe SSH Honeypot trong luồng riêng."""
        self.is_running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        self.server_socket.settimeout(1.0)

        print(f"[🛡️ SSH HONEYPOT] Đang lắng nghe kết nối SSH THẬT tại port {self.port} (0.0.0.0:{self.port})")
        print(f"    👉 Thử nghiệm kết nối thật: ssh root@127.0.0.1 -p {self.port}\n")

        while self.is_running:
            try:
                client_sock, addr = self.server_socket.accept()
                t = threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except Exception:
                break

    def start_background(self):
        self._thread = threading.Thread(target=self.start, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
