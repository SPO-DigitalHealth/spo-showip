import tkinter as tk
from PIL import Image, ImageTk
import src.config as config
from src.system_info import get_system_info
import json


class ShowIPApp:
    def __init__(self, app, mqtt_client, topic, update_interval_sec):
        self.window_width = config.config.get('window_width', 300)
        self.use_mqtt = config.config.get('use_mqtt', False)
        self.tel_label = config.config.get('tel_label', "โทรภายใน : 101")
        self.developer_info_label = config.config.get(
            'developer_info_label', "โทรภายใน : 101")

        self.app = app
        self.mqtt_client = mqtt_client
        self.topic_prefix = topic
        self.update_interval_sec = update_interval_sec
        self.setup_gui()

    def setup_gui(self):
        self.app.title("SPO ShowIP")
        self.app.overrideredirect(True)
        self.app.attributes('-topmost', False)

        window_width = self.window_width
        window_height = 140 if self.use_mqtt else 120
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        taskbar_height = 48
        x_position = screen_width - window_width
        y_position = screen_height - window_height - taskbar_height
        self.app.geometry(f"{window_width}x{
                          window_height}+{x_position}+{y_position}")

        # สร้าง layout
        main_frame = tk.Frame(self.app)
        main_frame.place(relwidth=1, relheight=1)

        # โหลดโลโก้
        logo_frame = tk.Frame(main_frame)
        logo_frame.pack(side=tk.LEFT, padx=(5, 5))

        logo_path = "img/logo_MOPH.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((90, 90), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(logo_frame, image=logo_photo, bd=0)
        logo_label.image = logo_photo
        logo_label.pack()

        # ข้อความ
        text_frame = tk.Frame(main_frame)
        text_frame.pack(side=tk.LEFT)

        self.hostname_label = tk.Label(
            text_frame, text="", font=("Arial", 12), bd=0)
        self.hostname_label.pack(anchor="w", pady=(5, 0))

        self.ip_label = tk.Label(text_frame, font=("Arial", 18, "bold"), bd=0)
        self.ip_label.pack(anchor="w")

        if self.use_mqtt:
            self.status_label = tk.Label(
                text_frame, text="", font=("Arial", 8), bd=0)
            self.status_label.pack(anchor="w", pady=(2, 0))

        developer_tel_label = tk.Label(
            text_frame, text=self.tel_label, font=("Arial", 14, "bold"), bd=0)
        developer_tel_label.pack(anchor="w", pady=(2, 0))

        developer_info_label = tk.Label(
            text_frame, text=self.developer_info_label, font=("Arial", 12), bd=0)
        developer_info_label.pack(anchor="w", pady=0)

        self.update_info()

    def update_info(self):
        hostname, ip_address = get_system_info()

        self.hostname_label.config(text=f"Name : {hostname}")
        if ip_address:
            self.ip_label.config(text=f"IP : {ip_address}", fg="green")
            if self.use_mqtt:
                self.send_mqtt(hostname, ip_address)  # ส่งข้อมูล MQTT
        else:
            self.ip_label.config(text="IP : Disconnect", fg="red")

        # ตั้งเวลาให้ทำงานทุก x วินาที
        self.app.after(self.update_interval_sec, self.update_info)

    def send_mqtt(self, hostname, ip_address):
        payload = json.dumps({"hostname": hostname, "ip": ip_address})
        # print(self.use_mqtt)
        # try:
        topic = self.topic_prefix
        self.mqtt_client.publish(topic, payload)  # ส่ง payload ไปที่ MQTT
        # except Exception as e:
        #     self.status_label.config(
        #         text=f"MQTT Error: {str(e)}", fg="red")

    def update_status(self, message, color="black"):
        if self.use_mqtt:
            self.status_label.config(text=message, fg=color)
