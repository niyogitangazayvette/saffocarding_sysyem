import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_autorefresh import st_autorefresh

# --- Page Config ---
st.set_page_config(page_title="Scaffolding Safety Dashboard", layout="wide")

# --- Custom CSS Styling with Brefonse (dark gray) Background and White Font + Bordered Metrics ---
st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #1f2937 !important;  /* brefonse/dark gray */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: white !important;
    }
    .section {
        background-color: rgba(30, 30, 30, 0.95);
        padding: 30px;
        margin-bottom: 25px;
        border-radius: 12px;
        border: 2px solid white;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
    }
    h1, h2, h3, .stSubheader {
        color: #00ffff !important;
    }
    .custom-metric {
        background-color: rgba(255, 255, 255, 0.07);
        border: 2px solid white;
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

# --- SMS Alert with Textbelt ---
def send_sms_alert(tilt, vibration):
    try:
        message_text = f"ALERT! Scaffold danger. Tilt:{tilt}°, Vib:{vibration}."
        if len(message_text) > 160:
            st.warning("Message too long. Please reduce characters.")
            return
        response = requests.post('https://textbelt.com/text', {
            'phone': '+250788886315',
            'message': message_text,
            'key': 'textbelt'
        })
        result = response.json()
        if result.get('success'):
            st.success("🚨 SMS alert sent successfully!")
        else:
            st.warning(f"SMS failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to send SMS alert: {e}")

# --- Title and Description ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.title("🛠️ Scaffolding Safety Monitoring System (Live Stream)")
    st.markdown("Monitor scaffold **tilt**, **vibration**, **distance from ground**, and **sound levels** in real-time. Data updates every 5 seconds, categorized by risk level.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Simulate Data ---
tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state = get_simulated_sensor_data()
status, emoji = evaluate_status(tilt)

# --- Display System Metrics ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader(f"System Status: {emoji} {status}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Tilt Angle (°)</h4>
            <p>{tilt}°</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Vibration Level</h4>
            <p>{vibration}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Distance from Ground (cm)</h4>
            <p>{distance}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Sound Level (dB)</h4>
            <p>{sound_level}</p>
        </div>
        """, unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Bluetooth Status</h4>
            <p>{"🟦 Connected" if bluetooth_signal else "❌ Disconnected"}</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="custom-metric">
            <h4>Buzzer</h4>
            <p>{buzzer_state}</p>
        </div>
        """, unsafe_allow_html=True)

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

# --- Send SMS if DANGER ---
if status == "DANGER":
    send_sms_alert(tilt, vibration)

# --- Project Overview ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("""
    ### 📘 Project Overview
    The **Scaffolding Safety Monitoring System** is built with Arduino components to monitor tilt, vibration, sound levels, and distance on scaffolding.

    **Sensors and Modules:**
    - MPU6050 (Accelerometer + Gyroscope)
    - HC-SR04 Ultrasonic Sensor
    - Microphone or Sound Sensor
    - LEDs (Green, Yellow, Red)
    - Active Buzzer (alerts on danger)
    - HC-05 Bluetooth Module (wireless transmission)

    **Functionality:**
    - 🟢 SAFE: Tilt ≤ 5°
    - 🟠 WARNING: Tilt between 5° and 10°
    - 🔴 DANGER: Tilt > 10°
    - Vibration triggers buzzer if above threshold
    - Ultrasonic sensor detects distance (collapse risk)
    - Bluetooth HC-05 sends data wirelessly

    ⚠️ This dashboard simulates sensor values and is ready for real data integration.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
