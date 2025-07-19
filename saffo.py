import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_autorefresh import st_autorefresh

# --- Set up page config ---
st.set_page_config(page_title="Scaffolding Safety Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        background-color: #eaf6fb;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #014f86;
    }
    </style>
""", unsafe_allow_html=True)

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="data_refresh")

# --- Dashboard Title ---
st.title("🛠️ Scaffolding Safety Monitoring System (Live Stream)")
st.markdown("""
This live dashboard simulates monitoring of **scaffolding tilt**, **vibration**, **distance from ground**, and **sound levels** using an Arduino-based safety system.

Real-time data is updated every 5 seconds and categorized based on **risk thresholds**. Data is wirelessly transmitted using Bluetooth (HC-05) to this dashboard.
""")

# --- Simulated Sensor Data Function ---
def get_simulated_sensor_data():
    tilt = round(np.random.uniform(0, 15), 2)
    vibration = round(np.random.uniform(0, 2.5), 2)
    distance = round(np.random.uniform(50, 200), 2)
    sound_level = round(np.random.uniform(20, 100), 2)
    bluetooth_signal = True if np.random.rand() > 0.1 else False
    buzzer_state = "ON" if tilt > 10 or vibration > 2.0 else "OFF"
    return tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state

# --- Safety Status Evaluation ---
def evaluate_status(tilt):
    if tilt <= 5:
        return "SAFE", "🟢"
    elif tilt <= 10:
        return "WARNING", "🟠"
    else:
        return "DANGER", "🔴"

# --- Fetch Sensor Data ---
tilt, vibration, distance, sound_level, bluetooth_signal, buzzer_state = get_simulated_sensor_data()
status, emoji = evaluate_status(tilt)

# --- Display System Status ---
st.subheader(f"System Status: {emoji} {status}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tilt Angle (°)", f"{tilt}°")
col2.metric("Vibration Level", f"{vibration}")
col3.metric("Distance from Ground (cm)", f"{distance}")
col4.metric("Sound Level (dB)", f"{sound_level}")

col5, col6 = st.columns(2)
col5.metric("Bluetooth Status", "🟦 Connected" if bluetooth_signal else "❌ Disconnected")
col6.metric("Buzzer", buzzer_state)

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
st.plotly_chart(fig, use_container_width=True)

# --- Textbelt Alert on DANGER ---
if status == "DANGER":
    try:
        response = requests.post('https://textbelt.com/text', {
            'phone': '+250788886315',
            'message': f"⚠️ ALERT: Scaffolding is in DANGER!\nTilt: {tilt}°, Vibration: {vibration}. Immediate attention required!",
            'key': 'textbelt'  # 1 free SMS per day
        })

        result = response.json()
        if result['success']:
            st.success("🚨 Free SMS sent to Supervisor via Textbelt.")
        else:
            st.warning(f"SMS failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to send SMS alert: {e}")

# --- Project Overview Section ---
st.markdown("""
---
### 📘 Project Overview
The **Scaffolding Safety Monitoring System** is an embedded system built with Arduino components. It is designed to monitor real-time tilt, vibration, sound levels, and distance data on construction scaffolding to prevent hazards.

**Sensors and Modules Used:**
- MPU6050 (Accelerometer + Gyroscope)
- HC-SR04 Ultrasonic Sensor
- Microphone or Sound Sensor
- LEDs (Green, Yellow, Red)
- Active Buzzer (alerts during danger and high vibration)
- HC-05 Bluetooth Module (Wireless Transmission)

**Functionality:**
- 🟢 **SAFE**: Tilt ≤ 5° (Green LED ON)
- 🟠 **WARNING**: 5° < Tilt ≤ 10° (Yellow LED blinking + buzzer short beep)
- 🔴 **DANGER**: Tilt > 10° (Red LED blinking + continuous buzzer)
- **Vibration**: Triggers buzzer if above threshold
- **Ultrasonic Sensor**: Measures distance from ground (collapse risk)
- **Sound Sensor**: Detects abnormal sound levels on scaffolding
- **Bluetooth HC-05**: Sends all data wirelessly to this dashboard

⚠️ This dashboard simulates sensor values and is ready for integration with live serial data from Arduino.
""")
