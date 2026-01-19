# config.py
import json
import socket
import urllib.request

from src.system_info import get_system_info


def fetch_config_from_api(url):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("data", data)
    except Exception as e:
        print("Error fetching config from API:", e)
        return {}


def load_config(file_path="config.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            base_config = json.load(file)
    except Exception:
        base_config = {}

    window_width = base_config.get("window_width")
    api_url = base_config.get("api_url")

    # ดึงและผสานค่าจาก API ส่ง client name(เช่น ชื่อเครื่อง)
    hostname = socket.gethostname()
    api_cfg = fetch_config_from_api(
        f"{api_url}/api/config/mqtt?client={hostname}")
    base_config.update(api_cfg)
    # response api_cfg
    # print(api_cfg)
    # ไม่ให้ค่า API ทับ window_width จากไฟล์
    if window_width is not None:
        base_config["window_width"] = window_width

    return base_config


# โหลดคอนฟิกทันทีเมื่อ import
config = load_config()
