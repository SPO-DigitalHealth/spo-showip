## Papar Information
- Title:  `SPI ShowIP`
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
## License
```
pyinstaller --onefile --noconsole --name SpoShowIP --add-data "img/logo_MOPH.png;img" --add-data "config.json;." main.py
```

## License
- SPO MOPH


```
```
