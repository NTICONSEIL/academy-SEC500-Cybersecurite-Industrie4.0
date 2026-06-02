import ssl
import paho.mqtt.client as mqtt

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.connect("localhost", 8883)

client.subscribe("#")

client.loop_forever()