import requests

import datetime
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
    # Gets the weather data using the openweathermap API
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.get('key')}"

    r = requests.get(url)
    return r.json()


def find_valid_filepath(weather, time_of_day):
    # Find the valid filepath for the background
    for file_format in VALID_FORMATS:
        path = f"{config.get('backgrounds_path')}\\{time_of_day}_{weather}.{file_format}"

        if os.path.isfile(path):
            return path

    logging.warning(f"No image found for the weather condition \"{weather}\" and the time of day \"{time_of_day}\"")


def set_desktop(time_of_day, weather_condition):
    # Finds the file path for the background image and sets that image as the desktop background
    file_path = find_valid_filepath(weather_condition, time_of_day)

    if file_path is None:
        return

    # Sets the desktop background using the windll
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
    logging.info(f"Set desktop background to {file_path}")


def find_weather_name(weather_id):
    # Find the weather name from the weather IDs
    for condition, value in IDS.items():
        if weather_id not in value:
            continue

        return condition

    logging.warning(f"No background found for ID {weather_id}. To find a list of weather IDs, visit"
                    f" https://openweathermap.org/weather-conditions")


def find_time_of_day():
    # Find if the current time is between sunrise and sunset
    now = datetime.datetime.now()
    sunrise = now.replace(hour=config.get("sunrise_hour"), minute=config.get("sunrise_minute"))
    sunset = now.replace(hour=config.get("sunset_hour"), minute=config.get("sunset_minute"))

    if sunrise < now < sunset:
        return "day"

    return "night"


def main():
    logging.info("Starting...")

    while True:
        # Gather weather data
        logging.debug("Gathering weather data...")
        data = get_weather_data(config.get("lat"), config.get("lon"))
        weather_id = data["weather"][0]["id"]
        logging.debug(f"Collected weather data. ID: {weather_id}")
        condition = find_weather_name(weather_id)

        # Find the time of day
        time_of_day = find_time_of_day()

        # Use this information to set the desktop background
        set_desktop(time_of_day, condition)
        time.sleep(config.get("refresh_time"))


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)

    logging.basicConfig(
        level=config.get("logging_level"),
    )

    main()
