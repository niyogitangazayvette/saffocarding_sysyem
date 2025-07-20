import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Scaffolding Safety Dashboard", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #1f2937 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: white !important;
    }
    .section {
        background-color: rgba(31, 41, 55, 0.9);
        padding: 30px;
        margin-bottom: 25px;
        border-radius: 12px;
        border: 2px solid #3b4252;
        box-shadow: 0 4px 15px rgba(31, 41, 55, 0.9);
    }
    .custom-metric {
        background-color: transparent;
        border: 2px solid #3b4252;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .custom-metric h4 {
        color: #00ffff;
        font-size: 20px;
        margin-bottom: 5px;
    }
    .custom-metric p {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    h1, h2, h3, .stSubheader {
        color: #00ffff !important;
    }
    .bordered-card {
        border: 2px solid white !important;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 25px;
        background-color: #1f2937;
        box-shadow: 0 4px 15px rgba(31, 41, 55, 0.9);
    }
    .bordered-card-inner {
        background-color: rgba(31, 41, 55, 0.9);
        border-radius: 10px;
        padding: 20px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="data_refresh")

# --- Simulated Sensor Data ---
def get_simulated_sensor_data():
    tilt = round(np.random.uniform(0, 15), 2)
    vibration = round(np.random.uniform(0, 2.5), 2)
    distance = round(np.random.uniform(50, 200), 2)
    sound_level = round(np.random.uniform(20, 100), 2)
    bluetooth_signal = True if np.random.rand() > 0.1 else False
    buzzer_state = "ON" if tilt > 10 or vibration > 2.0 else "OFF"
    return tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state

# --- Safety Status ---
def evaluate_status(tilt):
    if tilt <= 5:
        return "SAFE", "🟢"
    elif tilt <= 10:
        return "WARNING", "🟠"
    else:
        return "DANGER", "🔴"

# --- SMS Alert using Twilio Secrets ---
def send_twilio_sms_alert(tilt, vibration):
    try:
        from twilio.rest import Client
        account_sid = st.secrets["TWILIO"]["ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO"]["AUTH_TOKEN"]
        from_phone = st.secrets["TWILIO"]["FROM_PHONE"]
        to_phones = st.secrets["TWILIO"]["TO_PHONE"].split(",")

        message_body = f"ALERT: Scaffolding DANGER!\nTilt: {tilt}°, Vibration: {vibration}"
        client = Client(account_sid, auth_token)

        for to_phone in to_phones:
            msg = client.messages.create(
                body=message_body,
                from_=from_phone,
                to=to_phone.strip()
            )
        st.success("🚨 Twilio SMS sent to all supervisors!")
    except Exception as e:
        st.error(f"❌ Failed to send Twilio SMS: {e}")

# --- Initialize Session State ---
if "log" not in st.session_state:
    st.session_state.log = []

# --- Title Card ---
with st.container():
    st.markdown('<div class="bordered-card"><div class="bordered-card-inner">', unsafe_allow_html=True)
    st.title("🛠️ Scaffolding Safety Monitoring System (Live Stream)")
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- Description ---
with st.container():
    st.markdown('<div class="bordered-card"><div class="bordered-card-inner">', unsafe_allow_html=True)
    st.markdown("Monitor scaffold **tilt**, **vibration**, **distance**, and **sound** in real-time. Auto-refresh every 5 seconds. Danger triggers SMS.")
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- Fetch Data ---
tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state = get_simulated_sensor_data()
status, emoji = evaluate_status(tilt)
timestamp = datetime.now().strftime("%H:%M:%S")

# --- Store Data in Session Log ---
st.session_state.log.append({
    "time": timestamp,
    "tilt": tilt,
    "vibration": vibration,
    "distance": distance,
    "sound": sound_level,
    "status": status
})

# --- System Metrics ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader(f"System Status: {emoji} {status}")
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"""<div class='custom-metric'><h4>Tilt Angle (°)</h4><p>{tilt}°</p></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class='custom-metric'><h4>Vibration Level</h4><p>{vibration}</p></div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class='custom-metric'><h4>Distance (cm)</h4><p>{distance}</p></div>""", unsafe_allow_html=True)
    col4.markdown(f"""<div class='custom-metric'><h4>Sound Level (dB)</h4><p>{sound_level}</p></div>""", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    col5.markdown(f"""<div class='custom-metric'><h4>Bluetooth Status</h4><p>{'🟦 Connected' if bluetooth_signal else '❌ Disconnected'}</p></div>""", unsafe_allow_html=True)
    col6.markdown(f"""<div class='custom-metric'><h4>Buzzer</h4><p>{buzzer_state}</p></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tilt Gauge ---
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=tilt,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Tilt Angle Gauge"},
    delta={'reference': 5},
    gauge={
        'axis': {'range': [None, 15]},
        'steps': [
            {'range': [0, 5], 'color': "lightgreen"},
            {'range': [5, 10], 'color': "orange"},
            {'range': [10, 15], 'color': "crimson"},
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 10
        }
    }
))

with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Trigger SMS if in Danger ---
if status == "DANGER":
    send_twilio_sms_alert(tilt, vibration)

# --- Project Overview ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("""
    ### 📘 Project Overview
    This dashboard displays real-time data from an Arduino-based safety system monitoring scaffolding tilt, vibration, distance, and sound.

    **Sensors & Modules:**
    - MPU6050: Tilt + Vibration
    - HC-SR04: Distance
    - Microphone: Sound level
    - LEDs + Buzzer: Alerts
    - HC-05: Bluetooth transmission

    **Danger triggers:**
    - 🔴 Tilt > 10°
    - High vibration
    - SMS alerts via Twilio (configured)

    ⚠️ This dashboard is simulation-ready and fully prepared for real sensor integration.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- History Chart ---
history_df = pd.DataFrame(st.session_state.log)

if not history_df.empty:
    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("### 📊 Sensor Data History (Last 10 mins)")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(x=history_df["time"], y=history_df["tilt"], name="Tilt", line=dict(color="cyan")))
        fig_hist.add_trace(go.Scatter(x=history_df["time"], y=history_df["vibration"], name="Vibration", line=dict(color="orange")))
        fig_hist.add_trace(go.Scatter(x=history_df["time"], y=history_df["distance"], name="Distance", line=dict(color="lightgreen")))
        fig_hist.update_layout(template="plotly_dark", xaxis_title="Time", yaxis_title="Sensor Values")
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
