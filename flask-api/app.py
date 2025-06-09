from flask import Flask, request
import paho.mqtt.client as mqtt
import sqlite3
import os

app = Flask(__name__)

# MQTT Setup
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
username = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(broker, port)

# SQLite Setup
def init_db():
    conn = sqlite3.connect("alerts.db")
    conn.execute("CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()

@app.route("/alert", methods=["POST"])
def receive_alert():
    alert_data = request.json
    conn = sqlite3.connect("alerts.db")
    conn.execute("INSERT INTO alerts (message) VALUES (?)", (alert_data["message"],))
    conn.commit()
    return "Alert logged", 200

if __name__ == "__main__":
    init_db()
    app.run()