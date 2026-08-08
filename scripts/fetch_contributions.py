import json
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "PyRobix-Tech"
URL = f"https://github.com/users/{USERNAME}/contributions"
ROOT = Path(__file__).resolve().parents[1]

response = requests.get(URL, headers={"User-Agent": "PyRobix-Tech-profile"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

days = []
for cell in soup.select("[data-date][data-level]"):
    day = cell.get("data-date")
    if day and not any(item["date"] == day for item in days):
        count = cell.get("data-count")
        if count is None:
            tooltip_id = cell.get("id")
            tooltip = soup.select_one(f'tool-tip[for="{tooltip_id}"]') if tooltip_id else None
            text = tooltip.get_text(" ", strip=True) if tooltip else "0"
            first = text.split()[0].replace(",", "")
            count = first if first.isdigit() else "0"
        days.append({"date": day, "count": int(count), "level": int(cell.get("data-level", 0))})

if not days:
    raise RuntimeError("GitHub returned no public contribution cells")

days.sort(key=lambda item: item["date"])
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "contributions.json").write_text(
    json.dumps({"username": USERNAME, "updated": date.today().isoformat(), "days": days}, indent=2),
    encoding="utf-8",
)
