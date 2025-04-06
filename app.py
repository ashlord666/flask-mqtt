from flask import Flask, jsonify
import threading
import paho.mqtt.client as mqtt
import os
import time

app = Flask(__name__)

# Dictionary to store MQTT data with thread-safe access
mqtt_data = {}
data_lock = threading.Lock()

# MQTT configuration using environment variables
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = '#'  # Subscribe to all topics

# MQTT client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
    except UnicodeDecodeError:
        payload = str(msg.payload)
    with data_lock:
        mqtt_data[msg.topic] = payload

client.on_connect = on_connect
client.on_message = on_message

def mqtt_loop():
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            print(f"MQTT error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

@app.route('/', methods=['GET'])
def get_mqtt_data():
    with data_lock:
        return jsonify(mqtt_data)

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_PORT', 5000)))
