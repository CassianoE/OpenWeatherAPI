from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.weather import Weather


class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_from_payload(self, city: str, country: str, payload: dict) -> Weather:
        rec = Weather(
            city=city,
            country=country,
            temp=payload["main"].get("temp"),
            feels_like=payload["main"].get("feels_like"),
            humidity=payload["main"].get("humidity"),
            wind_speed=payload.get("wind", {}).get("speed"),
            weather_main=(payload.get("weather") or [{}])[0].get("main"),
            weather_description=(payload.get("weather") or [{}])[0].get("description"),
            raw=payload,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def list(self, city: Optional[str], limit: int) -> List[Weather]:
        q = self.db.query(Weather).order_by(desc(Weather.timestamp))
        if city:
            q = q.filter(Weather.city.ilike(f"%{city}%"))
        return q.limit(limit).all()
