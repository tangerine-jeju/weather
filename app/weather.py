from __future__ import annotations

import json
from datetime import datetime

import requests

from .config import Config


def fetch_today_weather(config: Config) -> dict:
    url = f"{config.kma_base_url.rstrip('/')}{config.kma_today_path}"
    today = datetime.now().strftime("%Y%m%d")
    params = {
        "authKey": config.kma_api_key,
        "tm1": today,
        "tm2": today,
        "lat": config.kma_lat,
        "lon": config.kma_lon,
        "help": config.kma_help,
        "disp": config.kma_disp,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        return {
            "source": response.url,
            "raw": data,
            "raw_pretty": json.dumps(data, ensure_ascii=False, indent=2),
            "summary": _json_summary(data),
        }

    text = response.text.strip()
    structured = {
        "content_type": content_type or "text/plain",
        "rows": [line for line in text.splitlines() if line.strip()],
    }
    return {
        "source": response.url,
        "raw": structured,
        "raw_pretty": json.dumps(structured, ensure_ascii=False, indent=2),
        "summary": _text_summary(text),
    }


def _json_summary(data: dict) -> str:
    if not data:
        return "No weather data returned from API."

    if isinstance(data, dict):
        for key in ("result", "data", "response"):
            if key in data:
                return f"Today's weather data received in '{key}' field."

    return "Today's weather data loaded successfully."


def _text_summary(text: str) -> str:
    if not text:
        return "No weather data returned from API."

    lines = [line for line in text.splitlines() if line.strip()]
    if lines:
        return lines[0][:180]
    return "Today's weather data loaded successfully."
