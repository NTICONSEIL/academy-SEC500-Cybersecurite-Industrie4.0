import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/line1/machineA/telemetry"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER_HOST, BROKER_PORT)

print("Capteur IIoT démarré. Publication MQTT non sécurisée.")

while True:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "machine": "machineA",
        "temperature": round(random.uniform(55, 85), 2),
        "vibration": round(random.uniform(0.2, 1.8), 2),
        "status": random.choice(["OK", "OK", "OK", "WARNING"])
    }

    client.publish(TOPIC, json.dumps(payload))
    print(f"Message publié : {payload}")
    time.sleep(2)