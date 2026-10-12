"""
Module: correlation_engine.py
Mục đích: Động cơ tương quan sự kiện an ninh (Security Event Correlation Engine).
Tích hợp:
1. Dynamic Threat Risk Scoring (Chấm điểm nguy cơ tích lũy 0-100).
2. Multi-tier Progressive Mitigation (Không chỉ Tarpit: Giám sát -> Bẫy mồi -> Tarpit -> Adaptive Block).
3. Session Telemetry & Attacker Forensics Tracking.
"""

from collections import defaultdict
from dataclasses import dataclass, field
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
    risk_score: int = 0  # Dynamic Risk Score 0 - 100


class EventCorrelationEngine:
    """
    Động cơ tương quan thế hệ mới:
    - Tích hợp Dynamic Risk Scoring Engine
    - Theo dõi TTPs và lưu vết Forensic keystrokes của từng session
    - Đưa ra phản ứng đa tầng (Multi-tier Action Escalation)
    """

    def __init__(self, brute_force_threshold: int = 5, window_seconds: int = 60):
        self.brute_force_threshold = brute_force_threshold
        self.window_seconds = window_seconds

        # Lưu lịch sử login thất bại theo IP: ip -> list of timestamps
        self.failed_logins: Dict[str, List[float]] = defaultdict(list)
        # Lưu các phiên đang active: session_id -> metadata
        self.active_sessions: Dict[str, Dict] = {}

        # 1. Dynamic Risk Scoring per IP: ip -> {score, history_actions, last_seen}
        self.ip_risk_profiles: Dict[str, Dict] = defaultdict(
            lambda: {
                "score": 0,
                "violation_count": 0,
                "ttps": set(),
                "last_seen": time.time(),
                "escalation_level": "MONITOR",  # MONITOR -> TARPIT -> RESTRICT -> BLOCK
            }
        )

        # 2. Session Forensics History for Terminal Replay
        self.session_recordings: Dict[str, List[Dict]] = defaultdict(list)

    def calculate_risk_delta(self, ttp_type: str, weight: int = 10) -> int:
        """Tính điểm rủi ro gia tăng theo từng hành vi tấn công."""
        scoring_table = {
            "BRUTE_FORCE_ATTEMPT": 10,
            "BRUTE_FORCE_BURST": 30,
            "SUCCESSFUL_BREACH": 35,
            "SYSTEM_RECON": 20,
            "MALWARE_DOWNLOAD": 45,
            "HONEYTOKEN_ACCESS": 50,
            "TOR_EXIT_NODE": 15,
        }
        return scoring_table.get(ttp_type, weight)

    def update_ip_risk(self, ip: str, ttp_code: str, ttp_name: str, delta: int) -> int:
        """Cập nhật điểm rủi ro tích lũy cho IP và phân hạng mức độ phản ứng."""
        profile = self.ip_risk_profiles[ip]
        profile["score"] = min(100, profile["score"] + delta)
        profile["violation_count"] += 1
        profile["ttps"].add(f"{ttp_code}:{ttp_name}")
        profile["last_seen"] = time.time()

        score = profile["score"]
        if score >= 80:
            profile["escalation_level"] = "CONTAINMENT_BLOCK"
        elif score >= 55:
            profile["escalation_level"] = "TARPIT_EXHAUSTION"
        elif score >= 30:
            profile["escalation_level"] = "ACTIVE_DECEPTION"
        else:
            profile["escalation_level"] = "PASSIVE_MONITOR"

        return score

    def record_session_keystroke(self, session_id: str, src_ip: str, cmd: str, timestamp: str) -> None:
        """Lưu lại telemetry của phiên để hỗ trợ tính năng Replay Attack Session."""
        self.session_recordings[session_id].append({
            "timestamp": timestamp,
            "ip": src_ip,
            "command": cmd,
            "seq": len(self.session_recordings[session_id]) + 1,
        })

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

            delta = self.calculate_risk_delta("BRUTE_FORCE_ATTEMPT")
            self.update_ip_risk(src_ip, "T1110.001", "Password Guessing", delta)

            if len(self.failed_logins[src_ip]) >= self.brute_force_threshold:
                count = len(self.failed_logins[src_ip])
                self.failed_logins[src_ip].clear()

                total_risk = self.update_ip_risk(src_ip, "T1110", "Brute Force Threshold Hit", 25)
                rec_action = "tarpit_and_block" if total_risk >= 70 else "tarpit_slowdown"

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
                        "dynamic_risk_score": total_risk,
                        "escalation_tier": self.ip_risk_profiles[src_ip]["escalation_level"],
                    },
                    recommended_action=rec_action,
                    risk_score=total_risk,
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

            delta = self.calculate_risk_delta("SUCCESSFUL_BREACH")
            total_risk = self.update_ip_risk(src_ip, "T1078", "Valid Accounts Initial Breach", delta)

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
                    "dynamic_risk_score": total_risk,
                    "escalation_tier": self.ip_risk_profiles[src_ip]["escalation_level"],
                },
                recommended_action="reverse_recon_and_honeytoken_monitor",
                risk_score=total_risk,
            )

        # 3. Phát hiện Tải mã độc (MITRE ATT&CK T1105 - Ingress Tool Transfer)
        elif eventid in ("cowrie.session.file_download", "cowrie.session.file_upload"):
            file_url = event.get("url", "")
            outfile = event.get("outfile", "")
            sha256 = event.get("shasum", "")

            delta = self.calculate_risk_delta("MALWARE_DOWNLOAD")
            total_risk = self.update_ip_risk(src_ip, "T1105", "Ingress Tool Transfer", delta)

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
                    "dynamic_risk_score": total_risk,
                    "escalation_tier": self.ip_risk_profiles[src_ip]["escalation_level"],
                },
                recommended_action="quarantine_and_vt_scan",
                risk_score=total_risk,
            )

        # 4. Phân tích lệnh thực thi đáng ngờ (MITRE ATT&CK T1059 - Command Execution & Discovery)
        elif eventid == "cowrie.command.input":
            cmd = event.get("input", "")
            session_id = event.get("session", "")

            if session_id:
                self.record_session_keystroke(session_id, src_ip, cmd, timestamp)

            # Kiểm tra xem có thực sự MỞ/ĐỌC nội dung file Honeytoken không (MITRE T1552)
            read_actions = ["cat", "head", "tail", "more", "less", "grep", "nano", "vim", "vi", "cp", "scp", "strings"]
            is_read_op = any(cmd.lower().strip().startswith(act + " ") or f"| {act}" in cmd.lower() for act in read_actions)
            honeytoken_keywords = ["credentials", "id_rsa", "canary", "password", "backup", ".bash_history"]
            is_honeytoken_breach = is_read_op and any(kw in cmd.lower() for kw in honeytoken_keywords)

            if is_honeytoken_breach:
                delta = self.calculate_risk_delta("HONEYTOKEN_ACCESS")
                total_risk = self.update_ip_risk(src_ip, "T1552.001", "Credentials in Files Decoy", delta)

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
                        "dynamic_risk_score": total_risk,
                        "escalation_tier": self.ip_risk_profiles[src_ip]["escalation_level"],
                    },
                    recommended_action="activate_de_cloaking_and_isolate",
                    risk_score=total_risk,
                )

            # Các lệnh thu thập thông tin hệ thống (Discovery: T1082, T1016)
            recon_keywords = ["uname -a", "cat /etc/issue", "cat /proc/cpuinfo", "ifconfig", "ip a", "whoami", "crontab -l"]
            if any(kw in cmd.lower() for kw in recon_keywords):
                delta = self.calculate_risk_delta("SYSTEM_RECON")
                total_risk = self.update_ip_risk(src_ip, "T1082", "System Information Discovery", delta)

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
                        "dynamic_risk_score": total_risk,
                        "escalation_tier": self.ip_risk_profiles[src_ip]["escalation_level"],
                    },
                    recommended_action="log_telemetry",
                    risk_score=total_risk,
                )

        return None
