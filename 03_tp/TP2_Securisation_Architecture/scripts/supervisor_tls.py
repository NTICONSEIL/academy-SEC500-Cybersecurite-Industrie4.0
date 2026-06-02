import ssl
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 8883

TOPIC = "factory/line1/#"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connexion MQTTs réussie")
    client.subscribe(TOPIC)

def on_message(client, userdata, message):
    print(
        f"[MESSAGE] {message.topic}"
        f" -> {message.payload.decode()}"
    )

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER_HOST,
    BROKER_PORT
)

client.loop_forever()