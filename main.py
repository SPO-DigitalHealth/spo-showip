# main.py
import json
import tkinter as tk
from src.mqtt_client import MQTTClient
from src.gui import ShowIPApp
from tkinter import messagebox
import src.config as config  # Import global config


if __name__ == "__main__":
    # ดึงข้อมูลจาก config.py
    use_mqtt = config.config.get('use_mqtt', True)  # ค่า default คือ True
    mqtt_host = config.config.get('mqtt_host', 'localhost')
    mqtt_port = config.config.get('mqtt_port', 1883)
    mqtt_user = config.config.get('mqtt_user', '')
    mqtt_pass = config.config.get('mqtt_pass', '')
    client_prefix = config.config.get('mqtt_client_prefix', 'client_')
    topic_prefix = config.config.get(
        'mqtt_topic_prefix', '/spo-client/windown/online')
    update_interval_sec = config.config.get('mqtt_update_interval_sec', 2000)

    # สร้าง instance ของ MQTTClient
    mqtt_client = MQTTClient(mqtt_host, mqtt_port,
                             client_prefix, mqtt_user, mqtt_pass)

    # เริ่ม GUI
    app = tk.Tk()
    show_ip_app = ShowIPApp(
        app, mqtt_client, topic_prefix, update_interval_sec)

    # เชื่อมต่อกับ MQTT Broker
    try:
        mqtt_client.connect()
        show_ip_app.update_status("Connected to MQTT", "green")
    except Exception as e:
        # print(f"Failed to connect to MQTT Broker: {str(e)}")
        # อัปเดต GUI เพื่อแสดงสถานะ
        show_ip_app.update_status(f"MQTT connection failed", "red")
        if use_mqtt:
            messagebox.showerror("MQTT connection failed", str(e))

    def on_closing():
        mqtt_client.disconnect()  # ตัดการเชื่อมต่อ MQTT
        app.destroy()  # ปิดแอปพลิเคชัน

    # เมื่อปิดหน้าต่างให้เรียกฟังก์ชัน on_closing
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
