# mqtt_client.py
import random
import ssl
import traceback
import json
import threading
import requests
import os
from datetime import datetime
from paho.mqtt import client as mqtt_client
from src.system_command import get_status


class MQTTClient:
    def __init__(self, broker, port, client_prefix=None, username=None, password=None,
                 use_ssl=False, ca_cert=None, log_file="mqtt_debug_log.txt", callback_url=None):
        # ✅ สร้างโฟลเดอร์ logs ในตำแหน่งที่มี write permission
        # ใช้ AppData ถ้าจำเป็น (เมื่อติดตั้ง)
        if "Program Files" in os.getcwd() or "Program Files (x86)" in os.getcwd():
            # ติดตั้งแล้ว - ใช้ AppData
            log_dir = os.path.join(os.getenv('APPDATA'), 'SpoShowIP', 'logs')
        else:
            # ยังเป็น dev environment - ใช้ logs ที่ repo
            log_dir = "logs"
        
        os.makedirs(log_dir, exist_ok=True)
        
        # ✅ ถ้าไม่ระบุ log_file ให้ใช้ default พร้อม timestamp
        if log_file == "mqtt_debug_log.txt":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"mqtt_debug_{timestamp}.txt")
        
        self.client_id = f'{client_prefix}-{random.randint(0, 1000)}'
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password or ""
        self.use_ssl = use_ssl
        self.ca_cert = ca_cert
        self.log_file = log_file
        self.callback_url = callback_url
        self.response_topic = f"/spo-client/{self.client_id}/response"
        self.command_topic = None  # Will be set via subscribe()

        # ✅ เปิดไฟล์ log แบบ append
        self.log(f"========== MQTT Client Debug Start ==========")
        self.log(f"Broker: {broker}:{port}, SSL: {use_ssl}")
        self.log(f"Client ID: {self.client_id}")
        self.log(
            f"Username (first 40 chars): {username[:40] if username else 'None'}")
        if callback_url:
            self.log(f"Callback URL: {callback_url}")

        # ✅ สร้าง client
        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)

        # ✅ ตั้ง callback
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        # self.client.on_log = self.on_log

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
            # Auto-subscribe ถ้ากำหนด topic ไว้
            if self.command_topic:
                self._do_subscribe()
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
                msg += " | Not authorized (JWT or EMQX rule error)"
            else:
                msg += " | Unknown error"
            self.log(msg)

    def on_disconnect(self, client, userdata, rc):
        self.log(f"💥 Disconnected from broker (rc={rc})")

    def on_message(self, client, userdata, msg):
        """Run message processing in separate thread to avoid blocking MQTT loop"""
        t = threading.Thread(target=self._handle_message, args=(msg,))
        t.daemon = True
        t.start()
    
    def _handle_message(self, msg):
        """Handle received message (runs in separate thread)"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            self.log(f"📥 Received message on `{topic}`: {payload}")
            
            # Parse JSON command
            try:
                data = json.loads(payload)
                command = data.get("command")
                
                if command == "get_status":
                    self.log("🔄 Executing: get_status")
                    result = get_status()
                    response = {"status": "success", "data": result}
                    self._send_response(response)
                else:
                    self.log(f"⚠️ Unknown command: {command}")
                    response = {"status": "error", "message": f"Unknown command: {command}"}
                    self._send_response(response)
            except json.JSONDecodeError:
                self.log(f"⚠️ Invalid JSON payload: {payload}")
                response = {"status": "error", "message": "Invalid JSON"}
                self._send_response(response)
        except Exception as e:
            self.log(f"❌ Error processing message: {e}")
            traceback.print_exc()
    
    def _send_response(self, response):
        """Send response via MQTT or HTTP callback"""
        if self.callback_url:
            self._send_via_http(response)
        else:
            self._send_via_mqtt(response)
    
    def _send_via_http(self, response):
        """Send response via HTTP POST to callback URL"""
        try:
            self.log(f"📤 Sending response via HTTP POST to {self.callback_url}")
            headers = {"Content-Type": "application/json"}
            r = requests.post(self.callback_url, json=response, headers=headers, timeout=10)
            if r.status_code == 200:
                self.log(f"✅ Response sent successfully (HTTP {r.status_code})")
            else:
                self.log(f"⚠️ Response sent but got HTTP {r.status_code}: {r.text}")
        except Exception as e:
            self.log(f"❌ Error sending HTTP response: {e}")
            traceback.print_exc()
    
    def _send_via_mqtt(self, response):
        """Send response via MQTT publish"""
        self.publish(self.response_topic, json.dumps(response))

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

    def subscribe(self, topic):
        """Subscribe to topic for receiving commands"""
        self.command_topic = topic
        self._do_subscribe()
    
    def _do_subscribe(self):
        """Internal method to perform subscription"""
        if not self.command_topic:
            return
        try:
            self.log(f"🔔 Subscribing to `{self.command_topic}`")
            result = self.client.subscribe(self.command_topic)
            if result[0] == 0:
                self.log(f"✅ Subscribed to `{self.command_topic}`")
            else:
                self.log(f"❌ Failed to subscribe to `{self.command_topic}` (rc={result[0]})")
        except Exception as e:
            self.log(f"⚠️ Error subscribing: {e}")
            traceback.print_exc()

    def publish(self, topic, message):
        try:
            self.log(f"📤 Publishing `{message}` to `{topic}`")
            result = self.client.publish(topic, message)
            status = result[0]
            if status == 0:
                # self.log(f"✅ Message sent successfully to `{topic}`")
                print(f"✅ Message sent successfully to `{topic}`")
            else:
                # self.log(f"❌ Failed to send message (status={status}) to `{topic}`")
                print(f"❌ Failed to send message (status={status}) to `{topic}`")
        except Exception as e:
            # self.log(f"⚠️ Error publishing: {e}")
            print(f"⚠️ Error publishing: {e}")
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
