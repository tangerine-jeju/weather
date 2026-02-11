import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://weather_user:your_password_here@localhost:5432/weather_db",
    )
    kma_api_key: str = os.getenv("KMA_API_KEY", "")
    kma_base_url: str = os.getenv("KMA_BASE_URL", "https://apihub.kma.go.kr")
    kma_today_path: str = os.getenv("KMA_TODAY_PATH", "/api/typ01/url/sts_ta.php")
    kma_lat: str = os.getenv("KMA_LAT", "33.2968119")
    kma_lon: str = os.getenv("KMA_LON", "126.2890204")
    kma_help: str = os.getenv("KMA_HELP", "1")
    kma_disp: str = os.getenv("KMA_DISP", "1")
