import streamlit as st
import paho.mqtt.client as mqtt
import requests

# MQTT Setup
broker = st.secrets["MQTT_BROKER"]
port = st.secrets["MQTT_PORT"]
username = st.secrets["MQTT_USER"]
password = st.secrets["MQTT_PASSWORD"]

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port)

st.title("Safety Guard Dashboard")
alert_placeholder = st.empty()

def on_message(client, userdata, msg):
    if msg.topic == "alerts/person":
        alert_placeholder.warning(f"🚨 Alert: {msg.payload.decode()}")

client.subscribe("alerts/#")
client.on_message = on_message
client.loop_start()

# Fetch logs from Flask API
response = requests.get("https://your-flask-app.onrender.com/alerts") 
if response.status_code == 200:
    logs = response.json()
    st.subheader("Alert History")
    for log in logs:
        st.write(f"{log['timestamp']}: {log['message']}")