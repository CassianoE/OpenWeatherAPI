from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .database import Base, engine, get_db
from .models import Weather
from .openweather import fetch_weather

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest(city: str, country: str = "BR", db: Session = Depends(get_db)):
    try:
        data = fetch_weather(city, country)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    record = Weather(
        city=city,
        country=country,
        temp=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        weather_main=data["weather"][0]["main"],
        weather_description=data["weather"][0]["description"],
        raw=data,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

@app.get("/weather")
def get_weather(
    city: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Weather).order_by(Weather.timestamp.desc())

    if city:
        query = query.filter(Weather.city.ilike(f"%{city}%"))

    results = query.limit(limit).all()
    return results
