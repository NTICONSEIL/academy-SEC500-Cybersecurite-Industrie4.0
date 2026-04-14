import os, time, random
import paho.mqtt.client as mqtt

broker = os.getenv("BROKER", "192.168.10.200")
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="capteur_01")
client.connect(broker, 1883, 60)
client.loop_start()

while True:
    temp = random.randint(480, 540)
    client.publish("usine/four1/temperature", str(temp))
    client.publish("usine/four1/status", "RUN")
    time.sleep(3)
