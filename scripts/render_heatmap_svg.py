import html
import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
payload = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
values = {datetime.strptime(d["date"], "%Y-%m-%d").date(): d for d in payload["days"]}
end = max(values, default=date.today())
start = end - timedelta(days=370)
start -= timedelta(days=(start.weekday() + 1) % 7)
palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
cells = []
total = 0
for offset in range(371):
    current = start + timedelta(days=offset)
    item = values.get(current, {"count": 0, "level": 0})
    total += item["count"]
    week, row = offset // 7, offset % 7
    delay = (week + row) * 0.012
    cells.append(
        f'<rect class="day" x="{58 + week * 14}" y="{78 + row * 14}" width="10" height="10" rx="2" '
        f'fill="{palette[min(item["level"], 4)]}" style="animation-delay:{delay:.3f}s">'
        f'<title>{item["count"]} contributions on {current.isoformat()}</title></rect>'
    )
months = []
last_month = None
for week in range(53):
    current = start + timedelta(days=week * 7)
    if current.month != last_month and week < 51:
        months.append(f'<text x="{58 + week * 14}" y="62">{current.strftime("%b")}</text>')
        last_month = current.month
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="220" viewBox="0 0 860 220" role="img" aria-label="Contribution heatmap for {html.escape(payload['username'])}">
<style>text{{fill:#8b949e;font:12px ui-monospace,Consolas,monospace}}.day{{opacity:0;transform:translateY(8px);animation:in .35s ease forwards}}@keyframes in{{to{{opacity:1;transform:none}}}}</style>
<rect width="860" height="220" rx="16" fill="#0d1117"/><rect x=".5" y=".5" width="859" height="219" rx="15.5" fill="none" stroke="#30363d"/>
<text x="24" y="32" fill="#3fb950">$ git log --contributions</text>{''.join(months)}
<text x="23" y="90">M</text><text x="23" y="118">W</text><text x="23" y="146">F</text>{''.join(cells)}
<text x="24" y="196">{total:,} contributions in the displayed year</text><text x="690" y="196">Less  ▪ ▪ ▪ ▪ ▪  More</text>
</svg>'''
(ROOT / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")
