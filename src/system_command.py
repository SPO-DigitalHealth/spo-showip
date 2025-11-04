# src/system_command.py
import psutil
import platform
import subprocess
import os
import base64
import json
import io
from PIL import ImageGrab  # สำหรับ screenshot


def get_status():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "os": platform.system(),
        "release": platform.release(),
        "hostname": platform.node(),
    }


def get_process_list(limit=10):
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except Exception:
            pass
    return sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:limit]


def execute_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        return {"output": output.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}


def screenshot():
    try:
        img = ImageGrab.grab()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return {"image_base64": b64}
    except Exception as e:
        return {"error": str(e)}


def list_files(path="."):
    try:
        files = os.listdir(path)
        return {"path": path, "files": files}
    except Exception as e:
        return {"error": str(e)}


def delete_file(path):
    try:
        os.remove(path)
        return {"deleted": path}
    except Exception as e:
        return {"error": str(e)}


def open_app(path):
    try:
        subprocess.Popen(path, shell=True)
        return {"opened": path}
    except Exception as e:
        return {"error": str(e)}


def shutdown():
    os.system("shutdown /s /t 1" if platform.system()
              == "Windows" else "shutdown now")
    return {"status": "shutting down"}


def reboot():
    os.system("shutdown /r /t 1" if platform.system()
              == "Windows" else "reboot")
    return {"status": "rebooting"}


def run_custom_script(code):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return {"result": exec_globals}
    except Exception as e:
        return {"error": str(e)}
