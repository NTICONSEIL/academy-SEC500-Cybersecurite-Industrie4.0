import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "factory/line1/#"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connexion MQTT - code : {reason_code}")
    client.subscribe(TOPIC)
    print(f"Abonnement au topic : {TOPIC}")

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"[MESSAGE] {message.topic} -> {payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Démarrage de la supervision MQTT...")
print("Tentative de connexion au broker...")

client.connect(BROKER_HOST, BROKER_PORT, 60)

print("Connexion TCP établie, attente MQTT...")
client.loop_forever()