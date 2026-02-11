# Weather Today Website

A simple weather website for personal use:
- Account registration and login.
- After login, show today's weather from `https://apihub.kma.go.kr/`.
- Backend: Python (FastAPI).
- Database: PostgreSQL.

## 1) Setup on Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create PostgreSQL DB/user, then update `.env` as needed.

Required `.env` values:

```env
SECRET_KEY=replace-with-a-secret
DATABASE_URL=postgresql+psycopg2://weather_user:your_password_here@localhost:5432/weather_db
KMA_API_KEY=your_kma_api_key
KMA_BASE_URL=https://apihub.kma.go.kr
KMA_TODAY_PATH=/api/typ01/url/sts_ta.php
KMA_LAT=33.2968119
KMA_LON=126.2890204
KMA_HELP=1
KMA_DISP=1
```

## 2) Run

```bash
python run.py
```

Open http://localhost:5000

## Notes

- This project calls `sts_ta.php` with `tm1`, `tm2`, `lat`, `lon`, `help`, and `disp`.
- The dashboard shows a JSON-formatted raw payload (`Raw API response`) for debugging.
- If you get `403 Forbidden`, the API key does not have permission for this endpoint/params. Confirm key scope and allowed API products in KMA.
