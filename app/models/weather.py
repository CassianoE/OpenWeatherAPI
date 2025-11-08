from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base import Base


class Weather(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)

    temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)

    weather_main = Column(String)
    weather_description = Column(String)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSONB)
