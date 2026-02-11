from __future__ import annotations

from datetime import datetime

import requests

from .config import Config


def fetch_today_weather(config: Config) -> dict:
    url = f"{config.kma_base_url.rstrip('/')}{config.kma_today_path}"
    params = {
        "authKey": config.kma_api_key,
        "stn": config.kma_station_id,
        "tm": datetime.now().strftime("%Y%m%d"),
        "help": 0,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        return {"source": url, "raw": data, "summary": _json_summary(data)}

    text = response.text.strip()
    return {"source": url, "raw": text, "summary": _text_summary(text)}


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
