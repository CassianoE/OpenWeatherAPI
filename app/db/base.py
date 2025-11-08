from sqlalchemy.orm import declarative_base

Base = declarative_base()

# registre aqui os modelos para o create_all enxergar
from app.models.weather import Weather  # noqa: F401
