# config.py
import json


def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return {}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}


config = load_config()  # โหลด config.json ทันทีที่ import
