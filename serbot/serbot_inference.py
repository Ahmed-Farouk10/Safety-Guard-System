import cv2
from ultralytics import YOLO
import paho.mqtt.client as mqtt
import os
import RPi.GPIO as GPIO
import time

# Obstacle Avoidance Setup
TRIG_PIN = 17
ECHO_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()
    return (end_time - start_time) * 17150

# MQTT Setup
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
username = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")
ca_cert = os.getenv("MQTT_CA_CERT")  # Path to CA certificate



client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker, port)
client.tls_set(ca_certs=ca_cert, tls_version=ssl.PROTOCOL_TLSv1_2)  # Enable TLS
client.connect(broker, port) #remove if unnecessary
# Load YOLOv8s
model = YOLO("yolov8s.pt")

# Camera Setup
cap = cv2.VideoCapture(0)

while True:
    # Obstacle Detection
    distance = get_distance()
    if distance < 20:
        print("🛑 Obstacle detected! Stopping...")
        continue  # Replace with actual movement control logic

    # Person Detection
    ret, frame = cap.read()
    results = model(frame)
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)
            if model.names[cls] == "person":
                print("⚠️ Person detected without PPE")
                client.publish("alerts/person", "Person detected without PPE")