"""
Module: telegram_soar_bot.py
Mục đích: Telegram SOAR Bot tương tác 2 chiều (Interactive Security Operations Bot).
Không chỉ gửi cảnh báo một chiều, Bot cung cấp các nút bấm tương tác (Inline Buttons) cho phép chuyên viên SOC:
- Quét ngược IP (Trigger Reverse OSINT)
- Chặn IP lập tức (Firewall Drop)
- Giam lỏng vào Tarpit (Exhaust Resources)
- Mở chặn IP (Whitelist/Release)
"""

import json
import threading
import time
from typing import Callable, Dict, Optional
import requests


class TelegramSOARBot:
    def __init__(self, bot_token: str, chat_id: str, action_callback: Optional[Callable[[str, str], Dict]] = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.action_callback = action_callback  # Hàm thực thi hành động: callback(action_type, ip)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_update_id = 0
        self.is_running = False

    def send_incident_alert(self, alert_data: Dict) -> bool:
        """Gửi thẻ cảnh báo sự cố kèm các nút bấm hành động tương tác."""
        if not self.bot_token or self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            # In ra màn hình console ở chế độ mô phỏng
            print("\n[TELEGRAM SOAR BOT SIMULATION]")
            print(f"🚨 TIÊU ĐỀ: {alert_data.get('rule_name')}")
            print(f"🎯 IP Mục tiêu: {alert_data.get('source_ip')}")
            print(f"🛡️ MITRE ATT&CK: {alert_data.get('mitre_id')} - {alert_data.get('mitre_name')}")
            print(f"⚙️ Hành động đề xuất: {alert_data.get('recommended_action')}")
            print("[NÚT BẤM CÓ SẴN]: [🔍 Quét ngược OSINT] | [⛔ Chặn IP ngay] | [⏳ Đưa vào Tarpit]\n")
            return True

        ip = alert_data.get("source_ip", "0.0.0.0")
        severity_icon = "🚨" if alert_data.get("severity") in ("CRITICAL", "HIGH") else "⚠️"

        text = (
            f"{severity_icon} <b>CẢNH BÁO AN NINH SOAR - MINI SOC</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>Sự kiện:</b> {alert_data.get('rule_name')}\n"
            f"<b>Mức độ:</b> <code>{alert_data.get('severity')}</code>\n"
            f"<b>Kẻ tấn công (IP):</b> <code>{ip}</code>\n"
            f"<b>Kỹ thuật MITRE:</b> <code>{alert_data.get('mitre_id')}</code> - {alert_data.get('mitre_name')}\n"
            f"<b>Thời gian:</b> <code>{alert_data.get('timestamp')}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>Chi tiết:</b>\n"
        )
        for k, v in alert_data.get("details", {}).items():
            text += f"• <i>{k}:</i> <code>{v}</code>\n"

        text += "\n👇 <b>Chọn hành động phản ứng chủ động:</b>"

        # Bàn phím nút bấm tương tác (Inline Keyboard)
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🔍 Trinh sát ngược OSINT", "callback_data": f"recon:{ip}"},
                    {"text": "⏳ Đưa vào Tarpit", "callback_data": f"tarpit:{ip}"},
                ],
                [
                    {"text": "⛔ Chặn Firewall tức thì", "callback_data": f"block:{ip}"},
                    {"text": "🔓 Mở khóa IP", "callback_data": f"unblock:{ip}"},
                ],
            ]
        }

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(reply_markup),
        }

        try:
            resp = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            print(f"Lỗi gửi tin nhắn Telegram: {e}")
            return False

    def send_simple_message(self, message: str) -> bool:
        """Gửi tin nhắn phản hồi văn bản đơn giản."""
        if not self.bot_token or self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            print(f"[BOT PHẢN HỒI]: {message}")
            return True

        try:
            requests.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"},
                timeout=5,
            )
            return True
        except Exception:
            return False

    def start_polling(self) -> None:
        """Chạy luồng nền lắng nghe tương tác nút bấm từ người dùng Telegram."""
        if not self.bot_token or self.bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            return

        self.is_running = True
        thread = threading.Thread(target=self._poll_loop, daemon=True)
        thread.start()

    def _poll_loop(self) -> None:
        while self.is_running:
            try:
                url = f"{self.base_url}/getUpdates?offset={self.last_update_id + 1}&timeout=10"
                resp = requests.get(url, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    for update in data.get("result", []):
                        self.last_update_id = update["update_id"]
                        if "callback_query" in update:
                            self._handle_callback(update["callback_query"])
            except Exception:
                time.sleep(2)

    def _handle_callback(self, query: Dict) -> None:
        """Xử lý khi chuyên viên SOC bấm vào các nút hành động."""
        query_id = query.get("id")
        data = query.get("data", "")
        # Phản hồi lại telegram để tắt biểu tượng loading trên nút
        try:
            requests.post(f"{self.base_url}/answerCallbackQuery", json={"callback_query_id": query_id})
        except Exception:
            pass

        if ":" not in data:
            return

        action, ip = data.split(":", 1)
        if self.action_callback:
            result = self.action_callback(action, ip)
            # Thông báo lại kết quả cho chuyên viên
            msg = f"🛡️ <b>HÀNH ĐỘNG ĐÃ THỰC THI:</b> <code>{action.upper()}</code>\n<b>Mục tiêu:</b> <code>{ip}</code>\n<b>Kết quả:</b> {result.get('action', 'Hoàn tất')}"
            self.send_simple_message(msg)
