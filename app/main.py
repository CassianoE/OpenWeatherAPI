from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.api.health import router as health_router
from app.api.v1.weather import router as weather_router


def create_app() -> FastAPI:
    app = FastAPI(title="Weather API")

    # routers
    app.include_router(health_router)
    app.include_router(weather_router)

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
