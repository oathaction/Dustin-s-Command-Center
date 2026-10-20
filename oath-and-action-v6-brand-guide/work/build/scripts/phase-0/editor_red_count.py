"""Count Pillar Red elements per application figure in V5 Polished chapters.

Exempt, per V5 rule R5: the grid lever (circle at 111.75,111.75) and the
wordmark symbol. Everything else drawn or filled in red is counted.
Usage: python3 -I editor_red_count.py <chapters-dir> <chapter-stem> [...]
"""
import re
import sys
from pathlib import Path

RED = re.compile(r'(#E63946|var\(--red\)|class="btn red|class="[^"]*\bred\b)', re.I)
LEVER = re.compile(r'<circle cx="111\.75" cy="111\.75" r="[0-9.]+" fill="#E63946"', re.I)
for stem in sys.argv[2:]:
    html = Path(sys.argv[1], stem + ".html").read_text(encoding="utf-8")
    for fig in re.finditer(r"<figure\b.*?</figure>", html, re.S):
        body = fig.group(0)
        label = re.findall(r'<figcaption[^>]*>(.*?)</figcaption>', body, re.S)
        label = re.sub(r"<[^>]+>", " ", label[-1] if label else "")
        label = re.sub(r"\s+", " ", label).strip()[:70]
        total = len(RED.findall(body))
        levers = len(LEVER.findall(body))
        amps = len(re.findall(r'href="#amp(-16)?"', body))
        if total - levers > 1:
            print(f"{stem} | {label} | red marks {total - levers} (levers exempt {levers}) | amp uses {amps}")
