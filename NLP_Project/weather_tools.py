# weather_tools.py

import random


def get_temperature(location: str, datetime_str: str) -> float:
    seed = hash((location.lower(), datetime_str)) % 10_000
    random.seed(seed)
    return round(random.uniform(4, 32), 1)


def get_precipitation(location: str, datetime_str: str) -> float:
    seed = hash(("rain", location.lower(), datetime_str)) % 10_000
    random.seed(seed)
    return round(random.uniform(0, 25), 1)


def get_weather(location: str, datetime_str: str) -> dict:
    seed = hash(("weather", location.lower(), datetime_str)) % 10_000
    random.seed(seed)

    temperature = round(random.uniform(4, 32), 1)
    precipitation = round(random.uniform(0, 25), 1)

    if precipitation < 2:
        summary = "ensoleillé"
    elif precipitation < 8:
        summary = "nuageux"
    else:
        summary = "pluvieux"

    return {
        "ville": location,
        "datetime": datetime_str,
        "resume": summary,
        "temperature_c": temperature,
        "precipitations_mm": precipitation,
    }
