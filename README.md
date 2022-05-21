# adaptive-desktop
Adaptive desktops for Windows based off of weather and time (time coming soon)

## Setup:
1. Input your longitude and latitude in `config.json` to the `lon` and `lat` values(you can google the coordinates of your city)
2. Get your API key at https://home.openweathermap.org/api_keys after making an account, then add it to the JSON file
3. Replace the images in the backgrounds folder with your own images. `.png`, `.jpg`, `.jpeg`, and `.gif` are supported.
4. Add your absolute file path using double backslashes as the seperator to the JSON file, e.g:
```
C:\\Users\\myUser\\Desktop\\Backgrounds
```
**This needs to be the _absolute_ file path starting with your drive letter, not the relative file path.**

## Image names:
For version 1.0 or later, image names need to be one of the following depending on the weather condition and time of day:
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
