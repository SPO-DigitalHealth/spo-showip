# mqtt_client.py
import random
from paho.mqtt import client as mqtt_client


class MQTTClient:
    def __init__(self, broker, port, client_prefix=None, username=None, password=None):
        client_id = f'{client_prefix}-{random.randint(0, 1000)}'
        self.broker = broker
        self.port = port
        self.client = mqtt_client.Client(client_id)

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, topic, message):
        # ส่งข้อความไปที่ topic
        try:
            result = self.client.publish(topic, message)
            status = result[0]
            if status == 0:
                print(f"Sent `{message}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic `{topic}`")
        except Exception as e:
            print(f"Error publishing message: {str(e)}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
