import streamlit as st
import requests
import random
import datetime

# --- Streamlit page setup ---
st.set_page_config(page_title="Scaffold Safety Monitor", layout="centered")
st.title("🏗️ Scaffolding Safety Monitoring System")

# --- Simulate sensor readings ---
tilt = round(random.uniform(0, 15), 2)  # degrees
vibration = round(random.uniform(0, 20), 2)  # arbitrary unit

# --- Determine safety status ---
if tilt > 10 or vibration > 15:
    status = "DANGER"
    status_color = "🔴"
elif tilt > 5 or vibration > 10:
    status = "WARNING"
    status_color = "🟠"
else:
    status = "SAFE"
    status_color = "🟢"

# --- Display sensor readings ---
st.subheader("📡 Live Sensor Data")
col1, col2 = st.columns(2)
col1.metric("Tilt (°)", tilt)
col2.metric("Vibration", vibration)

# --- Show Safety Status ---
st.subheader("📊 Safety Assessment")
st.markdown(f"**Status:** {status_color} {status}")
st.markdown(f"🕒 Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Send SMS alert via Textbelt if in danger ---
if status == "DANGER":
    st.warning("⚠️ Danger detected! Sending alert SMS...")

    try:
        response = requests.post('https://textbelt.com/text', {
            'phone': '+250788886315',  # Replace with supervisor's phone number
            'message': f"🚨 ALERT: Scaffold in DANGER!\nTilt: {tilt}°, Vibration: {vibration}.\nCheck immediately!",
            'key': 'textbelt'  # Free version allows 1 SMS/day
        })

        result = response.json()
        if result.get("success"):
            st.success("✅ SMS sent successfully to supervisor!")
        else:
            st.error(f"❌ Failed to send SMS: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"💥 Error sending SMS: {e}")
else:
    st.info("✅ No danger detected. System normal.")

# --- Optional: Show raw sensor data (for developers) ---
with st.expander("🔍 View Raw Sensor Readings"):
    st.json({
        "timestamp": datetime.datetime.now().isoformat(),
        "tilt": tilt,
        "vibration": vibration,
        "status": status
    })

# --- Footer ---
st.markdown("---")
st.markdown("📱 SMS alerts powered by [Textbelt](https://textbelt.com) • Built by Yvette 🚀")
