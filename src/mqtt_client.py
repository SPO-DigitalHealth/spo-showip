# mqtt_client.py
import random
import ssl
import traceback
from datetime import datetime
from paho.mqtt import client as mqtt_client


class MQTTClient:
    def __init__(self, broker, port, client_prefix=None, username=None, password=None,
                 use_ssl=False, ca_cert=None, log_file="mqtt_debug_log.txt"):
        self.client_id = f'{client_prefix}-{random.randint(0, 1000)}'
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password or ""
        self.use_ssl = use_ssl
        self.ca_cert = ca_cert
        self.log_file = log_file

        # ✅ เปิดไฟล์ log แบบ append
        self.log(f"========== MQTT Client Debug Start ==========")
        self.log(f"Broker: {broker}:{port}, SSL: {use_ssl}")
        self.log(f"Client ID: {self.client_id}")
        self.log(
            f"Username (first 40 chars): {username[:40] if username else 'None'}")

        # ✅ สร้าง client
        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)

        # ✅ ตั้ง callback
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log

        # ✅ ถ้าใช้ SSL
        if self.use_ssl:
            try:
                self.log(f"🔐 Setting up SSL/TLS with CA: {self.ca_cert}")
                self.client.tls_set(ca_certs=self.ca_cert,
                                    cert_reqs=ssl.CERT_REQUIRED)
                self.client.tls_insecure_set(True)
            except Exception as e:
                self.log(f"⚠️ SSL setup error: {e}")

    def log(self, message: str):
        """บันทึก log ทั้ง console และไฟล์"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

    # ========= CALLBACK ==========
    def on_connect(self, client, userdata, flags, rc):
        self.log(f"📡 [on_connect] rc={rc}")
        if rc == 0:
            self.log(f"✅ Connected successfully to {self.broker}:{self.port}")
        else:
            msg = f"❌ Failed to connect (rc={rc})"
            if rc == 1:
                msg += " | Incorrect protocol version"
            elif rc == 2:
                msg += " | Invalid client ID"
            elif rc == 3:
                msg += " | Server unavailable"
            elif rc == 4:
                msg += " | Bad username or password"
            elif rc == 5:
                msg += " | Not authorized (JWT หรือ EMQX rule ผิด)"
            else:
                msg += " | Unknown error"
            self.log(msg)

    def on_disconnect(self, client, userdata, rc):
        self.log(f"💥 Disconnected from broker (rc={rc})")

    def on_log(self, client, userdata, level, buf):
        self.log(f"🧾 [LOG] {buf}")

    # ========= ACTION ==========
    def connect(self):
        try:
            self.log(
                f"🚀 Connecting to {self.broker}:{self.port} (SSL={self.use_ssl}) ...")
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            self.log(f"❌ Exception while connecting: {e}")
            traceback.print_exc()
            with open(self.log_file, "a", encoding="utf-8") as f:
                traceback.print_exc(file=f)

    def publish(self, topic, message):
        try:
            self.log(f"📤 Publishing `{message}` to `{topic}`")
            result = self.client.publish(topic, message)
            status = result[0]
            if status == 0:
                self.log(f"✅ Message sent successfully to `{topic}`")
            else:
                self.log(
                    f"❌ Failed to send message (status={status}) to `{topic}`")
        except Exception as e:
            self.log(f"⚠️ Error publishing: {e}")
            traceback.print_exc()
            with open(self.log_file, "a", encoding="utf-8") as f:
                traceback.print_exc(file=f)

    def disconnect(self):
        self.log("🛑 Disconnecting...")
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.log("✅ Disconnected cleanly.")
        except Exception as e:
            self.log(f"⚠️ Disconnect error: {e}")
