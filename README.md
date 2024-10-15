## Demo
<div style="display: flex; align-items: top;">
    <div>
        <center><b>ใช้ MQTT</b></center>
        <img src="screen1.png" alt="รูปตัวอย่าง ใช้ MQTT" width="auto">
    </div>
    <div style="border-left: 1px solid black; margin: 0 20px;"></div>
    <div>
        <center><b>ไม่ใช้ MQTT</b></center>
        <img src="screen2.png" alt="รูปตัวอย่าง ไม่ใช้ MQTT" width="auto">
    </div>
</div>

## การใช้งาน .exe
- เข้าไปใน /dist
- กำหนด ค่า `config.json` และเปิดใช้ `SpoShowIP.exe`

## Papar Information
- Title:  `SpoShowIP`
- Authors:  `SPO DEV`

## Install & Dependence
- python
- tkinter
- paho.mqtt

## Directory Hierarchy
```
|—— config.json
|—— dist
|    |—— config.json
|    |—— img
|        |—— cybersecurit.jpg
|        |—— ddigital.gif
|        |—— glass_card.png
|        |—— glass_card_mini.png
|        |—— logo_MOPH.png
|    |—— SpoShowIP.exe
|—— img
|    |—— cybersecurit.jpg
|    |—— ddigital.gif
|    |—— glass_card.png
|    |—— glass_card_mini.png
|    |—— logo_MOPH.png
|—— main.py
|—— SpoShowIP.spec
|—— src
|    |—— config.py
|    |—— gui.py
|    |—— mqtt_client.py
|    |—— system_info.py
|    |—— __init__.py
```
## Build .exe
```
pyinstaller --onefile --noconsole --name SpoShowIP --add-data "img/logo_MOPH.png;img" --add-data "config.json;." main.py
```

## License
```
[FREE] SPO-MOPH
```
