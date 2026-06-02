import ssl
import json
import random
import time

from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 8883

TOPIC = "factory/line1/machineA/telemetry"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.connect(
    BROKER_HOST,
    BROKER_PORT
)

while True:

    payload = {

        "timestamp":
        datetime.now().isoformat(),

        "machine":
        "machineA",

        "temperature":
        round(random.uniform(50,80),2),

        "vibration":
        round(random.uniform(0.2,2.0),2),

        "status":
        "OK"
    }

    client.publish(
        TOPIC,
        json.dumps(payload)
    )

    print("Publication :", payload)

    time.sleep(2)