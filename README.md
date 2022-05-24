# adaptive-desktop
Adaptive desktops for Windows based off of weather and time

## Purpose
This program automatically changes the desktop background based off of weather and time. This program is fully customizeable, meaning images can be whatever you like and the treshold for daytime and nighttime is also customizeable.

## Setup
1. Install Python (if not already installed) and the `requests` depencency using `pip install requests`
2. Input your longitude and latitude in `config.json` to the `lon` and `lat` values (you can google the coordinates of your city)
3. Get your API key at https://home.openweathermap.org/api_keys after making an account, then add it to the JSON file
4. Replace the images in the backgrounds folder with your own images. `.png`, `.jpg`, `.jpeg`, and `.gif` are supported.
5. Add your absolute file path using double backslashes as the seperator to the JSON file, e.g:
```
C:\\Users\\myUser\\Desktop\\Backgrounds
```
**This needs to be the _absolute_ file path starting with your drive letter, not the relative file path.**

## Image names
Here is a list of valid image file names:
- day_thunderstorm
- night_thunderstorm
- day_drizzle
- night_drizzle
- day_rain
- night_rain
- day_snow
- night_snow
- day_atmosphere
- night_atmosphere
- day_clear
- night_clear
- day_clouds
- night_clouds
