"""
Module: payload_analyzer.py
Mục đích: Module Phân tích Mã độc & Cách ly Payload Độc hại (Malware Sandbox & Threat Analysis).
Tự động tính toán băm (SHA256/MD5), trích xuất IOCs từ mã độc do hacker tải lên Cowrie và tra cứu VirusTotal.
"""

import hashlib
import os
import re
from typing import Dict, List, Optional
import requests


class PayloadAnalyzer:
    def __init__(self, vt_api_key: Optional[str] = None):
        self.vt_api_key = vt_api_key

    def analyze_file(self, file_path: str) -> Dict:
        """Phân tích toàn diện file do kẻ tấn công tải lên máy bẫy."""
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        with open(file_path, "rb") as f:
            content = f.read()

        md5 = hashlib.md5(content).hexdigest()
        sha256 = hashlib.sha256(content).hexdigest()
        file_size = len(content)

        # Trích xuất chuỗi tĩnh (Static String Extraction) để tìm IP C2, URL độc hại
        extracted_iocs = self._extract_static_iocs(content)

        # Tra cứu VirusTotal (nếu có key)
        vt_report = self.query_virustotal(sha256)

        return {
            "file_name": os.path.basename(file_path),
            "file_size_bytes": file_size,
            "md5": md5,
            "sha256": sha256,
            "extracted_iocs": extracted_iocs,
            "virustotal_intel": vt_report,
            "malware_family": vt_report.get("family", "Unknown / Zero-day script"),
            "is_malicious": vt_report.get("positives", 0) > 0 or len(extracted_iocs["urls"]) > 0,
        }

    def _extract_static_iocs(self, content: bytes) -> Dict[str, List[str]]:
        """Trích xuất IP, URL và các lệnh nguy hiểm từ nội dung nhị phân/kịch bản."""
        text = content.decode("utf-8", errors="ignore")

        # Regex tìm IP và URL
        ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*"

        ips = list(set(re.findall(ip_pattern, text)))
        urls = list(set(re.findall(url_pattern, text)))

        # Nhận diện đặc trưng botnet phổ biến (Mirai, Tsunami, DDOS, Miner)
        signatures = []
        if "xmrig" in text.lower() or "stratum+tcp" in text.lower():
            signatures.append("Cryptocurrency Miner (XMRig / Monero)")
        if "/bin/busybox" in text or "dvrHelper" in text or "mirai" in text.lower():
            signatures.append("IoT Botnet Variant (Mirai / Gafgyt)")
        if "wget" in text and "chmod +x" in text:
            signatures.append("Multi-stage Malware Dropper Script")

        return {
            "ips": ips,
            "urls": urls,
            "signatures": signatures,
        }

    def query_virustotal(self, sha256_hash: str) -> Dict:
        """Truy vấn báo cáo phân tích mã độc từ VirusTotal."""
        if not self.vt_api_key or self.vt_api_key == "YOUR_VIRUSTOTAL_API_KEY":
            # Trả về kết quả mô phỏng mẫu phục vụ đồ án
            return {
                "positives": 48,
                "total": 72,
                "family": "Trojan.Linux.Mirai.Exploit",
                "permalink": f"https://www.virustotal.com/gui/file/{sha256_hash}",
                "simulated": True,
            }

        headers = {"x-apikey": self.vt_api_key}
        url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"

        try:
            resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                data = resp.json().get("data", {}).get("attributes", {})
                stats = data.get("last_analysis_stats", {})
                return {
                    "positives": stats.get("malicious", 0),
                    "total": sum(stats.values()),
                    "family": data.get("popular_threat_classification", {}).get("suggested_threat_label", "Malware"),
                    "permalink": f"https://www.virustotal.com/gui/file/{sha256_hash}",
                    "simulated": False,
                }
        except Exception as e:
            return {"error": str(e)}

        return {"positives": 0, "total": 0, "family": "Unrated"}
