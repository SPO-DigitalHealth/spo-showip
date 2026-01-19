# src/system_command.py
import psutil
import platform
import os
import pathlib
import subprocess
import json
import shutil
from datetime import datetime


def get_status():
    """Get system status information"""
    try:
        result = {
            "timestamp": datetime.now().isoformat(),
            "hostname": platform.node(),
            "os": platform.system(),
            "release": platform.release(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
        }
        
        try:
            cwd = os.path.abspath(os.getcwd())
            disk_info = shutil.disk_usage(cwd)
            disk_percent = (disk_info.used / disk_info.total) * 100
            result["disk_percent"] = round(disk_percent, 2)
        except Exception:
            result["disk_percent"] = None
        
        return result
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


def get_process_list(limit=10):
    """ดึงรายชื่อโปรเซสที่ใช้ CPU สูงสุด"""
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(p.info)
        except Exception:
            pass
    processes = sorted(processes, key=lambda x: x.get(
        'cpu_percent', 0), reverse=True)
    return processes[:limit]


def list_files(path='.'):
    """แสดงรายชื่อไฟล์ในโฟลเดอร์ (safe mode)"""
    try:
        p = pathlib.Path(path)
        if not p.exists():
            return {"error": "path not found", "path": path}

        files = []
        for item in p.iterdir():
            try:
                files.append({
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            except Exception:
                pass
        return {"path": str(p.resolve()), "files": files}
    except Exception as e:
        return {"error": str(e)}


def safe_exec(cmd: str):
    """รันคำสั่งจาก whitelist เท่านั้น"""
    WHITELIST = {
        "whoami": "whoami",
        "ipconfig": "ipconfig" if os.name == "nt" else "ifconfig",
        "hostname": "hostname",
        "uptime": "uptime"
    }

    if cmd not in WHITELIST:
        return {"error": f"Command '{cmd}' not allowed"}

    try:
        output = subprocess.check_output(
            WHITELIST[cmd], shell=True, text=True, stderr=subprocess.STDOUT)
        return {"command": cmd, "output": output.strip()}
    except Exception as e:
        return {"error": str(e)}


def download_only(url: str):
    """ดาวน์โหลดไฟล์จาก URL (ไม่ติดตั้ง / ไม่ execute)"""
    import tempfile
    import requests
    try:
        tmp_path = tempfile.gettempdir()
        filename = os.path.basename(url.split("?")[0])
        dest = os.path.join(tmp_path, filename)
        r = requests.get(url, timeout=15, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return {"downloaded": dest}
    except Exception as e:
        return {"error": str(e)}
