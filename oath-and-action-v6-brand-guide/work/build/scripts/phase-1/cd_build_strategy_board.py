"""Creative director, Phase 1: build the Strategy and Direction board.

Reads the template in work/boards/phase-1/strategy/, inlines V5 Polished vector
masters from work/extract/v5-polished/sprite/ (read only), draws the proposed hinge
loop and the Loop R9 sketch as inline SVG, and writes
work/boards/20261021_Strategy-And-Direction-Board.html.

Run: python3 -I work/build/scripts/phase-1/cd_build_strategy_board.py <project root>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SPRITE = ROOT / "work/extract/v5-polished/sprite"
TEMPLATE = ROOT / "work/boards/phase-1/strategy/strategy-board.template.html"
CHECKS = ROOT / "work/boards/phase-1/strategy/20261021_Board-Check-Results.json"
OUT = ROOT / "work/boards/20261021_Strategy-And-Direction-Board.html"

CHARCOAL, RED, MUTED = "#121212", "#E63946", "#45494F"


def read_svg(name):
    return (SPRITE / f"{name}.svg").read_text(encoding="utf-8")


def path_d(name):
    m = re.search(r'<path fill="currentColor" d="([^"]+)"', read_svg(name))
    return m.group(1)


def viewbox(name):
    return re.search(r'viewBox="([^"]+)"', read_svg(name)).group(1)


def amp_inner():
    svg = read_svg("amp")
    return re.search(r"<g fill=\"currentColor\">(.*?)</g>", svg, re.S).group(1)


AMP_VIEWBOX = "-3 -3 95.62 106.61"  # padded so the loop top and tail are not clipped (Phase 0 finding)


def wordmark():
    svg = read_svg("wordmark")
    svg = re.sub(r"<title>.*?</title>", "", svg)
    svg = svg.replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', "")
    svg = svg.replace(' style="color:#121212"', ' class="wm" role="img" aria-label="Oath &amp; Action wordmark, V5 Polished master"')
    return svg


def amp_small():
    return (f'<svg viewBox="{AMP_VIEWBOX}" aria-hidden="true" focusable="false">'
            f'<g fill="currentColor">{amp_inner()}</g></svg>')


def loop_svg():
    oath_vb, action_vb = viewbox("word-oath"), viewbox("word-action")
    ow = 358.67 * 30 / 108
    aw = 502.43 * 30 / 108
    ox, ax = 24, 520 - 24 - aw
    cx, cy, r, R = 240, 120, 38, 72
    import math

    def pt(deg):
        a = math.radians(deg)
        return round(cx + R * math.cos(a), 1), round(cy + R * math.sin(a), 1)

    t0, t1, b0, b1 = pt(205), pt(335), pt(25), pt(155)
    amp_h = 50
    amp_w = amp_h * 95.62 / 106.61
    parts = [
        '<svg viewBox="0 30 520 182" role="img" aria-label="Proposed hinge loop: OATH on the left and ACTION on the right, '
        'joined by a line through a circle around the red ampersand. One arc runs clockwise over the top from OATH to ACTION, '
        'and a second arc returns under the bottom from ACTION to OATH.">',
        f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0 0L10 5L0 10z" fill="{CHARCOAL}"/></marker></defs>',
        f'<svg x="{ox}" y="105" width="{ow:.1f}" height="30" viewBox="{oath_vb}"><path fill="{CHARCOAL}" d="{path_d("word-oath")}"/></svg>',
        f'<svg x="{ax:.1f}" y="105" width="{aw:.1f}" height="30" viewBox="{action_vb}"><path fill="{CHARCOAL}" d="{path_d("word-action")}"/></svg>',
        f'<g stroke="{CHARCOAL}" stroke-width="1.5" fill="none">'
        f'<line x1="132" y1="{cy}" x2="{cx - r}" y2="{cy}"/><line x1="{cx + r}" y1="{cy}" x2="348" y2="{cy}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
        f'<path d="M{t0[0]} {t0[1]} A{R} {R} 0 0 1 {t1[0]} {t1[1]}" marker-end="url(#ah)"/>'
        f'<path d="M{b0[0]} {b0[1]} A{R} {R} 0 0 1 {b1[0]} {b1[1]}" marker-end="url(#ah)"/></g>',
        f'<g fill="{CHARCOAL}"><circle cx="132" cy="{cy}" r="4"/><circle cx="{cx - r}" cy="{cy}" r="4"/>'
        f'<circle cx="{cx + r}" cy="{cy}" r="4"/><circle cx="348" cy="{cy}" r="4"/></g>',
        f'<svg x="{cx - amp_w / 2:.1f}" y="{cy - amp_h / 2:.1f}" width="{amp_w:.1f}" height="{amp_h}" viewBox="{AMP_VIEWBOX}">'
        f'<g fill="{RED}">{amp_inner()}</g></svg>',
        "</svg>",
    ]
    labels = (f'<div class="looplabels" aria-hidden="true"><span style="left:{(ox + ow / 2) / 520 * 100:.1f}%">Understand</span>'
              f'<span style="left:{(ax + aw / 2) / 520 * 100:.1f}%">Impact</span></div>')
    return "".join(parts) + labels


def r9_svg():
    def node(x, y, l1, l2):
        return (f'<rect x="{x}" y="{y}" width="150" height="56" fill="#FFFFFF" stroke="{CHARCOAL}" stroke-width="1.5"/>'
                f'<text x="{x + 75}" y="{y + 24}" text-anchor="middle">{l1}</text>'
                f'<text x="{x + 75}" y="{y + 44}" text-anchor="middle">{l2}</text>')

    dotted = f'stroke="{CHARCOAL}" stroke-width="2" stroke-dasharray="0.1 5" stroke-linecap="round" fill="none" marker-end="url(#ah9)"'
    return "".join([
        '<svg viewBox="0 0 360 236" role="img" aria-label="Loop R9 sketch: effective participation raises accountable delivery, '
        'which raises warranted trust, which raises effective participation. Every link is positive and drawn dotted as a hypothesis.">',
        f'<defs><marker id="ah9" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M0 0L10 5L0 10z" fill="{CHARCOAL}"/></marker></defs>',
        f'<g font-family="Inter, Helvetica Neue, Arial, sans-serif" font-size="15" fill="{CHARCOAL}">',
        node(0, 8, "Effective", "participation"), node(210, 8, "Accountable", "delivery"), node(105, 172, "Warranted", "trust"),
        f'<path d="M154 36 L204 36" {dotted}/>', f'<path d="M296 68 L236 166" {dotted}/>', f'<path d="M124 166 L64 68" {dotted}/>',
        '<g font-weight="700" font-size="17"><text x="179" y="27" text-anchor="middle">+</text>'
        '<text x="284" y="124" text-anchor="middle">+</text><text x="76" y="124" text-anchor="middle">+</text></g>',
        f'<circle cx="180" cy="104" r="21" fill="none" stroke="{CHARCOAL}" stroke-width="1.5"/>'
        '<text x="180" y="109" text-anchor="middle" font-weight="700">R9</text>',
        "</g></svg>",
    ])


def li(items):
    return "".join(f"<li>{i}</li>" for i in items)


def main():
    html = TEMPLATE.read_text(encoding="utf-8")
    checks = json.loads(CHECKS.read_text(encoding="utf-8")) if CHECKS.exists() else {}
    fill = {
        "{{WORDMARK}}": wordmark(),
        "{{LOOP_SVG}}": loop_svg(),
        "{{R9_SVG}}": r9_svg(),
        "{{AMP_SMALL}}": amp_small(),
        "{{A11Y_SCORE}}": checks.get("a11y_score", "Pending"),
        "{{A11Y_REASON}}": checks.get("a11y_reason", "Board checks not yet run."),
        "{{CHECKED}}": li(checks.get("checked", ["Board checks not yet run."])),
        "{{NOT_CHECKED}}": li(checks.get("not_checked", ["Board checks not yet run."])),
    }
    for k, v in fill.items():
        html = html.replace(k, v)
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
    if left:
        raise SystemExit(f"Unfilled placeholders: {left}")
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
