import requests

import logging
import ctypes
import time
import json
import os

IDS = {
    "thunderstorm": (200, 201, 202, 210, 211, 212, 221, 230, 231, 232),
    "drizzle": (300, 301, 302, 310, 311, 312, 313, 314, 321),
    "rain": (500, 501, 502, 503, 504, 511, 520, 521, 522, 531),
    "snow": (600, 601, 602, 611, 612, 615, 616, 620, 621, 622),
    "atmosphere": (701, 711, 721, 731, 741, 751, 761, 762, 771, 781),
    "clear": (800, 801, 802),
    "clouds": (803, 804, )
}

VALID_FORMATS = ("png", "jpg", "jpeg", "gif")


def get_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.get('key')}"

    r = requests.get(url)
    return r.json()


def set_desktop(absolute_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)


def set_desktop_with_weather(weather_id):
    for condition, value in IDS.items():
        if weather_id not in value:
            continue

        for file_format in VALID_FORMATS:
            path = f"{config.get('backgrounds_path')}\\{condition}.{file_format}"
            if os.path.exists(path):
                set_desktop(path)
                break

        else:
            logging.warning(f"No background found for ID {weather_id}. To find a list of weather IDs, visit"
                            f" https://openweathermap.org/weather-conditions")


def main():
    logging.info("Starting...")

    while True:
        logging.debug("Gathering weather data...")
        data = get_weather_data(config.get("lat"), config.get("lon"))

        weather_id = data["weather"][0]["id"]
        logging.debug(f"Collected weather data. ID: {weather_id}")
        set_desktop_with_weather(weather_id)
        time.sleep(config.get("refresh_time"))


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)

    logging.basicConfig(
        level=config.get("logging_level"),
    )

    main()
