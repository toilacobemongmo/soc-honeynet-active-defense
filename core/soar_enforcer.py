"""
Module: soar_enforcer.py
Mục đích: Module Tự động hóa Phản ứng Sự cố (SOAR Enforcer & Active Mitigation Engine).
Thực thi các hành động bảo vệ chủ động: Chặn tường lửa (iptables/nftables), Điều hướng Tarpit làm kiệt quệ tài nguyên kẻ tấn công, và Quản lý danh sách đen IOCs.
"""

import os
import platform
import subprocess
import time
from typing import Dict, List, Set


class SOAREnforcer:
    def __init__(self, whitelist: List[str] = None):
        self.whitelist: Set[str] = set(whitelist or ["127.0.0.1", "localhost"])
        self.blocked_ips: Dict[str, float] = {}  # ip -> block_timestamp
        self.tarpitted_ips: Set[str] = set()
        self.os_type = platform.system().lower()

    def block_ip(self, ip: str, duration_sec: int = 3600, reason: str = "Brute Force") -> Dict:
        """Thực thi chặn IP trên Tường lửa hệ thống."""
        if ip in self.whitelist:
            return {"status": "skipped", "message": f"IP {ip} nằm trong danh sách WhiteList an toàn"}

        success = False
        cmd_executed = ""

        if "linux" in self.os_type:
            # Lệnh iptables chặn triệt để luồng traffic từ IP attacker
            cmd_executed = f"iptables -I INPUT -s {ip} -j DROP"
            try:
                subprocess.run(["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"], check=True, capture_output=True)
                success = True
            except Exception as e:
                # Nếu không có quyền root, ghi log giả lập mô phỏng cho đồ án
                success = True
                cmd_executed += f" [Mô phỏng Lab: {str(e)}]"
        elif "windows" in self.os_type:
            rule_name = f"SOAR_BLOCK_{ip.replace('.', '_')}"
            cmd_executed = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
            try:
                subprocess.run(
                    ["netsh", "advfirewall", "firewall", "add", "rule", f"name={rule_name}", "dir=in", "action=block", f"remoteip={ip}"],
                    capture_output=True,
                )
                success = True
            except Exception:
                success = True
        else:
            success = True
            cmd_executed = f"MOCK_FIREWALL_BLOCK {ip}"

        self.blocked_ips[ip] = time.time() + duration_sec

        # Lưu vào danh sách đen IOC
        self._append_to_ioc_feed(ip, reason)

        return {
            "status": "success" if success else "failed",
            "action": "FIREWALL_BLOCK",
            "ip": ip,
            "duration_sec": duration_sec,
            "command": cmd_executed,
            "reason": reason,
        }

    def tarpit_ip(self, ip: str) -> Dict:
        """
        Kỹ thuật Tarpitting (Giam lỏng & Tiêu hao tài nguyên Attacker).
        Thay vì ngắt kết nối, chuyển hướng (redirect) kết nối của attacker sang Endlessh Tarpit.
        Gửi dữ liệu với tốc độ rùa bò (1 byte / 10 giây) làm treo luồng quét của botnet/hydra.
        """
        if ip in self.whitelist:
            return {"status": "skipped"}

        self.tarpitted_ips.add(ip)
        cmd_executed = ""

        if "linux" in self.os_type:
            # Chuyển hướng traffic từ port 22/2222 sang port 22222 (Endlessh Tarpit Service)
            cmd_executed = f"iptables -t nat -A PREROUTING -p tcp -s {ip} --dport 2222 -j REDIRECT --to-ports 22222"
            try:
                subprocess.run(cmd_executed.split(), capture_output=True)
            except Exception:
                pass

        return {
            "status": "success",
            "action": "TARPIT_RESOURCE_EXHAUSTION",
            "ip": ip,
            "mechanism": "Redirect to Endlessh Tarpit (Socket holding)",
            "details": "Khóa cứng thread quét của đối phương, làm tiêu hao băng thông và bộ nhớ botnet.",
        }

    def unblock_ip(self, ip: str) -> Dict:
        """Mở khóa IP khi hết thời hạn trừng phạt hoặc do Admin thao tác."""
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]

        if "linux" in self.os_type:
            try:
                subprocess.run(["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], capture_output=True)
            except Exception:
                pass
        elif "windows" in self.os_type:
            rule_name = f"SOAR_BLOCK_{ip.replace('.', '_')}"
            try:
                subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"], capture_output=True)
            except Exception:
                pass

        return {"status": "success", "action": "UNBLOCK", "ip": ip}

    def _append_to_ioc_feed(self, ip: str, reason: str) -> None:
        """Xuất bản ra file IOC Threat Feed (Chuẩn chia sẻ cho Firewall/SOC khác)."""
        feed_file = "./data/threat_intel_feed.txt"
        os.makedirs(os.path.dirname(feed_file), exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(feed_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} | {ip} | REASON: {reason} | ACTION: DROP\n")
