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
cp .env.example .env
```

Create PostgreSQL DB/user, then update `.env` as needed.

## 2) Run

```bash
python run.py
```

Open http://localhost:5000

## Notes

- The KMA API has multiple endpoint formats. This project uses `KMA_TODAY_PATH` (default: `/api/typ01/url/kma_sfcdd.php`) and shows the raw response so you can verify/adjust endpoint+params for your account.
- Default API key is pre-filled per your request and can be changed in `.env`.
