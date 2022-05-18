import requests

import ctypes
import time
import json
import os

ids = {
    "thunderstorm": (200, 201, 202, 210, 211, 212, 221, 230, 231, 232),
    "drizzle": (300, 301, 302, 310, 311, 312, 313, 314, 321),
    "rain": (500, 501, 502, 503, 504, 511, 520, 521, 522, 531),
    "snow": (600, 601, 602, 611, 612, 615, 616, 620, 621, 622),
    "atmosphere": (701, 711, 721, 731, 741, 751, 761, 762, 771, 781),
    "clear": (800, 801, 802),
    "clouds": (803, 804, )
}


def get_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.get('key')}"

    r = requests.get(url)
    return r.json()


def set_desktop(absolute_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)


def set_desktop_with_weather(weather_id):
    for condition, value in ids.items():
        if weather_id not in value:
            continue

        if os.path.exists(f"{config.get('backgrounds_path')}{condition}.jpg"):
            set_desktop(f"{config.get('backgrounds_path')}\\{condition}.jpg")

        elif os.path.exists(f"{config.get('backgrounds_path')}{condition}.png"):
            set_desktop(f"{config.get('backgrounds_path')}\\{condition}.png")


def main():
    print("Started")

    while True:
        data = get_weather_data(config.get("lat"), config.get("lon"))
        set_desktop_with_weather(data["weather"][0]["id"])
        time.sleep(config.get("refresh_time"))


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)

    main()
