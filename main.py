import requests

import datetime
import logging
import ctypes
import time
import json
import os


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


def find_time_of_day():
    # Find if the current time is between sunrise and sunset
    now = datetime.datetime.now()
    sunrise = now.replace(hour=config.get("sunrise_hour"), minute=config.get("sunrise_minute"))
    sunset = now.replace(hour=config.get("sunset_hour"), minute=config.get("sunset_minute"))

    if sunrise <= now <= sunset:
        return "day"

    return "night"


def main():
    logging.info("Starting...")

    while True:
        # Gather weather data
        logging.debug("Gathering weather data...")

        try:
            data = get_weather_data(config.get("lat"), config.get("lon"))

        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error. Retrying in {config.get('refresh_time')} seconds")
            time.sleep(config.get('refresh_time'))
            continue

        # Check if the data is valid
        if data.get("cod") != 200:
            logging.critical(f"Error code {data.get('cod')} recieved: {data.get('message')}")
            time.sleep(config.get("refresh_time"))
            continue

        # Set the weather conditions to variables
        weather_id = data["weather"][0]["id"]
        condition = data["weather"][0]["main"].lower() if weather_id not in (801, 802) else "clear"
        logging.debug(f"Collected weather data. ID: {weather_id}, condition: {condition}")

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
