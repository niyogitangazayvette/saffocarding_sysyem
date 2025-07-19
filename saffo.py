import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Scaffolding Safety Dashboard", layout="wide")

# --- Custom CSS Styling with Teal Gradient Background and Styled Sections ---
st.markdown("""
    <style>
    body, .main {
        background: linear-gradient(135deg, #008080 0%, #20b2aa 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #003333;
    }
    .section {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 25px 30px;
        margin-bottom: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        border: 2px solid #004d4d;
        color: #003333;
    }
    h1, h2, h3 {
        font-weight: 700;
        color: #004d4d;
    }
    .stMetric {
        font-weight: 600;
        color: #002626;
    }
    .stSuccess {
        color: #219653 !important;
    }
    .stWarning {
        color: #f2994a !important;
    }
    .stError {
        color: #eb5757 !important;
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
        response = requests.post('https://textbelt.com/text', {
            'phone': '+250788886315',  # Replace with your phone number including country code
            'message': message_text,
            'key': 'textbelt'  # Free API key, 1 SMS/day limit
        })
        result = response.json()
        if result.get('success'):
            st.success("🚨 SMS alert sent successfully!")
        else:
            st.warning(f"SMS failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to send SMS alert: {e}")

# --- Main UI ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.title("🛠️ Scaffolding Safety Monitoring System (Live Stream)")
    st.markdown("""
    Monitor scaffold **tilt**, **vibration**, **distance from ground**, and **sound levels** in real-time.
    Data updates every 5 seconds, categorized by risk level.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state = get_simulated_sensor_data()
status, emoji = evaluate_status(tilt)

with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader(f"System Status: {emoji} {status}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tilt Angle (°)", f"{tilt}°")
    col2.metric("Vibration Level", f"{vibration}")
    col3.metric("Distance from Ground (cm)", f"{distance}")
    col4.metric("Sound Level (dB)", f"{sound_level}")

    col5, col6 = st.columns(2)
    col5.metric("Bluetooth Status", "🟦 Connected" if bluetooth_signal else "❌ Disconnected")
    col6.metric("Buzzer", buzzer_state)
    st.markdown('</div>', unsafe_allow_html=True)

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

if status == "DANGER":
    send_sms_alert(tilt, vibration)

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
