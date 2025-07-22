import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_autorefresh import st_autorefresh

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
        color: ;
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
    rotation_360 = round(np.random.uniform(0, 360), 1)
    bluetooth_signal = True if np.random.rand() > 0.1 else False
    buzzer_state = "ON" if tilt > 10 or vibration > 2.0 else "OFF"

    # New fields
    acceleration_x = round(np.random.uniform(-10, 10), 2)
    acceleration_y = round(np.random.uniform(-10, 10), 2)
    acceleration_z = round(np.random.uniform(-10, 10), 2)
    acceleration_total = round(np.sqrt(acceleration_x**2 + acceleration_y**2 + acceleration_z**2), 2)
    temperature = round(np.random.uniform(20, 50), 1)  # degrees Celsius

    return (tilt, vibration, distance, sound_level, rotation_360, bluetooth_signal, buzzer_state,
            acceleration_x, acceleration_y, acceleration_z, acceleration_total, temperature)

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
            st.success(" SMS alert sent successfully!")
        else:
            st.warning(f"SMS failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to send SMS alert: {e}")

# --- Title ---
st.markdown('<div class="bordered-card"><div class="bordered-card-inner">', unsafe_allow_html=True)
st.title(" Scaffolding Safety Monitoring System (Live Stream)")
st.markdown('</div></div>', unsafe_allow_html=True)

# --- Description ---
st.markdown('<div class="bordered-card"><div class="bordered-card-inner">', unsafe_allow_html=True)
st.markdown("Monitor scaffold **tilt**, **vibration**, **distance from ground**, **sound levels**, **rotation angle**, **acceleration** and **temperature** in real-time. Data updates every 5 seconds, categorized by risk level.")
st.markdown('</div></div>', unsafe_allow_html=True)

# --- Sensor Data ---
(tilt, vibration, distance, sound_level, rotation_360, bluetooth_signal, buzzer_state,
 acceleration_x, acceleration_y, acceleration_z, acceleration_total, temperature) = get_simulated_sensor_data()

status, emoji = evaluate_status(tilt)

# --- Metrics ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader(f"System Status: {emoji} {status}")

# -------------------- Bluetooth Status --------------------
col5, col6 = st.columns(2)
with col5:
    st.subheader(" Bluetooth Status")
    if bluetooth_signal:
        st.success("Connected ")
    else:
        st.error("Disconnected ")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"""
    <div class="custom-metric">
        <h4>Tilt Angle (°)</h4><p>{tilt}°</p>
    </div>""", unsafe_allow_html=True)
col2.markdown(f"""
    <div class="custom-metric">
        <h4>Vibration Level</h4><p>{vibration}</p>
    </div>""", unsafe_allow_html=True)
col3.markdown(f"""
    <div class="custom-metric">
        <h4>Distance from Ground (cm)</h4><p>{distance}</p>
    </div>""", unsafe_allow_html=True)
col4.markdown(f"""
    <div class="custom-metric">
        <h4>Sound Level (dB)</h4><p>{sound_level}</p>
    </div>""", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
col5.markdown(f"""
    <div class="custom-metric">
        <h4>Rotation Angle (°)</h4><p>{rotation_360}°</p>
    </div>""", unsafe_allow_html=True)
col6.markdown(f"""
    <div class="custom-metric">
        <h4>Buzzer</h4><p>{buzzer_state}</p>
    </div>""", unsafe_allow_html=True)
col7.markdown(f"""
    <div class="custom-metric">
        <h4>Acceleration X (m/s²)</h4><p>{acceleration_x}</p>
    </div>""", unsafe_allow_html=True)
col8.markdown(f"""
    <div class="custom-metric">
        <h4>Acceleration Y (m/s²)</h4><p>{acceleration_y}</p>
    </div>""", unsafe_allow_html=True)

col9, col10, col11, col12 = st.columns(4)
col9.markdown(f"""
    <div class="custom-metric">
        <h4>Acceleration Z (m/s²)</h4><p>{acceleration_z}</p>
    </div>""", unsafe_allow_html=True)
col10.markdown(f"""
    <div class="custom-metric">
        <h4>Total Acceleration (m/s²)</h4><p>{acceleration_total}</p>
    </div>""", unsafe_allow_html=True)
col11.markdown(f"""
    <div class="custom-metric">
        <h4>Temperature (°C)</h4><p>{temperature}°C</p>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Tilt Gauge Chart ---
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
st.markdown('<div class="section">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Trigger Alert ---
if status == "DANGER":
    send_sms_alert(tilt, vibration)

