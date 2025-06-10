import streamlit as st
import paho.mqtt.client as mqtt
import requests
import time
from dotenv import load_dotenv
import os
import ssl
import threading

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Safety Guard Dashboard", layout="wide")

# Shared list for alerts
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

alerts = st.session_state.alerts

def on_message(client, userdata, msg):
    alerts.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {msg.payload.decode()}")

def mqtt_thread():
    client = mqtt.Client()
    client.username_pw_set("nzurqfdn:nzurqfdn", "N4XQP7hZTkrIzaSJrnfTE7mfSsjkCk_j")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    client.on_message = on_message
    client.connect("rabbit.lmq.cloudamqp.com", 8883, 60)
    client.subscribe("alerts/#")
    client.loop_forever()

if 'mqtt_started' not in st.session_state:
    threading.Thread(target=mqtt_thread, daemon=True).start()
    st.session_state.mqtt_started = True

st.title("Safety Guard Dashboard")

# Display current alerts
st.subheader("Recent Alerts")
for alert in reversed(alerts[-10:]):
    st.warning(f"🚨 {alert}")

# Add a refresh button
if st.button("Refresh"):
    st.experimental_rerun()

# Fetch logs from Flask API
try:
    flask_api_url = os.getenv("FLASK_API_URL", "http://localhost:5000")
    if not flask_api_url.startswith(('http://', 'https://')):
        flask_api_url = f"https://{flask_api_url}"
    
    response = requests.get(f"{flask_api_url}/alerts")
    if response.status_code == 200:
        logs = response.json()
        st.subheader("Alert History")
        for log in logs:
            st.write(f"{log['timestamp']}: {log['message']}")
except Exception as e:
    st.error(f"Could not fetch alert history: {str(e)}")