import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://weather_user:your_password_here@localhost:5432/weather_db",
    )
    kma_api_key: str = os.getenv("KMA_API_KEY", "hSgUVllUQCmoFFZZVIApRQ")
    kma_base_url: str = os.getenv("KMA_BASE_URL", "https://apihub.kma.go.kr")
    kma_today_path: str = os.getenv("KMA_TODAY_PATH", "/api/typ01/url/kma_sfcdd.php")
    kma_station_id: str = os.getenv("KMA_STATION_ID", "108")
