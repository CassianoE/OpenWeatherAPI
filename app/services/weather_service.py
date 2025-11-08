from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.weather_repo import WeatherRepository
from app.clients.openweather import fetch_current_weather
from app.models.weather import Weather


class WeatherService:
    def __init__(self, db: Session):
        self.repo = WeatherRepository(db)

    def ingest(self, city: str, country: str = "BR") -> Weather:
        payload = fetch_current_weather(city, country)
        return self.repo.insert_from_payload(city, country, payload)

    def list(self, city: Optional[str], limit: int) -> List[Weather]:
        return self.repo.list(city, limit)
