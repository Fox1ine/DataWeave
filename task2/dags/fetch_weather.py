import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from logg_config import logger

dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path)


def fetch_weather_raw():
    """Fetches raw weather data from OpenWeather API and saves it as JSON."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    CITY = os.getenv("CITY")
    DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")

    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = os.path.join(DATA_RAW_PATH, f"current_raw_{now_str}.json")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    logger.info(f"Fetching weather data for {CITY} from {url}")

    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"API Error: {response.status_code} - {response.text}")
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    with open(raw_file, "w") as f:
        json.dump(data, f)

    logger.info(f"Raw weather data saved to {raw_file}")


def process_weather_data():
    """Processes raw weather data and saves it in Parquet format."""
    DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
    DATA_TEMP_PATH = os.getenv("DATA_TEMP_PATH")
    DATA_WIND_PATH = os.getenv("DATA_WIND_PATH")

    raw_files = sorted([f for f in os.listdir(DATA_RAW_PATH) if f.startswith("current_raw")])
    if not raw_files:
        logger.error("No raw data found for processing!")
        raise Exception("No raw data found for processing!")

    latest_raw_file = os.path.join(DATA_RAW_PATH, raw_files[-1])
    with open(latest_raw_file, "r") as f:
        data = json.load(f)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    day_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("time-%H-%M-%S")

    temp_day_folder = os.path.join(DATA_TEMP_PATH, f"minsk_{day_str}_temp")
    wind_day_folder = os.path.join(DATA_WIND_PATH, f"minsk_{day_str}_wind")

    os.makedirs(temp_day_folder, exist_ok=True)
    os.makedirs(wind_day_folder, exist_ok=True)

    temp_data = {
        "datetime": timestamp,
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "pressure": data["main"]["pressure"],
    }

    wind_data = {
        "datetime": timestamp,
        "speed": data["wind"]["speed"],
        "deg": data["wind"]["deg"],
        "gust": data["wind"].get("gust", None)
    }

    temp_file = os.path.join(temp_day_folder, f"{time_str}.parquet")
    wind_file = os.path.join(wind_day_folder, f"{time_str}.parquet")

    temp_df = pd.DataFrame([temp_data])
    wind_df = pd.DataFrame([wind_data])

    temp_df.to_parquet(temp_file, engine="pyarrow", index=False)
    wind_df.to_parquet(wind_file, engine="pyarrow", index=False)

    logger.info(f"Processed weather data saved:\n  {temp_file}\n  {wind_file}")


if __name__ == "__main__":
    fetch_weather_raw()
    process_weather_data()
