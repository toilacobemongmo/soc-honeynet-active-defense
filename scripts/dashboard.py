"""
Web SOC Dashboard: Giao diện Trung tâm Điều hành An ninh Mạng (Mini-SOC & SOAR Dashboard).
Chạy bằng Streamlit: streamlit run scripts/dashboard.py
"""

from datetime import datetime
import json
import os
import sys
import pandas as pd
import streamlit as st

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.correlation_engine import EventCorrelationEngine
from core.reverse_intel import ReverseIntelligenceEngine

st.set_page_config(
    page_title="Mini-SOC Active Defense & SOAR Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOG_PATH = os.path.abspath("./data/cowrie.json")
DOWNLOADS_DIR = os.path.abspath("./data/downloads")


def load_events():
    events = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        pass
    return events


def analyze_events(events):
    engine = EventCorrelationEngine(brute_force_threshold=5, window_seconds=60)
    alerts = []
    blocked_ips = set()
    honeytoken_hits = 0

    for evt in events:
        alert = engine.process_event(evt)
        if alert:
            alerts.append(alert)
            if alert.recommended_action == "tarpit_and_block":
                blocked_ips.add(alert.source_ip)
            if "Honeytoken" in alert.rule_name or "CANARY" in alert.alert_id:
                honeytoken_hits += 1

    return alerts, blocked_ips, honeytoken_hits


# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/shield.png", width=70)
st.sidebar.title("Mini-SOC Control")
st.sidebar.markdown("**Active Defense & SOAR Deception**")
st.sidebar.markdown("---")

st.sidebar.markdown("### ⚡ Kích hoạt Tấn công Giả lập")
if st.sidebar.button("💥 Chạy 4 Kịch bản Red Team", type="primary"):
    with st.spinner("Đang bắn kịch bản tấn công mẫu vào Honeypot..."):
        from scripts.simulate_attack import (
            simulate_scenario_1_bruteforce,
            simulate_scenario_2_login_and_recon,
            simulate_scenario_3_honeytoken_breach,
            simulate_scenario_4_malware_drop,
        )
        simulate_scenario_1_bruteforce()
        simulate_scenario_2_login_and_recon()
        simulate_scenario_3_honeytoken_breach()
        simulate_scenario_4_malware_drop()
        st.sidebar.success("Đã sinh 4 kịch bản tấn công thành công!")
        st.rerun()

if st.sidebar.button("🔄 Làm mới dữ liệu (Refresh)"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 Kết nối SSH Honeypot")
st.sidebar.code("ssh root@127.0.0.1 -p 2222\n# Pass thử: root123 hoặc sai >5 lần", language="bash")

# Main content
events = load_events()
alerts, blocked_ips, honeytoken_hits = analyze_events(events)

st.title("🛡️ Trung tâm Điều hành An ninh Mạng Chủ động (Mini-SOC & SOAR)")
st.caption("Tích hợp SSH Cowrie Honeypot, Phân tích TTPs MITRE ATT&CK và Tự động Phản ứng Sự cố")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng sự kiện Log Cowrie", f"{len(events):,}", delta="Live Feed")
col2.metric("Sự cố An ninh (Threat Alerts)", f"{len(alerts):,}", delta="MITRE Correlated", delta_color="inverse")
col3.metric("IP bị SOAR Firewall chặn", f"{len(blocked_ips)}", delta="Active Defense", delta_color="inverse")
col4.metric("Bẫy Honeytoken kích hoạt", f"{honeytoken_hits}", delta="Deception Beacon", delta_color="inverse")

st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🚨 Danh sách Sự cố & Phản ứng SOAR",
    "🔎 Trinh sát ngược & Tình báo Đối phương (OSINT)",
    "📜 Nhật ký Raw Log Honeypot",
])

with tab1:
    st.subheader("Cảnh báo Sự cố được Động cơ SOAR Tương quan")
    if not alerts:
        st.info("Chưa có sự cố nào được ghi nhận. Hãy bấm nút 'Chạy 4 Kịch bản Red Team' ở thanh bên trái hoặc kết nối SSH vào port 2222!")
    else:
        table_data = []
        for a in reversed(alerts):
            table_data.append({
                "Mã sự cố": a.alert_id,
                "Thời gian": a.timestamp,
                "Mức độ": a.severity,
                "Quy tắc phát hiện": a.rule_name,
                "Kỹ thuật MITRE": f"{a.mitre_technique_id} - {a.mitre_technique_name}",
                "IP Tấn công": a.source_ip,
                "Hành động SOAR": a.recommended_action,
            })
        df_alerts = pd.DataFrame(table_data)

        def color_severity(val):
            if val == "CRITICAL":
                return "color: #ff4b4b; font-weight: bold;"
            elif val == "HIGH":
                return "color: #ffa421; font-weight: bold;"
            elif val == "MEDIUM":
                return "color: #ffd166; font-weight: bold;"
            return "color: #06d6a0;"

        try:
            st.dataframe(df_alerts.style.map(color_severity, subset=["Mức độ"]), use_container_width=True, height=350)
        except Exception:
            st.dataframe(df_alerts, use_container_width=True, height=350)

with tab2:
    st.subheader("Trinh sát ngược (Reverse Reconnaissance & OSINT)")
    unique_ips = list(set([a.source_ip for a in alerts if a.source_ip not in ("0.0.0.0", "127.0.0.1")]))
    if not unique_ips:
        unique_ips = ["185.220.101.5", "45.33.32.156", "103.20.144.12", "194.87.139.12"]

    selected_ip = st.selectbox("Chọn IP đối phương cần trinh sát:", unique_ips)
    if selected_ip:
        rev_engine = ReverseIntelligenceEngine()
        with st.spinner(f"Đang trinh sát ngược IP {selected_ip}..."):
            recon = rev_engine.gather_full_recon(selected_ip)

        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.markdown("#### 🌍 Thông tin Định vị & Mạng (GeoIP)")
            geo = recon.get("geo_intel", {})
            st.write(f"• **Quốc gia:** {geo.get('country', 'N/A')} ({geo.get('countryCode', 'N/A')})")
            st.write(f"• **Thành phố:** {geo.get('city', 'N/A')}")
            st.write(f"• **Nhà mạng (ISP):** {geo.get('isp', 'N/A')}")
            st.write(f"• **Tổ chức (Org):** {geo.get('org', 'N/A')}")
            st.write(f"• **ASN:** {geo.get('as', 'N/A')}")

        with r_col2:
            st.markdown("#### 🛡️ Danh tiếng Nguy hại & Nhận diện")
            rep = recon.get("reputation", {})
            score = rep.get("abuseConfidenceScore", 0)
            st.write(f"• **Điểm độc hại AbuseIPDB:** `{score}%`")
            st.progress(score / 100)
            st.write(f"• **Số lượt báo cáo toàn cầu:** {rep.get('totalReports', 'N/A')}")
            st.write(f"• **Cổng dịch vụ quét được:** `{recon.get('active_services', [])}`")
            st.write(f"• **Phân loại đối thủ:** **{recon.get('threat_classification', 'Unknown')}**")

with tab3:
    st.subheader("Nhật ký Luồng Sự kiện Thô (Raw Cowrie Log Feed)")
    if not events:
        st.write("File log trống.")
    else:
        st.dataframe(pd.DataFrame(list(reversed(events[-50:]))), use_container_width=True, height=400)
