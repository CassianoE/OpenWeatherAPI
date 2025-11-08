from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.weather import WeatherOut
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/v1", tags=["weather"])


@router.post("/ingest", response_model=WeatherOut)
def ingest(
    city: str = Query(...),
    country: str = Query("BR"),
    db: Session = Depends(get_db),
):
    try:
        return WeatherService(db).ingest(city=city, country=country)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/weather", response_model=List[WeatherOut])
def get_weather(
    city: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return WeatherService(db).list(city=city, limit=limit)
