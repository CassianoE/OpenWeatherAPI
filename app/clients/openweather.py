import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.core.config import settings

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

_session = requests.Session()
_session.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=False,  # retry em qualquer método
        )
    ),
)


def fetch_current_weather(city: str, country: str) -> dict:
    params = {
        "q": f"{city},{country}",
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }
    r = _session.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()
