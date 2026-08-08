from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pyrobix-logo.png"
OUTPUT = ROOT / "pyrobix-ascii.svg"

COLS = 66
ROWS = 48
RAMP = "@%#*+=-:. "

image = Image.open(SOURCE).convert("RGB")
gray = ImageOps.grayscale(image)
gray = ImageEnhance.Contrast(gray).enhance(1.8)
gray = gray.resize((COLS, ROWS), Image.Resampling.LANCZOS)

lines = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        value = gray.getpixel((x, y))
        # The source has a dark background: suppress it and map brighter logo
        # pixels to denser characters.
        if value < 32:
            chars.append(" ")
        else:
            index = max(0, min(len(RAMP) - 2, int((255 - value) / 255 * (len(RAMP) - 2))))
            chars.append(RAMP[index])
    lines.append("".join(chars).rstrip())

escaped = lambda text: text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
rows = []
for index, line in enumerate(lines):
    delay = index * 0.035
    rows.append(
        f'<text class="row" x="24" y="{62 + index * 8.1:.1f}" '
        f'style="animation-delay:{delay:.3f}s">{escaped(line)}</text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="740" height="500" viewBox="0 0 740 500" role="img" aria-label="Animated ASCII PYROBIX logo">
<style>.row{{fill:#f0883e;font:7.4px ui-monospace,Consolas,monospace;white-space:pre;opacity:0;animation:type .28s ease forwards}}@keyframes type{{from{{opacity:0;transform:translateX(-7px)}}to{{opacity:1;transform:none}}}}</style>
<rect width="740" height="500" rx="16" fill="#0d1117"/><rect x="1" y="1" width="738" height="498" rx="15" fill="none" stroke="#30363d" stroke-width="2"/>
<circle cx="24" cy="24" r="5" fill="#ff5f56"/><circle cx="41" cy="24" r="5" fill="#ffbd2e"/><circle cx="58" cy="24" r="5" fill="#27c93f"/>
<text x="370" y="29" fill="#8b949e" font="12px ui-monospace,Consolas,monospace" text-anchor="middle">pyrobix@github:~$ ./logo.sh</text>
{''.join(rows)}
</svg>'''
OUTPUT.write_text(svg, encoding="utf-8")
