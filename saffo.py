import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# --- Simulate Live Sensor Data Stream ---
st.set_page_config(page_title="Scaffolding Safety Live Dashboard", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    body {
        background-color: #e8f4fd;
    }
    .main {
        background-color: #f0f8ff;
        padding: 2rem;
        border-radius: 12px;
    }
    h1, h2, h3 {
        color: #02457a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Streamlit App Title & Description ---
st.title("🔧 Scaffolding Safety Monitoring System (Live)")
st.markdown("""
This live dashboard monitors **scaffolding tilt, vibration**, and **distance from ground** using an Arduino-based safety system.
Real-time data is streamed and safety thresholds trigger **visual and audible alerts**.
""")

# --- Function to Simulate Sensor Data ---
def simulate_data():
    tilt = round(np.random.uniform(0, 15), 2)
    vibration = round(np.random.uniform(0, 2.5), 2)
    distance = round(np.random.uniform(30, 200), 2)
    return tilt, vibration, distance

# --- Function to Evaluate System State ---
def get_status(tilt):
    if tilt <= 5:
        return "SAFE", "🟢"
    elif 5 < tilt <= 10:
        return "WARNING", "🟠"
    else:
        return "DANGER", "🔴"

# --- Real-time Update Loop ---
frame = st.empty()
while True:
    with frame.container():
        tilt, vibration, distance = simulate_data()
        status, emoji = get_status(tilt)

        st.subheader(f"System Status: {emoji} **{status}**")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tilt Angle (°)", f"{tilt}°")
        col2.metric("Vibration Level", f"{vibration}")
        col3.metric("Distance from Ground (cm)", f"{distance}")

        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = tilt,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Tilt Angle Gauge"},
            delta = {'reference': 5},
            gauge = {
                'axis': {'range': [None, 15]},
                'steps' : [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 10], 'color': "orange"},
                    {'range': [10, 15], 'color': "red"}
                ],
                'threshold' : {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10}
            }))

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        ---
        #### 📘 Project Description
        This system enhances construction safety by monitoring:
        - **Tilt angle** using MPU6050 sensor
        - **Vibration levels** from motion
        - **Distance from collapse risk** using ultrasonic sensor
        - **LEDs & Buzzer** provide immediate alerts
        - **Bluetooth module** enables wireless alerts

        Alerts:
        - 🟢 Green: Safe
        - 🟠 Yellow: Warning (tilt > 5°)
        - 🔴 Red: Danger (tilt > 10°)

        ⚠️ Dashboard refreshes live with simulated sensor values.
        """)

    time.sleep(3)
