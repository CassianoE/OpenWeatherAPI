from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


class WeatherOut(BaseModel):
    id: int
    city: str
    country: str
    temp: Optional[float] = None
    feels_like: Optional[float] = None
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    weather_main: Optional[str] = None
    weather_description: Optional[str] = None
    timestamp: datetime
    raw: Optional[Any] = None

    class Config:
        from_attributes = True  # (Pydantic v2) converte ORM → schema
