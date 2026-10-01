"""
Main Orchestrator: Hệ sinh thái Phòng thủ Chủ động (Active Defense & SOAR Ecosystem).
Tích hợp Cowrie SSH Honeypot, Correlation Engine, Reverse Intel, Honeytokens và Telegram SOAR Bot.
"""

import os
import sys
import yaml

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from core.correlation_engine import EventCorrelationEngine, ThreatAlert
from core.cowrie_listener import CowrieLogListener
from core.honeytoken_manager import HoneytokenManager
from core.payload_analyzer import PayloadAnalyzer
from core.reverse_intel import ReverseIntelligenceEngine
from core.soar_enforcer import SOAREnforcer
from core.telegram_soar_bot import TelegramSOARBot


class MiniSOCActiveDefenseOrchestrator:
    def __init__(self, config_path: str = "config/config.yaml"):
        print("[*] Đang khởi động Hệ thống Mini-SOC Active Defense & SOAR...")
        self.config = self._load_config(config_path)

        # 1. Khởi tạo Phân hệ Phản ứng Sự cố (SOAR Enforcer)
        whitelist = self.config.get("soar_rules", {}).get("firewall_enforcement", {}).get("whitelist", [])
        self.enforcer = SOAREnforcer(whitelist=whitelist)

        # 2. Khởi tạo Phân hệ Trinh sát ngược (Reverse Intel)
        intel_cfg = self.config.get("threat_intel", {})
        self.reverse_intel = ReverseIntelligenceEngine(
            abuseipdb_key=intel_cfg.get("abuseipdb", {}).get("api_key"),
            shodan_key=intel_cfg.get("shodan", {}).get("api_key"),
        )

        # 3. Khởi tạo Phân hệ Bẫy Mồi Honeytoken (Active Deception)
        self.honeytoken_mgr = HoneytokenManager()

        # 4. Khởi tạo Phân hệ Phân tích Mã độc (Malware Analyzer)
        self.payload_analyzer = PayloadAnalyzer(
            vt_api_key=intel_cfg.get("virustotal", {}).get("api_key")
        )

        # 5. Khởi tạo Động cơ Tương quan Sự kiện (Correlation Engine)
        brute_cfg = self.config.get("soar_rules", {}).get("brute_force", {})
        self.correlation_engine = EventCorrelationEngine(
            brute_force_threshold=brute_cfg.get("threshold_attempts", 5),
            window_seconds=brute_cfg.get("time_window_sec", 60),
        )

        # 6. Khởi tạo Telegram SOAR Bot tương tác 2 chiều
        tg_cfg = self.config.get("telegram", {})
        self.telegram_bot = TelegramSOARBot(
            bot_token=tg_cfg.get("bot_token", ""),
            chat_id=tg_cfg.get("chat_id", ""),
            action_callback=self._handle_analyst_action,
        )

        # 7. Khởi tạo Bộ lắng nghe Log Cowrie
        cowrie_log_path = self.config.get("cowrie", {}).get("log_path", "./data/cowrie.json")
        self.listener = CowrieLogListener(log_file_path=cowrie_log_path)

        print("[+] Toàn bộ phân hệ phòng thủ chủ động đã sẵn sàng hoạt động!")

    def _load_config(self, config_path: str) -> dict:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Không tìm thấy file cấu hình tại {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _handle_analyst_action(self, action: str, ip: str) -> dict:
        """Xử lý lệnh khi Chuyên viên SOC bấm nút trên Telegram."""
        print(f"\n[!] Nhận lệnh từ Telegram SOC Bot: Hành động '{action}' nhắm vào IP {ip}")

        if action == "recon":
            recon_data = self.reverse_intel.gather_full_recon(ip)
            summary = (
                f"🔎 <b>KẾT QUẢ TRINH SÁT NGƯỢC IP:</b> <code>{ip}</code>\n"
                f"• Quốc gia: {recon_data['geo_intel'].get('country')} ({recon_data['geo_intel'].get('city')})\n"
                f"• ISP: {recon_data['geo_intel'].get('isp')}\n"
                f"• Điểm độc hại (AbuseIPDB): {recon_data['reputation'].get('abuseConfidenceScore', 0)}%\n"
                f"• Cổng dịch vụ mở: {recon_data.get('active_services')}\n"
                f"• Phân loại đối thủ: <b>{recon_data.get('threat_classification')}</b>"
            )
            self.telegram_bot.send_simple_message(summary)
            return {"action": "Đã trinh sát ngược và gửi báo cáo tình báo"}

        elif action == "block":
            res = self.enforcer.block_ip(ip, duration_sec=3600, reason="SOC Analyst Manual Block")
            return res

        elif action == "tarpit":
            res = self.enforcer.tarpit_ip(ip)
            return res

        elif action == "unblock":
            res = self.enforcer.unblock_ip(ip)
            return res

        return {"action": "Không nhận diện được hành động"}

    def on_cowrie_event(self, event: dict) -> None:
        """Xử lý từng sự kiện log từ Cowrie."""
        alert: ThreatAlert = self.correlation_engine.process_event(event)
        if not alert:
            return

        print(f"\n[!] PHÁT HIỆN SỰ CỐ: {alert.rule_name} | IP: {alert.source_ip} | MITRE: {alert.mitre_technique_id}")

        # Tự động trinh sát ngược đối phương nếu mức độ nguy hiểm cao
        enriched_info = {}
        if alert.severity in ("HIGH", "CRITICAL"):
            recon = self.reverse_intel.gather_full_recon(alert.source_ip)
            enriched_info = {
                "Quốc gia/ISP": f"{recon['geo_intel'].get('country')} / {recon['geo_intel'].get('isp')}",
                "Phân loại hình thái": recon.get("threat_classification"),
                "Mức độ uy tín độc hại": f"{recon['reputation'].get('abuseConfidenceScore', 0)}% (AbuseIPDB)",
            }
            alert.details.update(enriched_info)

        # Xử lý tự động theo quy tắc SOAR (Automated Playbook)
        if alert.recommended_action == "tarpit_and_block":
            auto_block = self.config.get("soar_rules", {}).get("firewall_enforcement", {}).get("auto_block", False)
            if auto_block:
                self.enforcer.block_ip(alert.source_ip, reason="Automated Brute Force Mitigation")
                alert.details["Hành động SOAR tự động"] = "Đã khóa IP trên Firewall trong 3600s"

        elif alert.recommended_action == "quarantine_and_vt_scan":
            file_path = alert.details.get("local_sandbox_file")
            if file_path and os.path.exists(file_path):
                analysis = self.payload_analyzer.analyze_file(file_path)
                alert.details["Malware Family"] = analysis.get("malware_family")
                alert.details["VirusTotal Positives"] = f"{analysis['virustotal_intel'].get('positives')}/{analysis['virustotal_intel'].get('total')}"

        # Gửi cảnh báo tương tác qua Telegram
        self.telegram_bot.send_incident_alert({
            "rule_name": alert.rule_name,
            "source_ip": alert.source_ip,
            "mitre_id": alert.mitre_technique_id,
            "mitre_name": alert.mitre_technique_name,
            "severity": alert.severity,
            "timestamp": alert.timestamp,
            "details": alert.details,
            "recommended_action": alert.recommended_action,
        })

    def run(self) -> None:
        """Khởi động toàn bộ luồng hoạt động."""
        self.telegram_bot.start_polling()
        print("[*] Đang lắng nghe luồng sự kiện Cowrie... (Nhấn Ctrl+C để dừng)")
        try:
            self.listener.start(callback=self.on_cowrie_event)
        except KeyboardInterrupt:
            print("\n[-] Dừng hệ thống.")
            self.listener.stop()


if __name__ == "__main__":
    orchestrator = MiniSOCActiveDefenseOrchestrator()
    orchestrator.run()
