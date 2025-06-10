import paho.mqtt.client as mqtt
import time
from dotenv import load_dotenv
import os
import ssl

# Load environment variables
load_dotenv()

# MQTT Configuration
broker = "rabbit.lmq.cloudamqp.com"
port = 8883  # Using TLS port
username = "nzurqfdn:nzurqfdn"
password = "N4XQP7hZTkrIzaSJrnfTE7mfSsjkCk_j"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully!")

# Create MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)

# Set SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_publish = on_publish

# Connect to broker
print(f"Connecting to {broker}:{port}")
try:
    client.connect(broker, port, 60)  # 60 second timeout
    client.loop_start()

    # Test message
    test_message = "Test alert: Person detected!"
    topic = "alerts/person"

    # Publish test message
    print(f"Publishing message to {topic}: {test_message}")
    client.publish(topic, test_message)
    time.sleep(2)  # Wait for message to be published
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    client.loop_stop()
    client.disconnect() 