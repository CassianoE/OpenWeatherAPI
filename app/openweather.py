import os
import requests


def fetch_weather(city: str, country: str = "BR"):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY não foi definida no ambiente")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city},{country}",
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # lança erro se API retornar erro

    return response.json()
