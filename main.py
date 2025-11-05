# main.py
import tkinter as tk
import time
import threading
from tkinter import messagebox
from src.mqtt_client import MQTTClient
from src.gui import ShowIPApp
from src.config import fetch_config_from_api
import socket

# ------------------------
# ฟังก์ชันหลัก
# ------------------------


def run_agent():
    hostname = socket.gethostname()
    api_url = "http://127.0.0.1:8000"  # ✅ เปลี่ยนเป็น URL Laravel Center ของคุณ
    api_config_url = f"{api_url}/api/config/mqtt?client={hostname}"

    cfg = fetch_config_from_api(api_config_url)
    print("🔧 Loaded initial config:", cfg)

    mqtt_client = None
    app = tk.Tk()
    show_ip_app = ShowIPApp(app, None, "", 2000)

    def connect_mqtt():
        nonlocal mqtt_client
        mqtt_host = cfg.get("mqtt_host")
        mqtt_port = cfg.get("mqtt_port", 1883)
        mqtt_user = cfg.get("mqtt_user", "")
        mqtt_pass = cfg.get("mqtt_pass", "")
        client_prefix = cfg.get("mqtt_client_prefix", "spo_client_")
        topic_prefix = cfg.get("mqtt_topic_prefix",
                               "/spo-client/windown/online")
        update_interval_sec = cfg.get("mqtt_update_interval_sec", 2000)

        mqtt_client = MQTTClient(mqtt_host, mqtt_port,
                                 client_prefix, mqtt_user, mqtt_pass)
        show_ip_app.mqtt_client = mqtt_client
        show_ip_app.topic_prefix = topic_prefix
        show_ip_app.update_interval_sec = update_interval_sec

        try:
            mqtt_client.connect()
            show_ip_app.update_status("Connected to MQTT", "green")
        except Exception as e:
            show_ip_app.update_status("MQTT connection failed", "red")
            messagebox.showerror("MQTT connection failed", str(e))

    def refresh_config_loop():
        """ตรวจสอบ config ใหม่จาก API ทุก 1 นาที"""
        nonlocal cfg, mqtt_client
        while True:
            try:
                new_cfg = fetch_config_from_api(api_config_url)
                if not new_cfg:
                    print("⚠️ ไม่สามารถดึง config ใหม่จาก API ได้")
                    time.sleep(60)
                    continue

                new_use_mqtt = new_cfg.get("use_mqtt", False)
                old_use_mqtt = cfg.get("use_mqtt", False)

                # ถ้า config เปลี่ยน -> อัปเดตค่าทั้งหมด
                cfg = new_cfg

                if new_use_mqtt and not old_use_mqtt:
                    print("✅ use_mqtt เปลี่ยนจาก False → True: เชื่อมต่อ MQTT")
                    connect_mqtt()
                elif not new_use_mqtt and old_use_mqtt and mqtt_client:
                    print("🛑 use_mqtt เปลี่ยนจาก True → False: ตัดการเชื่อมต่อ MQTT")
                    mqtt_client.disconnect()
                    mqtt_client = None
                    show_ip_app.update_status(
                        "MQTT disabled by server", "orange")

            except Exception as e:
                print(f"⚠️ เกิดข้อผิดพลาดในการตรวจสอบ config: {e}")

            time.sleep(60)

    # เริ่มทำงานตามค่า config เริ่มต้น
    if cfg.get("use_mqtt", False):
        connect_mqtt()
    else:
        show_ip_app.update_status("Waiting for MQTT enable...", "orange")

    # สร้าง thread สำหรับอัปเดต config ทุก 1 นาที
    t = threading.Thread(target=refresh_config_loop, daemon=True)
    t.start()

    def on_closing():
        if mqtt_client:
            mqtt_client.disconnect()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    run_agent()
