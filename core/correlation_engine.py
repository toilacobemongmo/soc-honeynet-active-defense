"""
Module: correlation_engine.py
Mục đích: Động cơ tương quan sự kiện an ninh (Security Event Correlation Engine).
Ánh xạ các sự kiện Honeypot thành TTPs chuẩn MITRE ATT&CK và phát hiện các hành vi tấn công phức tạp.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import time
from typing import Dict, List, Optional


@dataclass
class ThreatAlert:
    alert_id: str
    rule_name: str
    mitre_technique_id: str
    mitre_technique_name: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    source_ip: str
    timestamp: str
    details: Dict
    recommended_action: str


class EventCorrelationEngine:
    def __init__(self, brute_force_threshold: int = 5, window_seconds: int = 60):
        self.brute_force_threshold = brute_force_threshold
        self.window_seconds = window_seconds

        # Lưu lịch sử login thất bại theo IP: ip -> list of timestamps
        self.failed_logins: Dict[str, List[float]] = defaultdict(list)
        # Lưu các phiên đang active: session_id -> metadata
        self.active_sessions: Dict[str, Dict] = {}

    def process_event(self, event: dict) -> Optional[ThreatAlert]:
        """Phân tích một sự kiện từ Cowrie và trả về Cảnh báo nếu thỏa mãn quy tắc tương quan."""
        eventid = event.get("eventid", "")
        src_ip = event.get("src_ip", "0.0.0.0")
        timestamp = event.get("timestamp", datetime.now(timezone.utc).isoformat())
        now = time.time()

        # 1. Phát hiện Tấn công Dò quét mật khẩu (MITRE ATT&CK T1110 - Brute Force)
        if eventid == "cowrie.login.failed":
            username = event.get("username", "")
            password = event.get("password", "")

            # Xóa các mốc thời gian đã trượt ra ngoài khung cửa sổ (time window)
            self.failed_logins[src_ip] = [
                t for t in self.failed_logins[src_ip] if now - t <= self.window_seconds
            ]
            self.failed_logins[src_ip].append(now)

            if len(self.failed_logins[src_ip]) >= self.brute_force_threshold:
                # Reset bộ đếm sau khi kích hoạt để tránh spam alert liên tục
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
                    details={
                        "failed_attempts": count,
                        "window_seconds": self.window_seconds,
                        "last_targeted_user": username,
                        "sample_password": password,
                    },
                    recommended_action="tarpit_and_block",
                )

        # 2. Phát hiện Truy cập trái phép thành công (MITRE ATT&CK T1078 - Valid Accounts)
        elif eventid == "cowrie.login.success":
            username = event.get("username", "")
            password = event.get("password", "")
            session_id = event.get("session", "")

            self.active_sessions[session_id] = {
                "src_ip": src_ip,
                "login_time": timestamp,
                "username": username,
                "commands": [],
            }

            return ThreatAlert(
                alert_id=f"ALT-LOGIN-{int(now)}",
                rule_name="Xâm nhập thành công vào Honeypot (Initial Access Breach)",
                mitre_technique_id="T1078",
                mitre_technique_name="Valid Accounts: Default / Guessed Credentials",
                severity="CRITICAL",
                source_ip=src_ip,
                timestamp=timestamp,
                details={
                    "compromised_user": username,
                    "accepted_password": password,
                    "session_id": session_id,
                },
                recommended_action="reverse_recon_and_honeytoken_monitor",
            )

        # 3. Phát hiện Tải mã độc (MITRE ATT&CK T1105 - Ingress Tool Transfer)
        elif eventid in ("cowrie.session.file_download", "cowrie.session.file_upload"):
            file_url = event.get("url", "")
            outfile = event.get("outfile", "")
            sha256 = event.get("shasum", "")

            return ThreatAlert(
                alert_id=f"ALT-DROP-{int(now)}",
                rule_name="Phát hiện Payload/Mã độc được tải lên hệ thống (Malware Staging)",
                mitre_technique_id="T1105",
                mitre_technique_name="Ingress Tool Transfer",
                severity="CRITICAL",
                source_ip=src_ip,
                timestamp=timestamp,
                details={
                    "payload_url": file_url,
                    "local_sandbox_file": outfile,
                    "sha256_hash": sha256,
                },
                recommended_action="quarantine_and_vt_scan",
            )

        # 4. Phân tích lệnh thực thi đáng ngờ (MITRE ATT&CK T1059 - Command Execution & Discovery)
        elif eventid == "cowrie.command.input":
            cmd = event.get("input", "")
            session_id = event.get("session", "")

            # Kiểm tra xem có thực sự MỞ/ĐỌC nội dung file Honeytoken không (MITRE T1552)
            read_actions = ["cat", "head", "tail", "more", "less", "grep", "nano", "vim", "vi", "cp", "scp", "strings"]
            is_read_op = any(cmd.lower().strip().startswith(act + " ") or f"| {act}" in cmd.lower() for act in read_actions)
            honeytoken_keywords = ["credentials", "id_rsa", "canary", "password", "backup", ".bash_history"]
            is_honeytoken_breach = is_read_op and any(kw in cmd.lower() for kw in honeytoken_keywords)

            if is_honeytoken_breach:
                return ThreatAlert(
                    alert_id=f"ALT-CANARY-{int(now)}",
                    rule_name="Bẫy Honeytoken bị kích hoạt (Canary Token Access Detected)",
                    mitre_technique_id="T1552.001",
                    mitre_technique_name="Unsecured Credentials: Credentials In Files",
                    severity="CRITICAL",
                    source_ip=src_ip,
                    timestamp=timestamp,
                    details={
                        "triggered_command": cmd,
                        "session_id": session_id,
                        "objective": "Attacker trying to steal credential breadcrumbs",
                    },
                    recommended_action="activate_de_cloaking_and_isolate",
                )

            # Các lệnh thu thập thông tin hệ thống (Discovery: T1082, T1016)
            recon_keywords = ["uname -a", "cat /etc/issue", "cat /proc/cpuinfo", "ifconfig", "ip a", "whoami", "crontab -l"]
            if any(kw in cmd.lower() for kw in recon_keywords):
                return ThreatAlert(
                    alert_id=f"ALT-DISC-{int(now)}",
                    rule_name="Kẻ tấn công thực hiện trinh sát nội bộ (System Information Discovery)",
                    mitre_technique_id="T1082",
                    mitre_technique_name="System Information Discovery",
                    severity="MEDIUM",
                    source_ip=src_ip,
                    timestamp=timestamp,
                    details={
                        "recon_command": cmd,
                        "session_id": session_id,
                    },
                    recommended_action="log_telemetry",
                )

        return None
